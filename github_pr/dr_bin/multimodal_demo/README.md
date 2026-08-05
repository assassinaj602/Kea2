# 🚀 Qwen3-VL Mobile Vision AI (On-Device Flutter App)

An ultra-fast, privacy-first **On-Device Multimodal Vision AI** Flutter application running **Qwen3-VL-2B-Instruct** locally on Android using hardware-accelerated C++ FFI bindings (`llama.cpp` + `llamadart`). Zero cloud APIs required!

---

## ✨ Features

- 📱 **100% On-Device Multimodal Inference**: Describe images, answer complex visual questions, and extract visual insights completely offline.
- ⚡ **Hardware Acceleration**: Optimized for `arm64-v8a` Android devices leveraging Vulkan & Impeller GPU backends.
- 🛑 **Real-Time Token Streaming & Generation Controls**: Stream text token-by-token with instant **Stop Generating** cancellation support.
- 🎨 **Modern ChatGPT-Style UI**: Modern dark-mode UI with sleek message bubbles, thumbnail attachments, and real-time status indicators.
- 🧪 **Live SATE AI Stress Testing Suite**: Built-in benchmark suite executing memory pressure injection and synthetic query fault recovery.

---

## 🛠️ Tech Stack & Architecture

| Layer | Technology |
| :--- | :--- |
| **Frontend Framework** | [Flutter](https://flutter.dev) (Dart 3.x, Material 3) |
| **Inference Engine** | [`llamadart`](https://pub.dev/packages/llamadart) / `llama.cpp` C++ FFI |
| **Native Toolchain** | Android NDK 28 (`Clang 19`), CMake 3.22, Ninja Build System |
| **Vision Model** | `Qwen3-VL-2B-Instruct-Q4_K_M.gguf` + `mmproj-F16.gguf` |
| **Architecture** | `arm64-v8a` (Android 10+ / API 26+) |

---

## 📂 Model Setup Guide

To run the model on your Android device:

1. Download the model files from Hugging Face:
   - **Model GGUF**: `Qwen3VL-2B-Instruct-Q4_K_M.gguf`
   - **Vision Projector**: `mmproj-Qwen3VL-2B-Instruct-F16.gguf`
2. Push the `.gguf` files to your app's external storage directory on the device:
   ```bash
   adb push Qwen3VL-2B-Instruct-Q4_K_M.gguf /sdcard/Android/data/com.example.multimodal_demo/files/model.gguf
   adb push mmproj-Qwen3VL-2B-Instruct-F16.gguf /sdcard/Android/data/com.example.multimodal_demo/files/mmproj.gguf
   ```
3. Run the app in release mode:
   ```bash
   flutter run --release
   ```

---

## 📄 License

Licensed under the [MIT License](LICENSE).
