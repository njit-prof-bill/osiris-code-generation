from fastapi import FastAPI, HTTPException
from openai import OpenAI
from pydantic import BaseModel
import asyncio

# Define the request model for API input
class CodeRequest(BaseModel):
    description: str  # Natural language description of the task
    code: str
    language: str     # Target programming language for the generated code


class Api10:
    def __init__(self, _client, router):
        self.client = _client
        router.add_api_route(
            path="/validate_code",
            endpoint=self.validate_code,
            methods=["POST"]
        )

    def generateValidation(self, description: str, code: str, language: str):
        prompt = [
                {"role": "system", "content": f"You are a code tester, you will be given a function in {language} and a description of what the code should do. Respond in either a yes or a no if the code works as intended and explain why it does or does not work as intended"},
                {"role": "user", "content": f"The description is as follows: {description}\n The code is as follows: {code}"}
                ]
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=prompt)
        if "yes" in response.choices[0].message.content.lower():
            return True
        else:
            return False


    async def validate_code(self, request: CodeRequest):
        if not request.description.strip():
            raise HTTPException(status_code=400, detail="Description cannot be empty.")
        if not request.language.strip():
            raise HTTPException(status_code=400, detail="Language cannot be empty.")
        if not request.code.strip():
            raise HTTPException(status_code=400, detail="Code cannot be empty.")
        try:
            code = await asyncio.to_thread(self.generateValidation, request.description, request.code, request.language)
            return {"valid": code}
        except ValueError as ve:
            raise HTTPException(status_code=500, detail=str(ve))
        except Exception:
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")
