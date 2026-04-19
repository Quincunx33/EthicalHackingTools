import logging
from datetime import datetime
from pathlib import Path

class SirraLogger:
    def __init__(self):
        log_path = Path("output/logs")
        log_path.mkdir(exist_ok=True, parents=True)
        filename = log_path / f"sirra_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            filename=filename,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def log(self, message):
        logging.info(message)
        print(f"[*] {message}")

logger = SirraLogger()
