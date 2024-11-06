import asyncio
from fastapi import HTTPException
from pydantic import BaseModel


class CodeRequest(BaseModel):
    description: str  # The natural language description of the class to generate
    language: str  # The programming language for the generated class


class Api6:
    def __init__(self, _client, router):
        self.client = _client
        router.add_api_route(
            path="/generate_class/",
            endpoint=self.generate_class,
            methods=["POST"]
        )

    def generateClassFromNL(self, description: str, language: str) -> dict:
        base_prompt = f"Create a {language} class based of the following discription: \"{description}\""

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": base_prompt}]
        )

        class_string = str(response.choices[0].message.content)

        return class_string

    async def generate_class(self, request: CodeRequest):
        if not request.description:
            raise HTTPException(
                status_code=400, detail="Description must be provided in search query")

        try:
            class_string = await asyncio.to_thread(self.generateClassFromNL, request.description)
            return class_string

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
