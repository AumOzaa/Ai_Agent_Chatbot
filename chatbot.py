import streamlit as st
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

# Define structured response format
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

# Initialize the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# Parser
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# Prompt
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

# Agent
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- STREAMLIT FRONTEND ---

st.set_page_config(page_title="ResearchBot", page_icon="🤖")
st.title("🤖 ResearchBot - AI Research Assistant")

# Session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.chat_input("Ask me something to research... (type /bye to exit)")

if user_input:
    if user_input.strip().lower() in ["/bye", "bye", "exit"]:
        st.chat_message("assistant").write("Goodbye! 👋 Happy researching.")
    else:
        # Display user message
        st.chat_message("user").write(user_input)

        # Add to history
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Run agent
        raw_response = agent_executor.invoke({
            "query": user_input,
            "chat_history": st.session_state.chat_history
        })

        try:
            structured_response = parser.parse(raw_response.get("output"))

            # Show bot response
            with st.chat_message("assistant"):
                st.write(f"**Topic:** {structured_response.topic}")
                st.write(f"**Summary:** {structured_response.summary}")
                st.write(f"**Sources:** {', '.join(structured_response.sources)}")
                st.write(f"**Tools Used:** {', '.join(structured_response.tools_used)}")

            # Save automatically
            save_tool.func(str(structured_response))

            # Add bot response to history
            st.session_state.chat_history.append(
                {"role": "assistant", "content": str(structured_response)}
            )

        except Exception as e:
            with st.chat_message("assistant"):
                st.error("Error parsing response. Showing raw response.")
                st.write(raw_response)