import bincode


def test_search():
    assert bincode.search(371449635)['id'] == 'amex'
