#!/usr/bin/env python3
import sys
import time
import signal
import logging
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.storage.db import DatabaseManager
from src.collectors.shopee import ShopeeIntelligenceCollector

LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_DIR / "pipeline_runtime.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("RADAR_DAEMON")

class RadarDaemon:
    def __init__(self):
        self.is_running = True
        self.db = DatabaseManager(PROJECT_ROOT / "storage" / "operacoes.db")
        self.shopee = ShopeeIntelligenceCollector()
        self._setup_signals()

    def _setup_signals(self):
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)

    def _handle_shutdown(self, signum, frame):
        logger.info(f"Shutdown signal ({signum}) caught. Executing graceful teardown...")
        self.is_running = False

    def run(self):
        logger.info("Starting Autonomous Deal Radar Ingestion Loop (24/7 Production Mode)...")
        while self.is_running:
            try:
                today = datetime.now().strftime("%Y-%m-%d")
                pending = self.db.get_pending_count(today)
                logger.info(f"Status: Ingestion active. Current pending items in queue: {pending}")

                trends = self.shopee.fetch_trending_searches()
                logger.info(f"Polled {len(trends)} market trends successfully.")

                for _ in range(10):
                    if not self.is_running:
                        break
                    time.sleep(1)
            except Exception as e:
                logger.error(f"Unexpected error in daemon execution loop: {e}", exc_info=True)
                time.sleep(5)

        logger.info("Radar Daemon terminated cleanly.")

if __name__ == "__main__":
    daemon = RadarDaemon()
    daemon.run()
