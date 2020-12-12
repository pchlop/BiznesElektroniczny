from dotenv import load_dotenv
from pathlib import Path
env_path = Path('.').parent / '.env'
load_dotenv(dotenv_path=env_path)
