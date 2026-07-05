import streamlit as st
from rag_chain import ask

# ---- Page config ----
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

# ---- Session state: chat history ----
# st.session_state persists across reruns within the same browser session.
# Each entry is a dict: {"role": "user"/"assistant", "content": str, "sources": list}
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---- Render existing chat history ----
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("sources"):
            with st.expander("Sources"):
                for src in msg["sources"]:
                    st.write(f"- {src}")

# ---- Chat input box (pinned at bottom automatically by Streamlit) ----
user_question = st.chat_input("Ask a cloud security question...")

if user_question:
    # 1. Show the user's message immediately
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    # 2. Call your existing RAG pipeline (unchanged logic from rag_chain.py)
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

    # 3. Save assistant response to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources
    })

# ---- Sidebar: reset button ----
with st.sidebar:
    st.header("Options")
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()