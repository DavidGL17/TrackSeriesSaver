import yaml

# Settings

with open("settings.yml", "r") as f:
    config = yaml.safe_load(f)

username = config["username"]
password = config["password"]

data_path = config["data_path"]
image_path = data_path + "/images"
database_path = data_path + "/database"
