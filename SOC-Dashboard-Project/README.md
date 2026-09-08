# SOC Dashboard Project

A Python Flask web application that ingests pfSense firewall logs, 
stores them in SQLite, and visualizes network traffic and suspicious 
IP activity on a SOC-style dashboard. Integrates AbuseIPDB API for 
IP reputation lookups.

## Network Infrastructure
- pfSense firewall (bare metal) with router-on-a-stick architecture
- TP-Link TL-SG108PE managed switch with 802.1Q VLAN segmentation
- VLANs: Management (10), Main LAN (20), IoT (30), WAN (40)
- Project taken offline following APT28 TP-Link exploitation campaign

## Setup

1. Create and activate a virtual environment:
   * macOS / Linux:

python3 -m venv .venv
source .venv/bin/activate

   * Windows PowerShell:

python -m venv .venv
..venv\Scripts\Activate.ps1


2. Install dependencies:

pip install -r requirements.txt


3. Run the log parser first to populate the database:

python log_parser.py


4. Start the Flask app:

python app.py


5. Open your browser at `http://127.0.0.1:5000/`

## Files
- `app.py` — Flask application, queries SQLite and renders dashboard
- `log_parser.py` — Parses pfSense filterlog format, writes to SQLite
- `templates/dashboard.html` — SOC dashboard template
- `requirements.txt` — Python dependencies
- `firewall.log` — Sample log file for testing

## Status
Network infrastructure currently offline. Flask dashboard and SQLite 
integration complete. AbuseIPDB API integration in progress.
