import requests
import os


def test_no_desc():
    description =  ""
    language= "python"
    response = requests.post(f'http://localhost:8000/unit?description={description}&language={language}')
    assert response.status_code == 400

def test_no_lang():
    description =  "desc"
    language= ""
    response = requests.post(f'http://localhost:8000/unit?description={description}&language={language}')
    assert response.status_code == 400

def test_resp():
    try:
        assert os.environ['OPENAI_API_KEY'] != ''
    except:
        assert 1 == 0
    description = "Sum of two integers"
    language = "python"
    response = requests.post(f'http://localhost:8000/unit?description={description}&language={language}')
    assert response.status_code == 200
