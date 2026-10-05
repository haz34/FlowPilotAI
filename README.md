# FlowPilot AI

FlowPilot AI is a prototype for goal-based automation. A user describes an outcome in natural language, and the system converts it into an actionable workflow, tracks progress, and can adapt the plan when constraints change.

## Prototype flow

User Goal -> Intent Understanding -> Task Planning -> Execution/Tracking -> Adaptation

## Run locally

1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Create a virtual environment:
   - Windows: `python -m venv venv`
4. Activate it:
   - PowerShell: `venv\Scripts\Activate.ps1`
5. Install Flask:
   - `pip install flask`
6. Run:
   - `python app.py`
7. Open `http://127.0.0.1:5000`

## Important

This is a hackathon prototype. The current version uses a lightweight local planning layer so it works without API keys. For the final Amazon hackathon build, the planning/execution layer should be connected to the actual Amazon/AWS services and agent tooling that the team implements.
