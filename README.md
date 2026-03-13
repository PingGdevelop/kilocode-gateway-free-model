# Kilo Gateway - Free Models

A simple backend API and web interface to browse free AI models available through Kilo.ai's gateway.

## Features

- **Backend**: FastAPI server that fetches models from Kilo.ai API
- **Frontend**: Clean, pixel-style dark/yellow themed web interface
- **API Endpoints**:
  - `GET /` - Web interface
  - `GET /api/models` - All models from Kilo.ai
  - `GET /api/models/free` - Free models only

## Installation

```bash
# Install dependencies
pip install fastapi uvicorn httpx

# Run the server
python main.py
```

The server will start at http://localhost:8000

## Project Structure

```
kilocode-gateway/
├── main.py          # FastAPI backend
├── static/
│   └── index.html   # Frontend interface
└── README.md
```

## License

MIT License
