import streamlit as st
import os
from os.path import isfile, join
from os import listdir
from ingest import delete_vectorstore, does_vectorstore_exist, \
      PERSIST_DIRECTORY,  \
    get_data_folders, get_source_files, SOURCE_DIRECTORY

st.set_page_config(
    page_title="Manage Indexes",
    page_icon="🧊",
)
st.title("Manage Indexes")
col1, col2 = st.columns([4,3])
def create_index_folder(dir, name):
    if not os.path.exists(dir):
        os.makedirs(dir)  
    if not os.path.exists(dir + name):
        os.makedirs(dir + name)
# Indexes

col1.markdown("## Index Folders")
data_folders = get_data_folders(PERSIST_DIRECTORY)

if data_folders:
    col1.success(f" {len(data_folders)} Index Folder(s) exists")
    sel_index = col1.selectbox("Choose index", data_folders)
    #st.button("Delete Index", on_click=lambda: delete_vectorstore(PERSIST_DIRECTORY))
else:
    col2.error(" No index folders exist")
    col2.text("Please create an index")
col2.markdown("## Index Actions")
index_name = col2.text_input("Index name")
col2.button("Create Index", on_click=lambda: create_index_folder(PERSIST_DIRECTORY, index_name) )
col2.divider()

col1.divider()
# Source Files
col1.markdown("## Source Files")
source_files = get_source_files(SOURCE_DIRECTORY)
if source_files:
    col1.success(f" {len(source_files)} Source File(s) exists")
    sel_source = col1.multiselect("Choose source", source_files)
# Source Actions
col2.markdown("## Source Actions")
uploaded_doc = col2.file_uploader("Upload a file", type=["pdf", "md", "txt", "zip"])
if uploaded_doc:
    with open(SOURCE_DIRECTORY + uploaded_doc.name, "wb") as f:
        bytes_data = uploaded_doc.read()
        f.write(bytes_data)
    col2.success("File uploaded")
    