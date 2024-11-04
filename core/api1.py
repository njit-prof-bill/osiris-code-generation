from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio

# Define the request model for API input
class CodeRequest(BaseModel):
    description: str  # Natural language description of the task
    language: str     # Target programming language for the generated code

class Api1:
    def __init__(self, _client, router):
        self.client = _client
        router.add_api_route(
            path="/generate-code", 
            endpoint=self.generate_code, 
            methods=["POST"]
        )
        
    # Function to generate code from natural language description using OpenAI's API
    def generateCodeFromNL(self, description: str, language: str) -> str:
        prompt = f"Write a function in {language} to accomplish the following task: {description}."
        
        # Call OpenAI API to generate the code based on the prompt
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant that provides code based on user descriptions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=512,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Extract generated code from the response
        code_block = response.choices[0].message.content.strip()
        
        # Raise an error if no code was generated
        if not code_block:
            raise ValueError("No code was generated by the model.")
        
        return code_block

    async def generate_code(self, request: CodeRequest):
        # Check if description and language are empty
        if not request.description.strip():
            raise HTTPException(status_code=400, detail="Description cannot be empty.")
        if not request.language.strip():
            raise HTTPException(status_code=400, detail="Language cannot be empty.")
        
        try:
            # Run the code generation in a separate thread to avoid blocking
            code = await asyncio.to_thread(self.generateCodeFromNL, request.description, request.language)
            return {"code": code}  # Return generated code as JSON response
        except ValueError as ve:
            # Handle cases where no code was generated
            raise HTTPException(status_code=500, detail=str(ve))
        except Exception:
            # Handle errors
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")
