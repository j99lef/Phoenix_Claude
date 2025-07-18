"""Command-line entry points for Travel AiGent.

Run `python cli.py web` to launch the web UI, or `python cli.py scheduler` to
kick off the periodic search loop. In production these would be wired to
separate container entry-points (web vs. worker).
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import NoReturn

import click

# Ensure project root is on path when running directly ----------------------------------
ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT))

from travel_aigent import create_app  # noqa: E402  pylint: disable=wrong-import-position
from travel_agent import TravelAgent  # noqa: E402  pylint: disable=wrong-import-position

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")


@click.group()
def cli() -> None:
    """Travel AiGent CLI."""


@cli.command()
@click.option("--host", default="0.0.0.0", help="Bind address.")
@click.option("--port", default=5000, help="Bind port.")
@click.option("--debug/--no-debug", default=False, help="Enable Flask debug mode.")
def web(host: str, port: int, debug: bool) -> None:  # noqa: D401
    """Start the Flask web server."""
    app = create_app()
    app.run(host=host, port=port, debug=debug)


@cli.command()
@click.option("--loop", default=False, is_flag=True, help="Run deal search loop forever.")
def scheduler(loop: bool) -> None:  # noqa: D401
    """Run the deal-search scheduler once or continuously."""
    agent = TravelAgent()
    if loop:
        import schedule, time  # local import to avoid startup cost if unused

        schedule.every().hours.at(":00").do(agent.run_deal_search)
        logging.info("Scheduler started; press Ctrl-C to exit.")
        while True:  # noqa: PLW0127
            schedule.run_pending()
            time.sleep(30)
    else:
        agent.run_deal_search()


def _main() -> NoReturn:  # pragma: no cover
    cli(main_module="cli")
    sys.exit(0)


if __name__ == "__main__":  # pragma: no cover
    _main()
