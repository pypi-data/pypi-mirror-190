import pytest
from kortical.app import get_config
from module_placeholder.api.http_status_codes import HTTP_OKAY, UNAUTHORISED

app_config = get_config(format='yaml')
api_key = app_config['api_key']


@pytest.mark.unit
def test_index_endpoint(client):
    response = client.get(f'/?api_key={api_key}')
    assert response.status_code == HTTP_OKAY


@pytest.mark.unit
def test_predict_endpoint(client):
    test_data = {
        "sport": "Ronaldo scored the goal",
        "tech": "Startups using crypto mining software used all the computers",
        "politics": "The corrupt ministers rise to leadership positions in all political parties",
        "entertainment": "Watching paint dry is an all time classic film",
        "business": "corporate merger, acquisition"
    }

    for category, text in test_data.items():
        request_data = {
            "input_text": text
        }
        response = client.post(f'/predict?api_key={api_key}', json=request_data)
        assert response.status_code == HTTP_OKAY, response.text
        assert response.text == category


@pytest.mark.unit
def test_predict_endpoint_no_api_key(client):
    response = client.post(f'/predict')
    assert response.status_code == UNAUTHORISED


@pytest.mark.unit
def test_predict_endpoint_wrong_api_key(client):
    response = client.post(f'/predict?api_key={api_key}12345')
    assert response.status_code == UNAUTHORISED
