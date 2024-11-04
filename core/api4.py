from fastapi import FastAPI, HTTPException
from openai import OpenAI
import os

app = FastAPI()
client = OpenAI()


@app.post('/unit', status_code=200)
def generateUnitTestFromNL(description: str, language: str):
    if description == '':
        raise HTTPException(status_code=400, detail="No description defined")
    if language == '':
        raise HTTPException(status_code=400, detail="No language defined")
    prompt = [
            {"role": "system", "content": f"You are a unit test writer, you will be given descriptions of functions and you must respond with runnable writen unit tests in {language}. Respond only with the unit test, not an implementation of the function and only respond in code"},
            {"role": "user", "content": description}
            ]
    try:
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=prompt)
    except:
        raise HTTPException(status_code=500, detail="Internal Service Error: Likely Need new API Key")
    return {"response": response.choices[0].message.content}


