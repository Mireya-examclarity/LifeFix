from flask import Flask, render_template, request, redirect, url_for
from datetime import date, datetime

app = Flask(__name__)
tasks = []

def get_score(task):
    
    today = date.today()

    days = (task['deadline'] - today).days

    if days <= 0: s1 = 100

    elif days == 1: s1 = 90

    elif days <= 3: s1 = 75

    elif days <= 7: s1 = 55

    elif days <= 14: s1 = 35

    else: s1 = 15

    if task['importance'] == "Low": s2 = 20

    elif task['importance'] == "Medium": s2 = 50

    else: s2 = 100

    s3 = task['hours'] * 8

    if s3 > 80: s3 = 80

    final = s1*0.5 + s2*0.35 + s3*0.15

    return round(final,1)

# this is the LifeFix part - detailed vision

def get_detailed_vision(task):

    today = date.today()

    days = (task['deadline'] - today).days

    if days <= 0:

        return f"OVERDUE by {abs(days)} days. If you ignore this it will cause more stress. Do this TODAY, no excuse."
    
    if days == 1:
        return "Deadline is tomorrow. This is your #1 priority. Finish it today and tomorrow will be free."
    
    if task['importance'] == "High" and days <= 3:

        return f"High importance and only {days} days left. This is what you should focus on more than anything else."
    
    if task['hours'] > 4:

        return f"This will take {task['hours']} hours. Don't do it at last minute, split it - do 2 hours today."
    
    return "This is a quick task. Do it now to get a small win and feel motivated."

@app.route("/", methods=["GET", "POST"])

def home():
    if request.method == "POST":

        name = request.form.get("name")

        date_str = request.form.get("deadline")

        hrs = request.form.get("hours")

        imp = request.form.get("importance")

        if name and date_str:
            try:
                d = datetime.strptime(date_str, "%Y-%m-%d").date()

                tasks.append({"name": name, "deadline": d, "hours": float(hrs), "importance": imp, "completed": False})
            except:

                pass

        return redirect(url_for("home"))

    sorted_tasks = sorted(tasks, key=get_score, reverse=True)

    total = len(tasks)

    done = sum(1 for t in tasks if t['completed'])


    # LifeFix focus logic - what to do now with vision

    focus_task = None

    focus_vision = None

    for t in sorted_tasks:

        if not t['completed']:

            focus_task = t

            focus_vision = get_detailed_vision(t)

            break

    return render_template("index.html", tasks=sorted_tasks, total=total, done=done,
                           score_func=get_score, focus_task=focus_task, focus_vision=focus_vision)

@app.route("/done/<int:num>")

def done(num):

    sorted_tasks = sorted(tasks, key=get_score, reverse=True)

    if num < len(sorted_tasks):

        sorted_tasks[num]["completed"] = not sorted_tasks[num]["completed"]

    return redirect(url_for("home"))

@app.route("/clear")

def clear():

    tasks.clear()

    return redirect(url_for("home"))

if __name__ == "__main__":

    app.run(debug=True)