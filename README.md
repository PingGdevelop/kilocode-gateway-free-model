# Kilo Gateway - Free Models

[![Python](https://img.shields.io/badge/Python-3.14+-blue?style=flat&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00a859?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/PingGdevelop/kilocode-gateway-free-model?style=flat)](https://github.com/PingGdevelop/kilocode-gateway-free-model/stargazers)

Free AI models browser for Kilo.ai gateway with a pixel-style dark/yellow themed web interface.

![Title Preview](assets/title%20preview.png)

![Models Preview](assets/preview%20model.png)

## Features

- **Backend**: FastAPI server that fetches models from Kilo.ai API
- **Frontend**: Clean, pixel-style dark/yellow themed web interface
- **API Endpoints**:
  - `GET /` - Web interface
  - `GET /api/models` - All models from Kilo.ai
  - `GET /api/models/free` - Free models only

## Quick Start

```bash
# Install dependencies
pip install fastapi uvicorn httpx

# Run the server
python main.py
```

Open http://localhost:8000 in your browser.

## API Usage

```bash
# Get all free models
curl http://localhost:8000/api/models/free
```

## Project Structure

```
kilocode-gateway/
├── main.py          # FastAPI backend
├── static/
│   └── index.html   # Frontend interface
├── assets/
│   └── *.png        # Screenshots
├── README.md
├── LICENSE
└── .gitignore
```

## License

MIT License - see [LICENSE](LICENSE) for details.
