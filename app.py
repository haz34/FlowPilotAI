from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

def build_workflow(goal):
    goal_l = goal.lower()
    tasks = []

    if "hackathon" in goal_l:
        tasks = [
            ("Understand the hackathon requirements", "Research", "high"),
            ("Define the project idea and scope", "Planning", "high"),
            ("Create the technical architecture", "Development", "high"),
            ("Build the minimum working prototype", "Development", "high"),
            ("Prepare the demo and presentation", "Presentation", "medium"),
            ("Run a final submission checklist", "Review", "medium"),
        ]
    elif "interview" in goal_l:
        tasks = [
            ("Review company and role requirements", "Research", "high"),
            ("Prepare technical questions", "Preparation", "high"),
            ("Practice aptitude and coding", "Practice", "high"),
            ("Prepare a 60-second introduction", "Communication", "medium"),
            ("Run a mock interview", "Practice", "medium"),
        ]
    elif "exam" in goal_l or "study" in goal_l:
        tasks = [
            ("List the topics and exam requirements", "Planning", "high"),
            ("Prioritize the most important topics", "Planning", "high"),
            ("Create a focused study schedule", "Scheduling", "high"),
            ("Complete practice questions", "Practice", "medium"),
            ("Run a final revision", "Review", "medium"),
        ]
    else:
        tasks = [
            ("Understand the goal and requirements", "Planning", "high"),
            ("Break the goal into actionable steps", "Planning", "high"),
            ("Complete the highest-priority task", "Execution", "high"),
            ("Complete the remaining tasks", "Execution", "medium"),
            ("Review the result and identify next steps", "Review", "medium"),
        ]

    return [
        {"id": i+1, "title": t[0], "category": t[1], "priority": t[2], "status": "pending"}
        for i, t in enumerate(tasks)
    ]

@app.route("/")
def index():
    return render_template("index.html")

@app.post("/api/plan")
def plan():
    data = request.get_json(silent=True) or {}
    goal = (data.get("goal") or "").strip()
    if not goal:
        return jsonify({"error": "Please enter a goal."}), 400
    tasks = build_workflow(goal)
    return jsonify({
        "goal": goal,
        "tasks": tasks,
        "message": "FlowPilot created an adaptive workflow from your goal."
    })

@app.post("/api/task/<int:task_id>/complete")
def complete(task_id):
    return jsonify({"id": task_id, "status": "completed"})

@app.post("/api/replan")
def replan():
    data = request.get_json(silent=True) or {}
    goal = (data.get("goal") or "").strip()
    constraint = (data.get("constraint") or "").strip().lower()
    tasks = build_workflow(goal)
    if "30" in constraint or "short" in constraint or "limited" in constraint:
        tasks = [t for t in tasks if t["priority"] == "high"][:3]
        for t in tasks:
            t["priority"] = "critical"
    return jsonify({
        "tasks": tasks,
        "message": "FlowPilot adapted the workflow to the new constraint."
    })

if __name__ == "__main__":
    app.run(debug=True)
