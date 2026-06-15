# Contributing to Parallax

Thank you for your interest in contributing to **Parallax — AI Co-Pilots That See Work From Every Angle**.

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Git

### Setup

```bash
# Clone the repo
git clone https://github.com/FrozenLionMax/Parallax.git
cd Parallax

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run the demo
python main.py

# Run the API
uvicorn src.api:app --reload

# Run the prototype
streamlit run prototype/app.py
```

## 📁 Project Structure

```
Parallax/
├── src/                    # Core source code
│   ├── config.py           # Co-pilot registry & configuration
│   ├── models.py           # Data models (Task, DAG, Message)
│   ├── memory.py           # 3-layer memory system
│   ├── message_bus.py      # Inter-co-pilot communication
│   ├── orchestrator.py     # Central brain
│   ├── api.py              # FastAPI backend
│   └── copilots/           # All 11 co-pilot implementations
│       ├── base.py         # Abstract base class
│       ├── agents.py       # Core 10 co-pilots
│       └── catalyst.py     # 11th Accelerator co-pilot
├── tests/                  # Test suite
├── prototype/              # Streamlit interactive demo
├── pitch-deck/             # HTML pitch deck
├── docs/                   # Documentation
└── assets/                 # Visual assets
```

## 🔧 How to Add a New Co-Pilot

Parallax is designed for extensibility. To add a new co-pilot:

### 1. Register in Config
Add your co-pilot to `COPILOT_REGISTRY` in `src/config.py`:
```python
"your_copilot": {
    "name": "Your Co-Pilot",
    "codename": "The Nickname",
    "icon": "🆕",
    "color": "#HEX",
    "description": "What it does.",
    "capabilities": ["cap1", "cap2", "cap3"],
},
```

### 2. Implement the Class
Create `src/copilots/your_copilot.py`:
```python
from src.copilots.base import BaseCoPilot

class YourCoPilot(BaseCoPilot):
    def __init__(self, memory, bus):
        super().__init__("your_copilot", memory, bus)

    def process(self, task):
        # Your logic here
        task.complete(result, confidence=0.90)
        return {"output": result, "confidence": 0.90, ...}
```

### 3. Register in Orchestrator
Add to `src/orchestrator.py`:
```python
from src.copilots.your_copilot import YourCoPilot
# In __init__:
"your_copilot": YourCoPilot(self.memory, self.bus),
```

### 4. Write Tests
Add tests in `tests/test_system.py`.

### 5. Run Tests
```bash
pytest tests/ -v
```

## 📝 Code Style

- Python 3.12+ with type hints
- Docstrings on all public methods
- Clear, descriptive variable names
- 100-char line limit

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src

# Run specific test class
pytest tests/test_system.py::TestOrchestrator -v
```

## 📜 License

MIT — see [LICENSE](LICENSE).
