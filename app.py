
import os
import uuid
import streamlit as st
from datetime import datetime
from langchain_groq import ChatGroq

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="NexaAI",
    page_icon="🤖",
    layout="wide"
)

# ---- SESSION STATE ----
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

# ---- CREATE NEW CHAT ----
def create_new_chat():
    chat_id = str(uuid.uuid4())

    st.session_state.chats[chat_id] = {
        "title": "New Chat",
        "messages": [],
        "created_at": datetime.now().strftime("%d %b %Y, %I:%M %p")
    }

    st.session_state.current_chat = chat_id


# Create first chat automatically
if st.session_state.current_chat is None:
    create_new_chat()


# ---- SIDEBAR ----
st.sidebar.title("🤖 NexaAI")
st.sidebar.caption("Your Intelligent AI Assistant")

if st.sidebar.button("➕ New Chat", use_container_width=True):
    create_new_chat()
    st.rerun()

st.sidebar.divider()

# ---- CHAT HISTORY ----
st.sidebar.subheader("💬 Chat History")

if not st.session_state.chats:
    st.sidebar.info("No chat history available.")

else:
    # Show latest chats first
    for chat_id, chat in reversed(
        list(st.session_state.chats.items())
    ):

        title = chat["title"]

        if st.sidebar.button(
            f"💬 {title[:30]}",
            key=f"chat_{chat_id}",
            use_container_width=True
        ):
            st.session_state.current_chat = chat_id
            st.rerun()

# ---- DELETE CURRENT CHAT ----
if st.sidebar.button(
    "🗑️ Delete Current Chat",
    use_container_width=True
):

    current_id = st.session_state.current_chat

    if current_id in st.session_state.chats:
        del st.session_state.chats[current_id]

    st.session_state.current_chat = None
    st.rerun()

st.sidebar.divider()

# ---- SETTINGS ----
st.sidebar.subheader("⚙️ Settings")

api_key = st.sidebar.text_input(
    "Enter GROQ API Key",
    type="password",
    placeholder="Enter your Groq API key"
)

temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.0,
    step=0.1
)

# ---- MULTIPLE AI MODELS ----
model_options = {
    "Qwen 3.8 27B": "qwen/qwen3.8-27b",
    "GPT OSS 120B": "openai/gpt-oss-120b",
    "GPT OSS 20B": "openai/gpt-oss-20b"
}

selected_model = st.sidebar.selectbox(
    "🤖 Select AI Model",
    options=list(model_options.keys())
)

model = model_options[selected_model]

st.sidebar.success(f"Selected: {selected_model}")

st.sidebar.divider()
st.sidebar.caption("Powered by Groq API")
st.sidebar.caption("Built with Python & Streamlit")


# ---- MAIN APP HEADER ----
st.title("🤖 NexaAI")
st.subheader("Your Intelligent Multi-Model AI Assistant")
st.write("Ask anything and explore the power of multiple AI models.")

st.divider()

# ---- CURRENT CHAT ----
current_chat = st.session_state.current_chat
chat_data = st.session_state.chats[current_chat]

st.markdown("### 💬 " + chat_data["title"])

# ---- DISPLAY CHAT MESSAGES ----
for message in chat_data["messages"]:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---- USER INPUT ----
user_input = st.chat_input(
    "Ask NexaAI anything..."
)

# ---- GENERATE RESPONSE ----
if user_input:

    if not api_key:
        st.warning("⚠️ Please enter your Groq API key.")

    else:

        try:
            os.environ["GROQ_API_KEY"] = api_key

            # Save user message
            chat_data["messages"].append({
                "role": "user",
                "content": user_input
            })

            # Set chat title from first question
            if chat_data["title"] == "New Chat":
                chat_data["title"] = user_input[:30]

            # Display user message
            with st.chat_message("user"):
                st.markdown(user_input)

            # Prepare conversation history
            messages = [
                {
                    "role": message["role"],
                    "content": message["content"]
                }
                for message in chat_data["messages"]
            ]

            groq_chat = ChatGroq(
                model=model,
                temperature=temperature
            )

            # Generate AI response
            with st.chat_message("assistant"):

                with st.spinner("🤖 NexaAI is thinking..."):

                    response = groq_chat.invoke(messages)

                ai_response = response.content

                st.markdown(ai_response)

            # Save AI response
            chat_data["messages"].append({
                "role": "assistant",
                "content": ai_response
            })

            st.rerun()

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


# ---- FOOTER ----
st.divider()

st.caption(
    "© 2026 NexaAI | Multi-Model Generative AI Assistant"
)
