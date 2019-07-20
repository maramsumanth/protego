from os import listdir
from os.path import isfile, join, dirname, abspath
import pytest

from protego import Protego

test_data_directory = join(dirname(abspath(__file__)), 'test_data')
robotstxts = [(f) for f in listdir(test_data_directory) if isfile(join(test_data_directory, f))]


@pytest.mark.parametrize('path_to_robotstxt', robotstxts)
def test_no_exceptions(path_to_robotstxt):
    try:
        with open(join(test_data_directory, path_to_robotstxt), 'rb') as f:
            Protego.parse(content=f.read().decode('utf-8'))
    except:
        assert False, "Exception raised while parsing {}".format(join(path_to_robotstxt, 'robots.txt'))