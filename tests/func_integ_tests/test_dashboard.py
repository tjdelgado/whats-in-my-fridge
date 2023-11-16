# runs a basic functional test on the dashboard

def test_dashboard(client): #TODO!
    response = client.get('/')
    # need b before string to make bytes literal for type matching to response.data

    expected_response = b"""<tr>
            <td>eggs</td>
            <td>2023-11-11</td>"""
    assert 1 == 1
