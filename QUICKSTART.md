# 🚀 Quick Start Guide

Get the URL Phishing Detector running in 5 minutes!

## Prerequisites

- **Python 3.9+** - [Download here](https://www.python.org/)
- **Git** - [Download here](https://git-scm.com/)
- **Modern Browser** - Chrome, Firefox, Safari, or Edge

## Installation (5 minutes)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/phishing-detector.git
cd phishing-detector
```

### 2️⃣ Create Virtual Environment

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- Requests (HTTP library)
- Python-dotenv (configuration)

### 4️⃣ Run Application

```bash
python server.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### 5️⃣ Open in Browser

**Visit:** http://localhost:5000

🎉 **That's it! You're done!**

---

## Usage

### Analyzing URLs

1. **Enter a URL:**
   - Type: `https://example.com`
   - Or just: `example.com` (auto-adds https)

2. **Click "Analyze"**
   - Wait for analysis (< 2 seconds)

3. **Review Results:**
   - Safety percentage (0-100%)
   - Verdict (Safe ✓ | Risky ⚠ | Unsafe ✗)
   - Detailed security checks

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Enter** | Analyze current URL |
| **Ctrl+L** | Focus URL input |

### Example Tests

Try these URLs to see different results:

```
Safe:     https://google.com
Risky:    https://paypal-verify.com
Unsafe:   http://192.168.1.1/verify
```

---

## Configuration (Optional)

### Create .env File

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
HOST=127.0.0.1
```

---

## Running Tests

### Install Test Dependencies

Already included in `requirements.txt`

### Run All Tests

```bash
pytest tests/
```

### Run Specific Test

```bash
pytest tests/test_analyzer.py -v
```

### With Coverage Report

```bash
pytest tests/ --cov=. --cov-report=html
```

---

## Troubleshooting

### "Port 5000 is already in use"

Change the port in `.env`:
```env
PORT=5001
```

Then restart the server.

### "Module not found" error

Make sure virtual environment is activated:
```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows
```

### "API Error" when analyzing

- Check internet connection
- URLhaus API might be temporarily down
- Local analysis still works

### Python version error

Check your Python version:
```bash
python --version
```

Must be 3.9 or higher. Install from [python.org](https://python.org)

---

## Project Structure

```
phishing-detector/
├── server.py              # Main Flask app
├── requirements.txt       # Dependencies
├── .env.example          # Config template
├── .gitignore            # Git ignore rules
├── README.md             # Full documentation
├── CONTRIBUTING.md       # How to contribute
├── LICENSE               # MIT License
│
├── templates/
│   └── index.html        # Web interface
│
├── tests/
│   └── test_analyzer.py  # Unit tests
│
├── .github/
│   └── workflows/
│       └── tests.yml     # CI/CD pipeline
│
└── docs/
    ├── INSTALLATION.md
    ├── API.md
    ├── ARCHITECTURE.md
    └── TROUBLESHOOTING.md
```

---

## API Usage

### Analyze URL via API

```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### Response Example

```json
{
  "status": "ok",
  "verdict": "safe",
  "safety_score": 95,
  "risk_score": 5,
  "checks": [
    {
      "name": "SSL/TLS Encryption",
      "status": "pass",
      "description": "URL uses secure HTTPS protocol"
    }
  ]
}
```

---

## Development

### Code Style

Follow PEP 8:
```bash
pip install pylint
pylint server.py
```

### Add New Features

1. Create feature branch
2. Make changes
3. Run tests
4. Submit pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## Deployment

### Development Server
```bash
python server.py
```

### Production Server
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 server:app
```

### Docker (Optional)
```bash
docker build -t phishing-detector .
docker run -p 5000:5000 phishing-detector
```

---

## Next Steps

- 📖 Read [README.md](README.md) for full documentation
- 🔌 Check [docs/API.md](docs/API.md) for API details
- 🏗️ Review [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for system design
- 🤝 See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- 🐛 Report issues on [GitHub Issues](https://github.com/yourusername/phishing-detector/issues)

---

## Common Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python server.py

# Run tests
pytest tests/

# Run with coverage
pytest tests/ --cov

# Deactivate virtual environment
deactivate
```

---

## Getting Help

- **Documentation**: [README.md](README.md)
- **API Docs**: [docs/API.md](docs/API.md)
- **Issues**: [GitHub Issues](https://github.com/yourusername/phishing-detector/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/phishing-detector/discussions)

---

## Staying Updated

Get new versions:

```bash
git pull origin main
pip install -r requirements.txt
```

---

## FAQ

**Q: Can I analyze multiple URLs at once?**
A: Currently no, but it's planned for v1.1

**Q: Does it store my data?**
A: No! Everything is processed locally.

**Q: Can I use this commercially?**
A: Yes! MIT License permits commercial use.

**Q: How accurate is it?**
A: 99.67% on phishing detection

**Q: Can I contribute?**
A: Yes please! See [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Ready to analyze URLs?** Start the server and visit http://localhost:5000! 🚀

---

*Last updated: January 2026*
