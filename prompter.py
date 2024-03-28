from openai import OpenAI
import streamlit as st
import json

PROMPTS = json.load(open("prompts.json"))

with st.sidebar:
    # Add a button to this sidebar to change the system prompt
    st.markdown("## Choose a mode")
    # The following button changes the system prompt on the first element of the messages state

    if st.button(f"Base system"):
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful assistant."},
        ]
        st.session_state.model = "nous-hermes-2-mixtral-8x7b-dpo"

    for prompt in PROMPTS:
        if st.button(prompt["name"]):
            st.session_state.messages = [
                {"role": "system", "content": prompt["prompt"]},
            ]
            st.session_state.model = prompt["model"]

    openai_api_key = st.text_input(
        "OctoAI API Key", key="chatbot_api_key", type="password"
    )
    "[View the source code](https://github.com/ptorru/prompter/blob/main/prompter.py)"


st.title("💬 Prompter")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key, base_url="https://text.octoai.run/v1")
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(
        model=st.session_state.model, messages=st.session_state.messages
    )
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
