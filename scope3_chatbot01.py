import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
import os
from pathlib import Path
import uuid
import json

def ensure_log_dir(log_dir_path):
    """
    Create chat log dir, if not exists
    """
    log_dir_path = Path(log_dir_path)
    if not log_dir_path.exists():
        log_dir_path.mkdir(parents=True)

def create_log_file(log_dir_path):
    """
    Create chat log file for each chat
    """
    log_dir_path = Path(log_dir_path)
    unique_filename = f"{uuid.uuid4()}.txt"
    log_file_path = log_dir_path / unique_filename
    log_file_path.touch()
    return log_file_path

# Establish the log_file for this chat instance
if "log_file_path" not in st.session_state.keys():
    log_dir_path = Path("chat_logs")
    ensure_log_dir(log_dir_path)
    log_file_path = create_log_file(log_dir_path)
    st.session_state.log_file_path = log_file_path

def log_message(log_file_path, message):
    """
    log each message to the log_file
    """
    with log_file_path.open('a') as f:
        f.write(json.dumps(message) + '\n')

title_str = "ClimateChoice Scope 3 Expert"
st.set_page_config(page_title=title_str, page_icon="💚", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title(title_str)
st.info("I’m your educational assistant for the latest GHG Protocol Scope 3 standards. "
        "Whether you’re new to Scope 3 accounting or need guidance on target setting, I provide detailed insights and updates, including the latest 2024 proposals. " 
        "Tip: sharing your industry and specific needs helps me offer more precise support.",
        icon="🍀")
st.info("Visit the ClimateChoice [here](https://www.theclimatechoice.com), and learn more about this chatbot [here](https://github.com/y-f-a/scope3chatbot).",
        icon="🖥️")


 # Initialize the chat message history
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I assist you with Scope 3 today?"}
    ]
    log_message(st.session_state.log_file_path, {"role": "system", "content": "<New-Chat-Started>"})

@st.cache_resource(show_spinner=False)
def create_index():
    """
    create the llamaindex RAG index as a cached resource
    # https://docs.llamaindex.ai/en/stable/
    """
    system_prompt="""You are a helpful expert on topics around Scope 3 emissions,
    and your job is to answer questions on the topic from people who want to learn from you. 
    Assume that all questions are related to Scope 3 emissions. 
    Make your answers accessible to a wide audience of non-experts, but keep your answers technical and based on facts – do not hallucinate features.
    Make answers easy to read - when it makes sense, you may occasionally use bullet points and markdown as useful formatting options.
    Try to be very brief and ask if any further detail is required on any of the key points.
    Ask the user questions to help them along with and guide the conversation. 
    A good place to start is to ask about what industry or activities they are involved in.
    If you do not have the data to answer to their question to a high level of confidence, apologise and let them know without making up an answer."""

    with st.spinner(text="Initialising chatbot: loading and indexing documents – this should take about a minute or so."):
        reader = SimpleDirectoryReader(input_dir="./scope3_data", recursive=True)
        docs = reader.load_data()
        Settings.llm = AzureOpenAI(engine="gpt-4-turbo-2024-04-09", #deployment_name
            #model="gpt-4o",
            api_key=st.secrets["AZURE_OPENAI_API_KEY"],
            azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT"],
            api_version=st.secrets["OPENAI_API_VERSION"],
            temperature=0.0,
            system_prompt = system_prompt
        )
        Settings.embed_model = AzureOpenAIEmbedding(
            deployment_name="text-embedding-3-large", #"text-embedding-3-large",
            api_key=st.secrets["AZURE_OPENAI_API_KEY"],
            azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT"],
            api_version=st.secrets["OPENAI_API_VERSION"]
        )
        index = VectorStoreIndex.from_documents(docs)
        return index

index = create_index()

# Get the chat engine from the session_state
if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
    st.session_state.chat_engine = index.as_chat_engine(
        chat_mode="condense_question", verbose=True, streaming=True
    )

# Retrieve existing messages 
if "messages" not in st.session_state:
    st.session_state.messages = []

# Print existing messages to screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Start the chat
if prompt:= st.chat_input("Ask a question."):
    # Add user message to message history
    user_message = {"role": "user", "content": prompt}
    st.session_state.messages.append(user_message)
    log_message(st.session_state.log_file_path, user_message)
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # get the llm response to the user prompt   
    with st.chat_message("assistant"):
        response_stream = st.session_state.chat_engine.stream_chat(prompt)
        st.write_stream(response_stream.response_gen)
        assistant_message = {"role": "assistant", "content": response_stream.response}
        st.session_state.messages.append(assistant_message)
        log_message(st.session_state.log_file_path, assistant_message)