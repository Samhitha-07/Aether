#setup API keys
from dotenv import load_dotenv
load_dotenv()
import os
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

#setup LLM and tools
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

openai_llm=ChatOpenAI(model="gpt-4o-min" , api_key=OPENAI_API_KEY)
groq_llm=ChatGroq(model="llama-3.3-70b-versatile",api_key=GROQ_API_KEY)

search_tool =TavilySearchResults(max_results=3)

#setup AI agent with search tool functionality
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage
system_prompt = "Act as an AI agent who is smart and friendly"

def get_response_from_ai_agent(llm_id,query,allow_search,system_prompt,provider):
    
    if provider =="Groq":
        llm=ChatGroq(model=llm_id,api_key=GROQ_API_KEY)
    elif provider=="OpenAI":
        llm=ChatOpenAI(model=llm_id,api_key=OPENAI_API_KEY)

    tools =[TavilySearchResults(max_results=3)] if allow_search else []
    agent = create_react_agent(
        model=groq_llm,
        tools=tools,
        state_modifier=system_prompt
    )

    state={"messages" : query}
    response = agent.invoke(state)
    messages=response.get("messages")
    ai_messages=[message.content for message in messages if isinstance(message, AIMessage)]
    return ai_messages[-1]