"""Status blueprint: returns JSON system status."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import TypedDict

from flask import Blueprint, jsonify, current_app

from travel_agent import TravelAgent
from version import get_version_info, get_version_string, VERSION_FULL

bp = Blueprint("status", __name__)

# Singleton-ish agent instance reused across requests
_agent: TravelAgent | None = None


def _get_agent() -> TravelAgent:
    global _agent  # noqa: PLW0603
    if _agent is None:
        _agent = TravelAgent()
    return _agent


class _Status(TypedDict):
    system: str
    last_check: str
    active_briefs: int
    total_deals_found: int
    notifications_sent: int
    services: dict[str, bool]
    error: str | None


@bp.route("/api/status")
def get_status():  # type: ignore[return-value]
    """Return a snapshot of system status as JSON."""
    try:
        agent = _get_agent()
        status: _Status = {
            "system": "running",
            "last_check": agent.get_last_check_time(),
            "active_briefs": agent.get_active_briefs_count(),
            "total_deals_found": agent.get_total_deals_count(),
            "notifications_sent": agent.get_notifications_count(),
            "services": {
                "amadeus": agent.amadeus is not None,
                "openai": agent.ai_analyzer is not None,
                "telegram": agent.telegram is not None,
                "sheets": agent.sheets.client is not None,  # type: ignore[attr-defined]
            },
            "error": None,
        }
        return jsonify(status)
    except Exception as exc:  # noqa: BLE001
        logging.exception("Status check error: %s", exc)
        return (
            jsonify({
                "system": "error",
                "last_check": "Never",
                "active_briefs": 0,
                "total_deals_found": 0,
                "notifications_sent": 0,
                "services": {},
                "error": str(exc),
            }),
            200,
        )


@bp.route("/health")
def health_check():  # type: ignore[return-value]
    """Health check endpoint for AWS load balancer."""
    try:
        # Basic database connectivity check
        from ..models import db
        db.session.execute("SELECT 1")
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"
    
    return jsonify({
        "status": "healthy",
        "service": "TravelAiGent",
        "version": VERSION_FULL,
        "database": db_status,
        "timestamp": datetime.now().isoformat()
    }), 200


@bp.route("/api/version")
def get_version():  # type: ignore[return-value]
    """Get detailed version information."""
    version_info = get_version_info()
    version_info['timestamp'] = datetime.now().isoformat()
    version_info['environment'] = current_app.config.get('ENV', 'production')
    return jsonify(version_info), 200
