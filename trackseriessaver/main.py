from trackseriessaver.dataSource.trackseries import save_series
from trackseriessaver.utils.config import username, password


def main():
    save_series(username, password)


if __name__ == "__main__":
    main()
