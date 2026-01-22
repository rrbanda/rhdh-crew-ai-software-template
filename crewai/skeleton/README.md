# 🐆 Leopard Pont des Arts - CrewAI Multi-Agent System

A **CrewAI multi-agent application** that calculates how fast a leopard can cross the Pont des Arts bridge in Paris.

This application demonstrates CrewAI best practices:
- ✅ **Multi-Agent Collaboration** – Researcher and Calculator agents work together
- ✅ **Real Tool Usage** – DuckDuckGo search integrated as a CrewAI tool
- ✅ **Task Context Chain** – Calculator receives context from Researcher's findings
- ✅ **LlamaStack Integration** – Uses OpenAI-compatible LlamaStack API
- ✅ **Configurable via YAML** – Agents and tasks defined in config files

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CrewAI Crew                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐         ┌─────────────────┐           │
│  │   Researcher    │────────▶│   Calculator    │           │
│  │     Agent       │ context │     Agent       │           │
│  └────────┬────────┘         └────────┬────────┘           │
│           │                           │                     │
│           ▼                           ▼                     │
│  ┌─────────────────┐         ┌─────────────────┐           │
│  │  Research Task  │         │ Calculation Task│           │
│  │                 │         │                 │           │
│  │ • Leopard speed │         │ • Convert units │           │
│  │ • Bridge length │         │ • Apply formula │           │
│  └────────┬────────┘         │ • Return JSON   │           │
│           │                  └─────────────────┘           │
│           ▼                                                 │
│  ┌─────────────────┐                                       │
│  │  DuckDuckGo     │                                       │
│  │  Search Tool    │                                       │
│  └─────────────────┘                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                 ┌─────────────────┐
                 │   LlamaStack    │
                 │   (LLM API)     │
                 └─────────────────┘
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file:

```bash
# LlamaStack Configuration
LLAMASTACK_BASE_URL=https://lss-lss.apps.cluster-nngf2.dynamic.redhatworkshops.io/v1
LLAMASTACK_MODEL=remote-llm/llama-4-scout-17b-16e-w4a16
LLAMASTACK_API_KEY=

# Logging
LOG_LEVEL=INFO
```

### 3. Run the Application

**Option A: API Server**
```bash
python app.py
# or
uvicorn src.api:app --reload --port 8000
```

**Option B: CLI Mode**
```bash
python -m src.cli
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info and available endpoints |
| GET | `/health` | Health check with LLM config info |
| GET | `/models` | List available LlamaStack models |
| GET | `/leopard-crossing` | Run the full crew calculation |
| GET | `/leopard-crossing/simple` | Get simplified result |

### Example Request

```bash
curl http://localhost:8000/leopard-crossing
```

### Example Response

```json
{
  "leopard_speed_kmh": 58,
  "leopard_speed_ms": 16.11,
  "bridge_length_meters": 155,
  "crossing_time_seconds": 9.62,
  "calculation": "155m ÷ 16.11 m/s = 9.62 seconds",
  "explanation": "A leopard running at its maximum speed of 58 km/h would cross the 155-meter Pont des Arts bridge in approximately 9.62 seconds."
}
```

---

## 📁 Project Structure

```
skeleton/
├── app.py                    # Application entry point
├── requirements.txt          # Python dependencies
├── Containerfile             # Container build file
├── configs/
│   ├── agents.yaml           # Agent role/goal/backstory definitions
│   ├── tasks.yaml            # Task descriptions and expected outputs
│   └── config.yaml           # Application configuration
└── src/
    ├── api.py                # FastAPI application
    ├── cli.py                # CLI runner
    ├── llm.py                # LlamaStack LLM configuration
    ├── agents.py             # CrewAI agent definitions
    └── tasks.py              # CrewAI task definitions
```

---

## ⚙️ Configuration

### Agents (`configs/agents.yaml`)

Define agent personas:

```yaml
researcher:
  role: Wildlife & Geography Researcher
  goal: Find accurate factual information about animals and landmarks
  backstory: |
    You are an expert researcher specializing in wildlife biology...

calculator:
  role: Physics Calculator
  goal: Calculate precise time measurements using physics formulas
  backstory: |
    You are a physicist who specializes in motion calculations...
```

### Tasks (`configs/tasks.yaml`)

Define what agents should do:

```yaml
research_task:
  description: |
    Research and find the following factual information:
    1. What is the maximum running speed of a leopard in km/h?
    2. What is the length of the Pont des Arts bridge in Paris?
  expected_output: |
    A clear report with leopard speed and bridge length...

calculation_task:
  description: |
    Using the research data, calculate crossing time...
  expected_output: |
    A JSON response with crossing_time_seconds...
```

---

## 🐳 Container Deployment

### Build

```bash
podman build -t leopard-pontdesarts:latest .
```

### Run

```bash
podman run -p 8000:8000 \
  -e LLAMASTACK_BASE_URL="https://your-llamastack-url/v1" \
  -e LLAMASTACK_MODEL="remote-llm/llama-4-scout-17b-16e-w4a16" \
  leopard-pontdesarts:latest
```

---

## 🔧 Available LlamaStack Models

Query available models:

```bash
curl http://localhost:8000/models
```

Or directly from LlamaStack:

```bash
curl https://lss-lss.apps.cluster-nngf2.dynamic.redhatworkshops.io/v1/models
```

Common models:
- `remote-llm/llama-4-scout-17b-16e-w4a16` - Llama 4 Scout
- `gemini-llm/gemini-2.5-flash` - Gemini 2.5 Flash
- `gemini-llm/models/gemini-2.0-flash` - Gemini 2.0 Flash

---

## 📚 Learn More

- [CrewAI Documentation](https://docs.crewai.com/)
- [LlamaStack](https://github.com/meta-llama/llama-stack)
- [FastAPI](https://fastapi.tiangolo.com/)
