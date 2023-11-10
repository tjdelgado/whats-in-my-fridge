# runs the most basic test on our most basic of stub homepage functions
# get rid of me soon!
# adapted from flaskr test tests/test_factory.py

def test_login(client):
    response = client.get('/')
    # need b before string to make bytes literal for type matching to response.data
    assert b"eggs, expiry_time: 14" in response.data
