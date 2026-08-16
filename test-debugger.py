from pathlib import Path
import configparser

PROJECT_ROOT = Path(__file__).resolve().parent

config_file = PROJECT_ROOT / "environment.cfg"

print("Config:", config_file)

config = configparser.ConfigParser()
config.read(config_file)

print("Sections:", config.sections())