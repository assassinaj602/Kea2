"""Download historical Fastbot native libraries into a local cache."""

from __future__ import annotations

import os
import platform
import re
import shutil
import tempfile
from pathlib import Path
from typing import Callable, Iterable
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


REPOSITORY = "ecnusse/Kea2"
GITEE_REPOSITORY = "XixianLiang/Kea2"
ABIS = ("armeabi-v7a", "arm64-v8a", "x86", "x86_64")
LIBRARY_NAME = "libfastbot_native.so"
GIT_REF_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


def default_cache_dir() -> Path:
    if platform.system() == "Darwin":
        cache_home = Path.home() / "Library" / "Caches"
    else:
        cache_home = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    return cache_home / "kea2" / "fastbot_libs"


def library_path(cache_dir: Path, version: str, abi: str) -> Path:
    return cache_dir / version / abi / LIBRARY_NAME


def is_valid_library(path: Path) -> bool:
    try:
        with path.open("rb") as library:
            return library.read(4) == b"\x7fELF"
    except OSError:
        return False


def raw_library_urls(version: str, abi: str) -> tuple[tuple[str, str], ...]:
    path = f"kea2/assets/fastbot_libs/{abi}/{LIBRARY_NAME}"
    return (
        ("GitHub", f"https://raw.githubusercontent.com/{REPOSITORY}/{version}/{path}"),
        ("Gitee", f"https://gitee.com/{GITEE_REPOSITORY}/raw/{version}/{path}"),
    )


def download_file(url: str, destination: Path, timeout: int) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=destination.parent, prefix=f".{destination.name}.", delete=False) as output:
        temporary_path = Path(output.name)
        try:
            with urlopen(url, timeout=timeout) as response:
                shutil.copyfileobj(response, output)
            output.flush()
            os.fsync(output.fileno())
            if not is_valid_library(temporary_path):
                raise ValueError("downloaded file is not a valid ELF shared library")
            temporary_path.replace(destination)
        except Exception:
            temporary_path.unlink(missing_ok=True)
            raise


def missing_abis(cache_dir: Path, version: str, force: bool = False) -> Iterable[str]:
    for abi in ABIS:
        if force or not is_valid_library(library_path(cache_dir, version, abi)):
            yield abi


def ensure_libraries(
    version: str,
    cache_dir: Path | None = None,
    timeout: int = 30,
    force: bool = False,
    progress: Callable[[str], None] | None = None,
) -> Path:
    """Ensure all ABI libraries for *version* are cached and return their root."""
    if not GIT_REF_PATTERN.fullmatch(version):
        raise ValueError("--fastbot-so-version must contain only letters, digits, '.', '_' and '-'")
    if timeout <= 0:
        raise ValueError("timeout must be greater than 0")

    cache_dir = cache_dir or default_cache_dir()
    pending = list(missing_abis(cache_dir, version, force=force))
    if not pending:
        return cache_dir / version

    for abi in pending:
        target = library_path(cache_dir, version, abi)
        errors = []
        for source, url in raw_library_urls(version, abi):
            if progress:
                progress(f"Downloading Fastbot SO {version} ({abi}) from {source}: {url}")
            try:
                download_file(url, target, timeout)
                break
            except HTTPError as error:
                errors.append(f"{source}: HTTP {error.code}")
            except (URLError, OSError, ValueError) as error:
                errors.append(f"{source}: {error}")
        else:
            raise RuntimeError(f"Failed to download Fastbot SO {version} for {abi}; {'; '.join(errors)}")

    return cache_dir / version
