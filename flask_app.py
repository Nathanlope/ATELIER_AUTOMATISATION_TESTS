from flask import Flask, render_template, jsonify
from tester.runner import run_all
from tester import storage

app = Flask(__name__)
storage.init_db()


@app.get("/")
def consignes():
    return render_template('consignes.html', active="home")


@app.get("/run")
def run():
    result = run_all()
    storage.save_run(result)
    return jsonify(result)


@app.get("/dashboard")
def dashboard():
    runs = storage.list_runs(limit=20)
    last_run = runs[0] if runs else None
    return render_template("dashboard.html", runs=runs, last_run=last_run, active="dashboard")


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
