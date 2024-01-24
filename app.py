from fastapi import FastAPI
from backend import main_point_for_answers, message_answer
from pydantic import BaseModel
import uvicorn

app = FastAPI()

qa_chain = None


# Register the function to run during startup
# @app.on_event("startup")
def startup_event():
    print("starting up")
    global qa_chain
    qa_chain = main_point_for_answers()


class QuestionResponse(BaseModel):
    question: str
    answer: str

@app.get("/predict")
def predict_sentiment(question: str):
    print(question)
    answer = message_answer(question, qa_chain)

    response = QuestionResponse(
        question=question,
        answer = answer,
    )

    return response

app.add_event_handler("startup", startup_event)

if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)