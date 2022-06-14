"""
Websocket Price Publisher
"""
from pathlib import Path
from dotenv import load_dotenv
import logging
import sys

__version__ = "0.0.2"

# Load env variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Setup Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug-publisher.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
