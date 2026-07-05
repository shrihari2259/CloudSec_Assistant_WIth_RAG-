import streamlit as st
from rag_chain import ask

st.set_page_config(
    page_title="CloudSec Assistant",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ CloudSec Assistant")
st.caption(
    "Ask about AWS, Azure, GCP, DevOps, Linux, Networking, Docker, "
    "Kubernetes, Terraform, CI/CD, or Cybersecurity. "
    "Answers are grounded in the ingested knowledge base."
)
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("sources"):
            with st.expander("Sources"):
                for src in msg["sources"]:
                    st.write(f"- {src}")


user_question = st.chat_input("Ask a cloud security question...")

if user_question:
st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)


    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base..."):
            result = ask(user_question)
            answer = result["answer"]
            sources = result.get("sources", [])

        st.markdown(answer)
        if sources:
            with st.expander("Sources"):
                for src in sources:
                    st.write(f"- {src}")

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources
    })

with st.sidebar:
    st.header("Options")
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()
