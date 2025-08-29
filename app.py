from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, save_tool, wiki_tool
import os

# Load environment variables
load_dotenv()   

# Define the structured response format
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

# Initialize the LLM
llm  = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# Parser for structured output
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# Prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a research assistant that will help generate a research paper.
Answer the user query and use necessary tools you require.
Whenever the user asks to save to a file you must use the 'save_to_txt' tool.
Output MUST be a valid JSON matching this structure:
{{
    "topic": "...",
    "summary": "...",
    "sources": ["...", "..."],
    "tools_used": ["...", "..."]
}}
Do not include any extra text outside the JSON.""",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),   
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

# Tools
tools = [search_tool, save_tool, wiki_tool]

# Create the tool-calling agent
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

# Create the executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Initialize chat history
chat_history = []

print("🤖 ResearchBot: Hi! I can help you research topics. Type /bye to exit.\n")

# Chat loop
while True:
    user_input = input("You: ")

    if user_input.strip().lower() in ["/bye", "bye", "exit"]:
        print("🤖 ResearchBot: Goodbye! Happy researching. 👋")
        break

    # Append user input to chat history
    chat_history.append({"role": "user", "content": user_input})

    # Invoke the agent
    raw_response = agent_executor.invoke({
        "query": user_input,
        "chat_history": chat_history
    })

    try:
        # Parse structured response
        structured_response = parser.parse(raw_response.get("output"))
        print("🤖 ResearchBot:", structured_response)

        # Save automatically
        save_tool.func(str(structured_response))

        # Append agent response to chat history for context
        chat_history.append({"role": "assistant", "content": str(structured_response)})

    except Exception as e:
        print("🤖 ResearchBot: Error parsing response:", e)
        print("Raw Response:", raw_response)