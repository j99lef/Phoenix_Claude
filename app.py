"""Legacy entry point retained for backward compatibility.

Prefer running `python cli.py web` or `python -m travel_aigent`.
This thin wrapper delegates to the new application factory."""
from __future__ import annotations
import os

from travel_aigent import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)

