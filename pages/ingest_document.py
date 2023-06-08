from privateGPT import QueryProcessor
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
from ingest import LOADER_MAPPING, \
    does_vectorstore_exist, \
    PERSIST_DIRECTORY, \
    SOURCE_DIRECTORY, index, \
    get_embeddings
from os.path import isfile, join
from os import listdir

@st.cache_resource()
def get_qp():
     qp = QueryProcessor(embeddings=get_embeddings())
     return qp

def get_data_files():
    filtered_files = [file for file in listdir(SOURCE_DIRECTORY) if isfile(join(SOURCE_DIRECTORY, file))]
    return filtered_files

if "document" not in st.session_state:
    st.session_state["document"] = "not done"

@st.cache_resource()
def embeddings():
    return get_embeddings()

def on_delete():
    if avail_docs:
        for document in avail_docs:
            os.remove(SOURCE_DIRECTORY + document)
        st.write(f"Deleted document(s) {avail_docs}")
def on_index():
    if avail_docs:
        index(embeddings(), get_qp().db)
        st.write(f"Indexing document {avail_docs}")
        for document in avail_docs:
            os.remove(SOURCE_DIRECTORY + document)
        st.write(f"Deleted document(s) {avail_docs}")

# title, indroduction
st.title("Private Document Assistant")
st.markdown("Indexes pdfs making them searchable.")
col1, col2, col3 = st.columns([2,1,3])

# show the status of the index
if does_vectorstore_exist(PERSIST_DIRECTORY):
    col1.success(" Index Database exists")
else:
    col1.error(" Index Database does not exist")

def update_available():
    avail_docs = col1.multiselect("Available documents", get_data_files())
    st.session_state["avail_docs"] = avail_docs
    return avail_docs
# document uploader
col3.markdown(" ### Document Uploader")
uploaded_pdf = col3.file_uploader("Upload a PDF file", type="pdf")


#st.selectbox("Available doc types", LOADER_MAPPING.keys() )
if uploaded_pdf is not None:
    st.write("filename:", uploaded_pdf.name)
    with open(SOURCE_DIRECTORY + uploaded_pdf.name, "wb") as f:
        bytes_data = uploaded_pdf.read()
        f.write(bytes_data)

    #st.session_state["document"] = "done"
avail_docs = update_available()
if len(avail_docs) > 0:
    col1.button("Index document(s)", on_click=on_index)
    col1.button("Delete document(s)", on_click=on_delete)
