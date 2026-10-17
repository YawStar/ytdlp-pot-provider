# YawStar yt-dlp PO Token Provider

`ytdlp-pot-provider` is a custom, lightweight Proof of Origin (PO) Token provider and plugin for [yt-dlp](https://github.com/yt-dlp/yt-dlp) that integrates with a Go-based HTTP server to generate and supply PO Tokens seamlessly.This project was used to bypass the 'Sign in to confirm you're not a bot' message when invoking yt-dlp from an IP address flagged by YouTube. See [PO Token Guide](https://github.com/yt-dlp/yt-dlp/wiki/PO-Token-Guide) for more details.

> [!CAUTION]
> Providing a PO token does not guarantee bypassing 403 errors or bot checks, but it _may_ help your traffic seem more legitimate.

[![GitHub Release](https://img.shields.io/github/v/release/YawStar/ytdlp-pot-provider?style=for-the-badge)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

---

## Features

- **Cross-Platform Go Server**: High-performance HTTP server built with Go, compiled as standalone binaries for Windows, Linux, and macOS (`yawstar-pot-server`).
- **Seamless yt-dlp Integration**: Implements the official `yt-dlp` PO Token provider architecture supporting various client contexts.
- **Flexible Configuration**: Supports custom host and port configuration via command-line flags and extractor arguments.
- **Docker Support**: Containerized deployment ready with `Dockerfile` and `docker-compose.yml`.

---

## Project Structure

```text
ytdlp-pot-provider/
├── yt_dlp_plugins/                 # yt-dlp namespace package plugin
│   └── extractor/                  # yt-dlp extractor
│       ├── getpot_yawstar.py       # Main HTTP provider and utilities
│       └── getpot_yawstar_http.py  # Auxiliary client plugin
├── server/                         # Go HTTP server source code
│   ├── go.mod                      # Go module definition and dependencies
│   ├── handler.go                  # HTTP request handlers & API endpoints
│   └── main.go                     # Main entry point & server configuration
├── build.py                        # Cross-platform Python build script for binaries
├── setup.py                        # Python package setup script
├── Dockerfile                      # Container configuration
├── docker-compose.yml              # Docker compose configuration
├── LICENSE                         # MIT License
└── README.md

```

---

## Getting Started

### 1. Build the Go Server Binary

You can easily compile the Go server for your target operating system using the provided Python build script:

```bash
python build.py

```

This will generate standalone binaries (e.g., `yawstar-pot-server-windows-amd64.exe`) inside the `dist/` folder.

### 2. Running the Go Server

Run the compiled binary with optional host and port flags:


#### Default (127.0.0.1:8080)
```bash
yawstar-pot-server-windows-amd64.exe
```

#### Custom host and port
```bash
yawstar-pot-server-windows-amd64.exe --host 127.0.0.1 --port 9000
```

#### Docker Deployment

Alternatively, you can run the server using Docker Compose:

```bash
docker compose up --build -d
```

---

## Installation & Usage

1. Copy `getpot_yawstar.py` and `getpot_yawstar_http.py` into your `yt-dlp` plugin directory (e.g., `yt-dlp-plugins` folder).
2. Ensure the Go server is running locally on port `8080` (or your configured port).
3. Use `yt-dlp` as normal. If your server runs on a custom URL or port, pass it via extractor arguments:

```bash
yt-dlp --extractor-args "yawstar:http:base_url=http://127.0.0.1:8080" "VIDEO_URL"
```

---

## Server Administrative Endpoints

The Go server includes built-in endpoints for monitoring and management (secured for localhost access only):

* **Version Check**: `http://127.0.0.1:8080/version`
* **Shutdown Server**: `http://127.0.0.1:8080/shutdown`
* **Restart Server**: `http://127.0.0.1:8080/restart`
* **Get poToken**: `http://127.0.0.1:8080/get_pot`
* **Clear Cache**: `http://127.0.0.1:8080/clear_cache`
* **Server Health**: `http://127.0.0.1:8080/health`
* **Server Status**: `http://127.0.0.1:8080/status`

---
## Support the Developer

If you find this app useful, consider supporting its development:

- ⭐ Star this repository
- 🐛 Report bugs or suggest features via [Issues](../../issues)
- ❤️ [Donate](https://yawstardancebox.github.io/donate/)
---
## License

This project is open-source and available under the [MIT License](https://www.google.com/search?q=LICENSE).

---

<div align="center">

**[⬆ Back to Top](#-access-configurations)**

Made with 💚 by YawHackka

</div>