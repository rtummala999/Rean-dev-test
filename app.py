
from fastapi import FastAPI, HTTPException
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langserve import add_routes
import uvicorn
import os

from langchain_community.llms import OpenAI

from dotenv import load_dotenv

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API Server"
)

# Initialize models for different tasks with a valid model ID
model_calories = ChatOpenAI(model="gpt-4o-mini")
model_diseases = ChatOpenAI(model="gpt-4o-mini")
model_emotions = ChatOpenAI(model="gpt-4o-mini")
model_combine = ChatOpenAI(model="gpt-4o-mini")


# Define prompts for different tasks
#prompt_calories = ChatPromptTemplate.from_template("Extract information about calories in this text and give it only  2 lines answer : {text} 2 lines please  ")
#prompt_diseases = ChatPromptTemplate.from_template("Extract information about any diseases mentioned in this text 2 lines answer please : {text} just 2 lines please")
#prompt_emotions = ChatPromptTemplate.from_template("Respond to this greeting or question appropriately: {text} in 2 lines please")
prompt_emotions = ChatPromptTemplate.from_template("Consider you an expert dietitian for {text} patients. Provide me with ten FAQs in this field along with the answers in a tabular format")
#prompt_document= ChatPromptTemplate.from_template("""Answer the following question based only on the provided context. Think step by step before providing a detailed answer. <context>{context}</context>Question: {input}""")

# Define routes for different tasks
#add_routes(app, prompt_calories | model_calories, path="/calories")
#add_routes(app, prompt_diseases | model_diseases, path="/diseases")
add_routes(app, prompt_emotions | model_emotions, path="/emotions")
#add_routes(app, prompt_combine  |  model_combine, path="/combine")
#add_routes(app, prompt_document | model_emotions, path="/combine")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)