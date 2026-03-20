import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# 1. Professional UI Setup
st.set_page_config(page_title="RK's AI Assistant", page_icon="", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; color: #e0f2fe !important; }
    h1 { color: #38bdf8 !important; text-shadow: 0px 0px 10px rgba(56,189,248,0.5); }
    [data-testid="stChatMessage"] { background-color: #111827 !important; border: 1px solid #38bdf8; border-radius: 10px; }
    .stChatInputContainer { border: 1px solid #38bdf8 !important; background-color: #111827 !important; }
    label, p { color: #7dd3fc !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("RK's AI Assistant")

# 2. Sidebar for Configuration
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Gemini API Key", type="password")
    model_choice = st.selectbox("Model", ["gemini-1.5-flash", "gemini-1.5-pro"])
    if st.button("Reset Chat"):
        st.session_state.messages = []
        st.rerun()

# 3. Chat Logic
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Message RK's AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if not api_key:
        st.info("Please enter your Gemini API Key in the sidebar.")
    else:
        try:
            # Using LangChain to connect to Gemini
            llm = ChatGoogleGenerativeAI(model=model_choice, google_api_key=api_key)
            response_obj = llm.invoke([HumanMessage(content=prompt)])
            response = response_obj.content
            
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error: {e}")
