# FlaskTest

A minimal Flask web app showing suspicious IP activity.
^rewrite all this later


## Setup

1. Create and activate a virtual environment:
   - macOS / Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - Windows PowerShell:
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   python app.py
   ```

4. Open your browser at `http://127.0.0.1:5000/`.

## Files

- `app.py` - Flask application entrypoint
- `parser.py` - Firewall log parser helper
- `requirements.txt` - Python dependencies
- `templates/index.html` - HTML template for the Flask app
