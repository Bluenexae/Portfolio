import sqlite3
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def home():
    con = sqlite3.connect("soc_dashboard.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("""
    SELECT * FROM firewall_logs
    """)
    db_logs = cur.fetchall()
    total_events = cur.execute ("SELECT COUNT(*) FROM firewall_logs")
    total_events = cur.fetchone()[0]
    total_blocked = cur.execute ("SELECT COUNT(*) FROM firewall_logs WHERE action = 'block'")
    total_blocked = cur.fetchone()[0]
    total_passed = cur.execute ("SELECT COUNT(*) FROM firewall_logs WHERE action = 'pass'")
    total_passed = cur.fetchone()[0]
    unique_ips = cur.execute ("SELECT COUNT(DISTINCT src_ip) FROM firewall_logs")
    unique_ips = cur.fetchone()[0]
    con.close()
    return render_template("dashboard.html", 
        logs=db_logs,
         total_events=total_events,
        total_blocked=total_blocked,
        total_passed=total_passed,
        unique_ips=unique_ips
        )



@app.route("/log/<int:id>")
def log_detail(id):
    con = sqlite3.connect("soc_dashboard.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM firewall_logs WHERE id = ?", (id,))
    db_logs = cur.fetchone()
    con.close()
    return render_template("dashboard.html", logs=db_logs)
    

if __name__ == "__main__":
    app.run(debug=True) 
