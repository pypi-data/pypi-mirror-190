
from kraken_image_face import kraken_image_face as k   



def test_get_face():

    file_path = 'tests/test.png'
    k.get(file_path)
    