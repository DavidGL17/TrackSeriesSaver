from .dataSource.trackseries import (
    login,
    processSerie,
)
from .general_utils import (
    image_path,
    serie1_json_path,
    serie2_json_path,
    serie1_reference_json_path,
    serie2_reference_json_path,
)
from .entities import decodeSerie
import json


def test_login():
    username = "test"
    password = "test"
    login_response = login(username, password)
    assert "message" in login_response
    assert "access_token" not in login_response


def test_process_serie():
    for reference, test in [
        (serie1_reference_json_path, serie1_json_path),
        (serie2_reference_json_path, serie2_json_path),
    ]:
        with open(reference) as f:
            reference_serie = decodeSerie(json.load(f))
        with open(test) as f:
            test_serie = json.load(f)
            test_serie = processSerie(test_serie, image_path)
        assert reference_serie.__eq__(test_serie)
