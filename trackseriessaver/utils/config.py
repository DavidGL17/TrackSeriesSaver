import yaml

# Settings

with open("settings.yml", "r") as f:
    config = yaml.safe_load(f)

username: str = config["username"]
password: str = config["password"]

data_path: str = config["data_path"]
image_path: str = data_path + "/images"
database_path: str = data_path + "/database"
