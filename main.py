from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os


load_dotenv()

llm  = ChatGoogleGenerativeAI(model="gemini-1.5-flash",google_api_key=os.getenv("GEMINI_API_KEY"))
response = llm.invoke("What is the meaning of coding all the day?!")
print(response.content)