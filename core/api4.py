from fastapi import FastAPI, HTTPException
from openai import OpenAI
from pydantic import BaseModel
import asyncio

# Define the request model for API input
class CodeRequest(BaseModel):
    description: str  # Natural language description of the task
    language: str     # Target programming language for the generated code

class Api4:
    def __init__(self, _client, router):
        self.client = _client
        router.add_api_route(
            path="/unit-test",
            endpoint=self.generate_unit,
            methods=["POST"]
        )

    def generateUnitTestFromNL(self, description: str, language: str):
        prompt = [
                {"role": "system", "content": f"You are a unit test writer, you will be given descriptions of functions and you must respond with runnable writen unit tests in {language}. Respond only with the unit test, not an implementation of the function and only respond in code"},
                {"role": "user", "content": description}
                ]
        response = self.client.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=prompt)
        return response.choices[0].message.content

    async def generate_unit(self, request: CodeRequest):
        if not request.description.strip():
            raise HTTPException(status_code=400, detail="Description cannot be empty.")
        if not request.language.strip():
            raise HTTPException(status_code=400, detail="Language cannot be empty.")
        code = await asyncio.to_thread(self.generateUnitTestFromNL, request.description, request.language)
        try:
            code = await asyncio.to_thread(self.generateUnitTestFromNL, request.description, request.language)
            return {"unit-test": code}  # Return generated code as JSON response
        except ValueError as ve:
            raise HTTPException(status_code=500, detail=str(ve))
        except Exception:
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")
