import data_loader
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings, SentenceTransformerEmbeddings

# This program stores the data as a vector to then be used by the chatbot. It is stored in hard drive so as to not have to do this process each time the main program restarts

model_name = "sentence-transformers/all-mpnet-base-v2"
hf = HuggingFaceEmbeddings(model_name=model_name)

# Supplying a persist_directory will store the embeddings on disk
persist_directory = 'db'

def create_vectordb():
    # Getting URLs from data_loader
    urls = ['https://brainlox.com/courses/category/technical'] #data_loader.get_urls()

    # Creating Embeddings and storing as vector using 
    loaders = UnstructuredURLLoader(urls=urls)
    data = loaders.load()

    # Splitting text by word count
    text_splitter = CharacterTextSplitter(separator='\n', 
                                        chunk_size=500,
                                        chunk_overlap=60)
    docs = text_splitter.split_documents(data)

    vectordb = Chroma.from_documents(documents=docs, 
                                    embedding=hf,
                                    persist_directory=persist_directory)

    #saving the created vector db
    vectordb.persist()