import yaml

# Settings

with open("settings.yml", "r") as f:
    config = yaml.safe_load(f)

username = config["username"]
password = config["password"]
