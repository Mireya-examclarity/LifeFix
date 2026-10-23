# LifeFix ✨ - Python Flask backend for NASA Stardance
# Main idea: Turn daily annoyances into simple digital solutions
# Detailed vision > just todo list

from flask import Flask, render_template, request, jsonify
from datetime import datetime
import math

app = Flask(__name__)

# Same scoring logic 

def get_score(deadline_str, importance, hours):
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    try:
        dd = datetime.strptime(deadline_str, "%Y-%m-%d")
    except:
        dd = today
    days = (dd - today).days
    
    if days <= 0: s1 = 100
    elif days == 1: s1 = 90
    elif days <= 3: s1 = 75
    elif days <= 7: s1 = 55
    elif days <= 14: s1 = 35
    else: s1 = 15

    if "Low" in importance: s2 = 20
    elif "Medium" in importance: s2 = 50
    else: s2 = 100

    s3 = hours * 8
    if s3 > 80: s3 = 80

    return round((s1*0.5 + s2*0.35 + s3*0.15), 1)


def get_detailed_vision(deadline_str, importance, hours):
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    try:
        dd = datetime.strptime(deadline_str, "%Y-%m-%d")
    except:
        dd = today
    days = (dd - today).days
    
    if days <= 0:
        return f"OVERDUE by {abs(days)} days 😭 Do TODAY no excuse!"
    if days == 1:
        return "Tomorrow deadline! #1 priority 🌟"
    if "High" in importance and days <= 3:
        return f"High 🔥 + only {days} days! Focus now!!"
    if hours > 4:
        return f"Takes {hours}h - split it, 2h today 🍰"
    return "Quick win! Do now and feel happy ✨"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/score", methods=["POST"])
def score_api():
    data = request.json
    deadline = data.get("deadline", "")
    importance = data.get("importance", "Medium")
    hours = float(data.get("hours", 1))
    
    score = get_score(deadline, importance, hours)
    vision = get_detailed_vision(deadline, importance, hours)
    
    return jsonify({

        "score": score,
        "vision": vision,
        "message": "LifeFix detailed vision generated"})
    

@app.route("/api/split", methods=["POST"])
def split_api():
    data = request.json
    total = float(data.get("total", 0))
    people = int(data.get("people", 1))
    if people == 0: people = 1
    return jsonify({"each": round(total/people, 2)})

if __name__ == "__main__":
    print("LifeFix running ✨ http://127.0.0.1:5000")
    app.run(debug=True)
    

