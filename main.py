from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

#temperory code check
@app.get("/check")
def check_key():
    key = os.getenv("OPENAI_API_KEY")
    return {"key_loaded": key is not None}

app = FastAPI()

class Question(BaseModel):
    question: str

class Answer(BaseModel):
    answer: str

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/solve", response_model=Answer)
def solve_question(q: Question):
    try:
        # ✅ Move client here (IMPORTANT FIX)
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        prompt = f"""
        Explain in simple steps for a Class 10 student.

        Step 1:
        Step 2:
        Final Answer:

        Question: {q.question}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return {"answer": response.choices[0].message.content}

    except Exception as e:
        return {"answer": f"Error: {str(e)}"}
