import yaml

# Settings

with open("settings.yml", "r") as f:
    config = yaml.safe_load(f)

username: str = config["username"]
password: str = config["password"]

# data paths
data_path: str = config["data_path"]
image_path: str = data_path + "/images"
database_path: str = data_path + "/database"

# Logging
logging_level: str = config["logging_level"]
log_file: str = config["log_file"]
