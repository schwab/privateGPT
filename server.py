from ingest import does_vectorstore_exist, get_embeddings
import streamlit as st
import os
from os.path import isfile, join
from os import listdir
from privateGPT import QueryProcessor
from ingest import get_data_folders
import gc

#from streamlit_chat import message

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)
PERSIST_DIRECTORY = os.environ.get('PERSIST_DIRECTORY')
if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []
    
if "document" not in st.session_state:
    st.session_state["document"] = "not done"



def get_data_files():
    filtered_files = [file for file in listdir(PERSIST_DIRECTORY) if isfile(join(PERSIST_DIRECTORY, file))]
    return filtered_files

qp = None
query = None

st.title("Private Document Assistant")
st.markdown("This application takes any document and indexes it using an embedding making it possible to query and ask questions against any content.")
st.markdown("## Getting started")
st.markdown(" First add a document in the uploaded then you'll be able to query it's contents and have the ML network analyse the results.")
col1, col2 = st.columns([4,3])
st.sidebar.selectbox("Choose index", get_data_folders(PERSIST_DIRECTORY))

@st.cache_resource()
def get_qp():
     qp = QueryProcessor(embeddings=get_embeddings())
     return qp

def on_new_document(document):
    col1.write(document)
def on_query():
    if not get_qp() is None:
        if not query is None:
            result = get_qp().ask(query)
            st.session_state.past.append(query)
            st.session_state.generated.append(result)
            #col2.write(qp.get_documents())
        else:
            st.error("Please enter a question")
    else:
        st.error("Please upload a document first")
# show the status of the index
if does_vectorstore_exist(PERSIST_DIRECTORY):
    col1.success(" Index Database exists")
    qp = get_qp()
    query = col1.text_area("Enter a question", height=28, max_chars=2000)
    col1.button("Ask", on_click=on_query)
else:
    col1.error(" Index Database does not exist")

if not get_qp() is None:
    if not get_qp().get_documents() is None:
        col2.markdown("## Result Documents:")
        for document in get_qp().get_documents():
            col2.write(document)
        
    if not get_qp().get_answser() is None:
        col1.markdown("## Result Answer:")
        col1.write(get_qp().get_answser())

# chat
#if st.session_state["generated"]:
#
#    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
#        message(st.session_state["generated"][i], key=str(i))
#        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")

#st.sidebar.success("Select a demo above.")
#files = get_data_files()
#if len(files) > 0:
#    st.selectbox("Available documents", files)

if st.session_state.get("document") == "done":
    st.markdown(f"Document uploaded succesfull!")


st.sidebar.button("Clear Cache", on_click=get_qp().reset_db)
