from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio

class CodeRequest(BaseModel):
    description: str
    language: str

class Api5:
    def __init__(self, _client, router):
        self.client = _client
        router.add_api_route(
            path="/generate-code-documentation", 
            endpoint=self.generate_code, 
            methods=["POST"]
        )
    
    def generateCodeDocumentationFromNL(self, description: str, language: str) -> str:
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant that provides code if not provided and places documentation comments in the function, class, or module."},
                {"role": "user", "content": f"In {language} document the following: {description}"}
            ],
            temperature=0,
            max_tokens=512,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        code_block = response.choices[0].message.content.strip()
        
        if not code_block:
            raise ValueError("No code was generated by the model.")
        
        return code_block

    async def generate_code(self, request: CodeRequest):
        if not request.description.strip():
            raise HTTPException(status_code=400, detail="Description cannot be empty.")
        if not request.language.strip():
            raise HTTPException(status_code=400, detail="Language cannot be empty.")
        
        try:
            code = await asyncio.to_thread(self.generateCodeDocumentationFromNL, request.description, request.language)
            return {"code": code}
        except ValueError as ve:
            raise HTTPException(status_code=500, detail=str(ve))
        except Exception:
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")

