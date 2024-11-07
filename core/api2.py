import asyncio
import json
from fastapi import HTTPException
from pydantic import BaseModel


class CodeRequest(BaseModel):
    description: str  # The natural language description of the API functionality
    method: str  # The HTTP method for the API

 
class Api2:
    def __init__(self, _client, router):
        self.client = _client
        router.add_api_route(
            path="/generate_api_defenition/",
            endpoint=self.generate_api_defenition,
            methods=["POST"]
        )

    def generateAPIDefinitionFromNL(self, description: str, method: str) -> dict:
        base_prompt = f"""Create an API definition with the following description:
"{description}"
The HTTP method of the API is {method} and the API definition in Python dictionary format like this:"
{{
    "method": "{method}",
    "url": "",
    "params": []
}}
Make sure the output is a valid Python dictionary."""

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": base_prompt}]
        )

        api_response = response.choices[0].message.content
        api_definition = json.loads(api_response)

        return api_definition

    async def generate_api_defenition(self, request: CodeRequest):
        if not request.description:
            raise HTTPException(
                status_code=400, detail="Description must be provided in search query")

        try:
            api_definition = await asyncio.to_thread(self.generateAPIDefinitionFromNL, request.description)
            return api_definition

        except json.JSONDecodeError:
            raise HTTPException(
                status_code=500, detail="Could not decode JSON response from OpenAI.")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
