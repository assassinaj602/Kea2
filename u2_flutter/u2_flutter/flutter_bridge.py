import re
import time
import logging
import websocket
import adbutils
from typing import Optional, Tuple

logger = logging.getLogger("u2_flutter.bridge")

class FlutterBridge:
    def _find_available_port(self, start_port=8181, max_attempts=100) -> int:
        """Find an available local port for ADB forwarding."""
        import socket
        for port in range(start_port, start_port + max_attempts):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('127.0.0.1', port))
                    return port
            except OSError:
                continue
        raise RuntimeError("No available port found")

    def __init__(self, device, local_port: Optional[int] = None):
        """
        Initialize the Flutter Bridge.
        
        Args:
            device: A uiautomator2.Device instance.
            local_port: Optional local port to forward the Dart VM service to.
                        If None, an available port will be auto-allocated.
        """
        self.device = device
        self._custom_port_requested = local_port is not None
        self.local_port = local_port if self._custom_port_requested else self._find_available_port()
        self.remote_port: Optional[int] = None
        self.auth_token: Optional[str] = None
        self.ws: Optional[websocket.WebSocket] = None
        
        # Extract serial if available, or fall back to default
        self.serial = getattr(device, "_serial", None) or getattr(device, "serial", None)
        self.adb = adbutils.adb.device(serial=self.serial) if self.serial else adbutils.adb

    def find_observatory_info(self) -> Tuple[int, str]:
        """
        Finds the Dart VM Service port and auth token from device logcat.
        
        Returns:
            Tuple[int, str]: The remote VM service port and the auth token.
        """
        logger.info("Scanning logcat for Dart VM Service URI...")
        logcat_lines = self.device.shell("logcat -d").output
        
        # Updated regex to capture both port AND optional auth token path
        # Example: http://127.0.0.1:42769/aBcDeFg1234=/
        pattern = re.compile(
            r"(?:The Dart VM service is listening on|Observatory listening on)\s+http://127.0.0.1:(\d+)(?:/([a-zA-Z0-9_\-=]+)/?)?"
        )
        
        for line in reversed(logcat_lines.splitlines()):
            match = pattern.search(line)
            if match:
                port = int(match.group(1))
                token = match.group(2) or ""
                logger.info(f"Found Dart VM Service port: {port}, auth token: '{token}'")
                return port, token
                
        raise RuntimeError("Could not find Dart VM Service port in logcat. Make sure the Flutter app is running in debug or profile mode.")

    def forward_port(self, remote_port: int):
        """
        Sets up ADB port forwarding from local_port to remote_port.
        """
        logger.info(f"Forwarding local tcp:{self.local_port} to remote tcp:{remote_port}")
        try:
            self.adb.forward(f"tcp:{self.local_port}", f"tcp:{remote_port}")
        except Exception as e:
            logger.error(f"Failed to forward port: {e}")
            raise

    def remove_forward(self):
        """
        Removes the ADB port forwarding.
        """
        if self.remote_port:
            logger.info(f"Removing port forwarding for local tcp:{self.local_port}")
            try:
                self.adb.forward_remove(f"tcp:{self.local_port}")
            except Exception as e:
                logger.debug(f"Error removing port forwarding: {e}")

    def attach(self) -> str:
        """
        Finds the VM service port and auth token, forwards it, and connects via WebSocket.
        
        Returns:
            str: The WebSocket URL.
        """
        if not self._custom_port_requested:
            self.local_port = self._find_available_port()
            
        self.remote_port, self.auth_token = self.find_observatory_info()
        self.forward_port(self.remote_port)
        
        # Append auth token to ws URL if present
        if self.auth_token:
            ws_url = f"ws://127.0.0.1:{self.local_port}/{self.auth_token}/ws"
        else:
            ws_url = f"ws://127.0.0.1:{self.local_port}/ws"
            
        logger.info(f"Connecting to WebSocket VM Service: {ws_url}")
        
        # Attempt WebSocket connection with retries
        for attempt in range(5):
            try:
                ws = websocket.WebSocket()
                ws.connect(ws_url, timeout=5)
                self.ws = ws
                logger.info("Successfully connected to Dart VM Service!")
                return ws_url
            except Exception as e:
                logger.warning(f"Connection attempt {attempt + 1} failed: {e}")
                time.sleep(1)
                
        self.remove_forward()
        raise ConnectionError("Failed to connect to Dart VM Service WebSocket after multiple attempts.")

    def detach(self):
        """
        Closes the WebSocket connection and removes port forwarding.
        """
        if self.ws:
            try:
                self.ws.close()
                logger.info("WebSocket connection closed.")
            except Exception as e:
                logger.debug(f"Error closing WebSocket: {e}")
            finally:
                self.ws = None
                
        self.remove_forward()
        self.remote_port = None
        self.auth_token = None
        if not self._custom_port_requested:
            self.local_port = None
