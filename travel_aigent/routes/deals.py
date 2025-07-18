"""Deals-specific endpoints (placeholder for future expansion)."""
from __future__ import annotations

from flask import Blueprint, jsonify

bp = Blueprint("deals", __name__)


@bp.route("/api/deals/recent")
def recent_deals():  # type: ignore[return-value]
    """Temporary stub endpoint until richer functionality is added."""
    return jsonify([])
