from fastapi import FastAPI, HTTPException
from openai import OpenAI
import os

app = FastAPI()
client = OpenAI()



@app.post('/validate', status_code=200)
def generateValidation(description: str, code: str, language: str):
    if description == '':
        raise HTTPException(status_code=400, detail="No description defined")
    elif language == '':
        raise HTTPException(status_code=400, detail="No language defined")
    elif code == '':
        raise HTTPException(status_code=400, detail="No code defined")

    prompt = [
            {"role": "system", "content": f"You are a code tester, you will be given a function in {language} and a description of what the code should do. Respond in either a yes or a no if the code works as intended and explain why it does or does not work as intended"},
            {"role": "user", "content": f"The description is as follows: {description}\n The code is as follows: {code}"}
            ]
    try:
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=prompt)
    except:
        raise HTTPException(status_code=500, detail="Internal Service Error: Likely Need new API Key")
    return {"response": response.choices[0].message.content}
