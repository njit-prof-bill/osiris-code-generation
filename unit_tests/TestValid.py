import requests
import os
from urllib.parse import quote, unquote

def test_no_desc():
    description =  ""
    language= "python"
    code = ""
    response = requests.post(f'http://localhost:8000/validate?description={description}&code={code}&language={language}')
    assert response.status_code == 400

def test_no_lang():
    description =  "desc"
    language= ""
    code=""
    response = requests.post(f'http://localhost:8000/validate?description={description}&code={code}&language={language}')
    assert response.status_code == 400

def test_no_code():
    description =  "desc"
    language= "python"
    code=""
    response = requests.post(f'http://localhost:8000/validate?description={description}&code={code}&language={language}')
    assert response.status_code == 400


def test_correct():
    try:
        assert os.environ['OPENAI_API_KEY'] != ''
    except:
        assert 1 == 0
    description = "Sum of two integers"
    with open('testFiles/sum.py', 'r') as f:
        code = quote(f.read().encode())
    language = "python"
    response = requests.post(f'http://localhost:8000/validate?description={description}&code={code}&language={language}')
    assert "yes" in response.text.lower()

def test_incorrect():
    try:
        assert os.environ['OPENAI_API_KEY'] != ''
    except:
        assert 1 == 0
    description = "Sum of two integers"
    with open('testFiles/badSum.py', 'r') as f:
        code = quote(f.read().encode())
    language = "python"
    params={"description": description, "code": code, "language": language}
    response = requests.post(f'http://localhost:8000/validate?description={description}&code={code}&language={language}')
    assert "no" in response.text.lower()

