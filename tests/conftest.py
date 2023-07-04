import pytest
import shutil
import os
from .general_utils import image_path


@pytest.fixture(autouse=True)
def setup():
    # remove the images directory if it exists
    if os.path.exists(image_path):
        shutil.rmtree(image_path)
    # create the images directory
    os.makedirs(image_path)


# at the end of all tests, remove the images directory
@pytest.fixture(autouse=True, scope="session")
def teardown_session():
    yield
    if os.path.exists(image_path):
        shutil.rmtree(image_path)
