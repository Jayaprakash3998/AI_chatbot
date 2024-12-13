import streamlit as st
from chatbot_logic import Chatbot

# Initialize session state for context and chatbot
if "context" not in st.session_state:
    st.session_state.context = []

if "chatbot" not in st.session_state:
    st.session_state.chatbot = Chatbot()

# Streamlit UI
st.title(" 🤖 Gobal the AI Bot 🤖")
st.markdown("Chat with **Gobal**, an AI assistant powered by LangChain, Ollama, and Streamlit!")

# User Input
user_input = st.text_input("You:", "")

if user_input:
    # Get chatbot response
    chatbot = st.session_state.chatbot
    response = chatbot.get_response(user_input, st.session_state.context)

    # Update context
    st.session_state.context.append((user_input, response))

    # Display conversation
    for user, assistant in st.session_state.context:
        st.write(f"**You:** {user}")
        st.write(f"**🤖Gobal🤖:** {assistant}")

# End Chat Button
if st.button("End Chat"):
    st.session_state.context = []
    st.write("**Assistant:** Goodbye! Let's start a new conversation.")
