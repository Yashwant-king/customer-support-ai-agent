
import streamlit as st
import uuid
from langchain_core.runnables import RunnableConfig
from graph.main import app
from graph.random_id import get_random_customer_id
from graph.state import SupportState

# Initialize session state once
if "customer_id" not in st.session_state:
    st.session_state.customer_id = str(get_random_customer_id())

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

customer_id = st.session_state.customer_id

config: RunnableConfig = {
    "configurable": {
        "thread_id": st.session_state.thread_id,
    },
}

st.title("Customer Support System")

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Accept one query at a time
user_query = st.chat_input("Enter your query here...")

if user_query:
    if user_query.strip().lower() in ["exit", "quit", "close"]:
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Chat ended. Goodbye!"
        })
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

    # Display and save the user's query
    st.session_state.messages.append({
        "role": "user",
        "content": user_query
    })

    with st.chat_message("user"):
        st.write(user_query)

    # Invoke your LangGraph workflow
    with st.chat_message("assistant"):
        with st.spinner("Processing your query..."):
            state = SupportState(
                customer_id=customer_id,
                customer_query=user_query,
                final_result=None,
                node_1=None,
                node_2=None,
                blank_list=None,
            )

            output = app.invoke(state, config=config)
            answer = output["final_result"]

        st.write(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
