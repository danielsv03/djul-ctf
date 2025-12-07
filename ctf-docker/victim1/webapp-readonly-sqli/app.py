# app.py
from flask import Flask, request, g
import sqlite3
import os

DB_PATH = '/data/ctf_readonly.db'   # mounted DB path (read-only)

app = Flask(__name__)

def get_db():
    if 'db' not in g:
        # open read-only (URI mode) to emphasize no writes allowed
        g.db = sqlite3.connect(f'file:{DB_PATH}?mode=ro', uri=True, check_same_thread=False)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return """<html><body>
    <h2>Victim1: Product search</h2>
    <form action="/search">
      Search product: <input name="q" />
      <input type="submit" value="Search" />
    </form>
    <p>Hint: try single quotes in the search box.</p>
    </body></html>"""

@app.route('/search')
def search():
    q = request.args.get('q','').strip()

    # Prevent empty searches from returning EVERYTHING
    if not q:
        return "<p>Please enter a search term.</p>", 200

    db = get_db()

    # Intentional SQL injection (still works)
    sql = f"SELECT id, name, description FROM products WHERE name LIKE '%{q}%' LIMIT 50;"

    try:
        cur = db.execute(sql)
        rows = cur.fetchall()
        if not rows:
            return f"<p>No results for <b>{q}</b></p>", 200
        out = "<h3>Results</h3><ul>"
        for r in rows:
            out += f"<li><b>{r['name']}</b>: {r['description']}</li>"
        out += "</ul>"
        return out, 200
    except Exception as e:
        return f"<pre>Database error: {e}</pre>", 200

# Extra helper endpoint for debugging (internal use only)
@app.route('/info')
def info():
    return {"service":"victim1-web-sqli","note":"internal-only"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)