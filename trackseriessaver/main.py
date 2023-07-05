from trackseriessaver.dataSource.trackseries import save_series
from trackseriessaver.utils.config import username, password, image_path


def main():
    save_series(username, password, image_path)


if __name__ == "__main__":
    main()
