# make a post request to an url and save the response in a file

from trackseriessaver.dataSource.trackseries import login, get_series
from trackseriessaver.config import username, password


def main():
    login_response: dict = login(username, password)
    print(login_response)
    access_token: str = login_response["access_token"]
    series = get_series(access_token)
    print(type(series))
    print(len(series))

    # with open("tests/data/serie1.json") as f:
    #     series1 = json.load(f)
    # with open("tests/data/serie2.json") as f:
    #     series2 = json.load(f)

    # img_path = "tmp_data"
    # if not os.path.exists(img_path):
    #     os.makedirs(img_path)

    # serie1: Serie = processSerie(series1, img_path)
    # serie2: Serie = processSerie(series2, img_path)
    # for serie in [serie1, serie2]:
    #     # save the serie to a json file
    #     with open(f"{img_path}/{serie.id}.json", "w") as f:
    #         json.dump(serie, f, indent=4, cls=SerieEncoder)

    # # test the reverse process
    # with open(f"{img_path}/{serie1.id}.json") as f:
    #     afterserie1 = json.load(f)
    # with open(f"{img_path}/{serie2.id}.json") as f:
    #     afterserie2 = json.load(f)

    # afterserie1 = decodeSerie(afterserie1)
    # afterserie2 = decodeSerie(afterserie2)

    # # check every attribute and see if they are equal
    # for reference, readSeries in [(serie1, afterserie1), (serie2, afterserie2)]:
    #     print(type(reference))
    #     print(type(readSeries))
    #     # compare them using the eq operator
    #     assert reference.__eq__(readSeries)


if __name__ == "__main__":
    main()
