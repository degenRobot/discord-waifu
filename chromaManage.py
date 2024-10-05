import chromadb
import os
chroma_db_path = os.path.join(os.getcwd(), "chromadb")
chroma = chromadb.PersistentClient(path=chroma_db_path)

client = chromadb.PersistentClient(path=chroma_db_path)

deleteCollection = "Rise"

client.delete_collection(deleteCollection)