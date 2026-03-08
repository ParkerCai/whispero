# WhisperO 😮

**Just speak.**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](pyproject.toml)
[![Backend](https://img.shields.io/badge/Backend-faster--whisper%20%7C%20whisper.cpp-orange.svg)](https://github.com/SYSTRAN/faster-whisper)

WhisperO is a push-to-talk desktop dictation app.
Hold the hotkey, speak, release, and text is pasted at your cursor.

Local mode is the default. No server is required.
On first run, WhisperO downloads a speech model to `~/.whispero/models/`.
`large-v3` is the default model and is about 3 GB.

## Demo

![Dictation demo](assets/demo.gif)

![Tray menu and custom dictionary](assets/tray.gif)

## Features

- Cross-platform: macOS, Windows, Linux
- Local transcription with faster-whisper (default)
- Optional remote whisper.cpp server backend
- Hold-to-record hotkey (`Win`+`Ctrl` on Windows, `⌘`+`Ctrl` on Mac)
- Auto-paste at cursor without losing clipboard contents
- Custom dictionary for names and project terms
- Start/stop sound feedback
- System tray app with quick controls

## Quick Start (Local Default)

1. **Install**
   ```bash
   git clone https://github.com/parkercai/whispero.git
   cd whispero
   pip install .
   ```

2. **Run**
   ```bash
   whispero
   ```
   or
   ```bash
   python -m whispero
   ```

That is it. WhisperO starts in local mode and uses model `large-v3`.

3. **Run in background without terminal window (optional)**

   **Windows:**
   ```bash
   pythonw -m whispero
   ```

   To start automatically on login, double-click `scripts\install-startup.bat`.
   To remove: `scripts\uninstall-startup.bat`.

   **macOS:**
   ```bash
   nohup python -m whispero &>/dev/null &
   ```

   For login startup, add WhisperO to System Settings → General → Login Items.

## Advanced: Remote Server

If you want to run transcription on another machine, set server backend:

```bash
export WHISPERO_BACKEND=server
export WHISPERO_SERVER="http://localhost:8080"
```

Server setup guide: [docs/SERVER_SETUP.md](docs/SERVER_SETUP.md)

## Configuration

Config priority:

1. Environment variables
2. `~/.whispero/config.json`
3. Built-in defaults

Supported environment variables:

- `WHISPERO_BACKEND=local|server`
- `WHISPERO_MODEL=large-v3|medium|small|base|tiny`
- `WHISPERO_SERVER=http://host:8080`

Default values:

```json
{
  "backend": "local",
  "server": "http://localhost:8080",
  "model": "large-v3",
  "hotkey": {
    "windows": ["win", "ctrl"],
    "mac": ["cmd", "ctrl"]
  },
  "sounds": true
}
```

Example `~/.whispero/config.json`:

```json
{
  "backend": "local",
  "model": "medium",
  "server": "http://localhost:8080",
  "hotkey": {
    "windows": ["win", "ctrl"],
    "mac": ["cmd", "ctrl"]
  },
  "sounds": true
}
```

Dictionary file location:

- `~/.whispero/dictionary.txt`

## How It Works

### Local mode (default)

```text
hold hotkey
   ↓
record mic audio
   ↓
transcribe with local faster-whisper model
   ↓
receive text
   ↓
paste at cursor
   ↓
restore original clipboard
```

### Server mode (optional)

```text
hold hotkey
   ↓
record mic audio
   ↓
send WAV to whisper.cpp /inference
   ↓
receive text
   ↓
paste at cursor
   ↓
restore original clipboard
```

## Benchmarks

Transcription speed for a 5-second audio clip using `large-v3`. Times exclude model loading (warm GPU).

| Hardware | Backend | Median | Avg |
|---|---|---|---|
| RTX 5090 | faster-whisper (local) | 378ms | 390ms |
| NVIDIA GB10 (DGX Spark) | whisper.cpp (server) | 323ms | 375ms |

Run your own benchmark:

```bash
python benchmark.py                    # local mode
python benchmark.py --backend server   # server mode
```

Run the benchmark a few times. The first run warms up GPU memory, so later runs are more accurate.

Got a result? PRs with new hardware numbers are welcome.

## Building Standalone Apps

WhisperO includes a PyInstaller build script.

```bash
pip install -r requirements.txt
python build/build.py
```

Output:

- macOS: `dist/WhisperO.app`
- Windows: `dist/WhisperO/WhisperO.exe`

## Contributing

PRs are welcome.
Keep behavior stable across both backends.
Please test on your target OS before opening a PR.

## License

MIT. See [LICENSE](LICENSE).
