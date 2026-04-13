# Kilo Gateway - Free Models

> Minimalist proxy gateway for browsing free AI models available on Kilo.ai API

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/PingGdevelop/kilocode-gateway-free-model?style=flat-square)](https://github.com/PingGdevelop/kilocode-gateway-free-model/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/PingGdevelop/kilocode-gateway-free-model?style=flat-square)](https://github.com/PingGdevelop/kilocode-gateway-free-model/commits/main)

---

## ✨ Features

- **FastAPI Backend** with proper async / await support
- **Automatic caching** of upstream API responses (60s TTL)
- Clean, minimalist paper-style web interface
- Filter only free models from the Kilo.ai catalog
- Structured logging and proper error handling
- Standard `/health` endpoint for monitoring
- OpenAPI documentation automatically available at `/docs`
- Zero client-side dependencies

---

## 🚀 Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/PingGdevelop/kilocode-gateway-free-model.git
cd kilocode-gateway-free-model

# Install dependencies
pip install fastapi uvicorn httpx aiofiles

# Run the server
python main.py

# Optional: specify custom port
python main.py --port 3000
```

Then open http://localhost:8000 in your browser.

---

## 📡 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Web interface |
| `GET /api/models` | Full unfiltered list of all models from Kilo.ai |
| `GET /api/models/free` | Only free models, cleaned and formatted |
| `GET /health` | Service health check |
| `GET /docs` | Automatic OpenAPI documentation |
| `GET /redoc` | Alternative API documentation |

### Example usage
```bash
# Get all free models
curl -s http://localhost:8000/api/models/free | jq
```

---

## 📋 Project Structure

```
kilocode-gateway-free-model/
├── main.py                 # FastAPI application
├── static/
│   └── index.html          # Minimalist web interface
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🔧 Configuration

All configuration constants are defined at the top of `main.py`:

```python
KILO_API_URL = "https://api.kilo.ai/api/gateway/models"
REQUEST_TIMEOUT = 10    # Upstream request timeout in seconds
CACHE_TTL = 60          # Cache duration in seconds
```

---

## 🛡️ Production deployment

For production usage:
- Use a proper ASGI server like `gunicorn`
- Restrict CORS origins instead of `*`
- Add rate limiting
- Place behind a reverse proxy (nginx / caddy)
- Set proper log levels

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.
