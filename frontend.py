# Setup streamlit app
import streamlit as st

st.set_page_config(
    page_title="LangGraph AI Agent",
    page_icon=":robot:",
    layout="centered",
    initial_sidebar_state="expanded",
)
st.title("AI Agentic chatbot")
st.write("Create and interact with your AI agent")

system_prompt = st.text_area("Define your AI agent", height=70, placeholder="Type your system prompt")

Groq_models = ["llama3-70b-8192", "mixtral-8x7b-32768", "llama3-70b-versatile"]
OpenAI_models = ["gpt-4o-mini"]

provider=st.radio("Select your model provider", ("Groq", "OpenAI"))
if provider == "Groq":
    model_name = st.selectbox("Select your model", Groq_models)
elif provider == "OpenAI":
    model_name = st.selectbox("Select your model", OpenAI_models)

allow_web_search = st.checkbox("Allow web search")
user_query=st.text_area("Enter your query", height=150,placeholder="Ask anything to your AI agent")

Api_url="http://127.0.0.1:8000/chat"

if st.button("Ask Agent"):
    if user_query.strip():
        # connect with backend
        import requests
        payload={
            "model_name": model_name,
            "model_provider": provider,
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": allow_web_search
        }
        response=requests.post(Api_url,json=payload)
        if response.status_code==200:
            response_json=response.json()
            if "error" in response_json:
                st.error(response_json["error"])
            else:
                # get response from backend and show here
                st.subheader("Agent's response")
                st.markdown(f"**Final response:** {response_json}")

