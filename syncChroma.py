import chromadb
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

LOCAL_CHROMA_PATH = os.path.join(os.getcwd(), "chromadb")
REMOTE_CHROMA_URL = os.getenv("REMOTE_CHROMA_URL")
API_KEY = os.getenv("REMOTE_CHROMA_API_KEY")

def sync_chroma():
    local_client = chromadb.PersistentClient(path=LOCAL_CHROMA_PATH)
    
    # Fetch remote collections
    response = requests.get(f"{REMOTE_CHROMA_URL}/collections", headers={"Authorization": f"Bearer {API_KEY}"})
    remote_collections = response.json()

    for collection in remote_collections:
        collection_name = collection['name']
        
        # Check if collection exists locally
        if collection_name not in local_client.list_collections():
            local_client.create_collection(name=collection_name)
        
        local_collection = local_client.get_collection(name=collection_name)
        
        # Fetch remote collection data
        response = requests.get(f"{REMOTE_CHROMA_URL}/collections/{collection_name}/data", 
                                headers={"Authorization": f"Bearer {API_KEY}"})
        remote_data = response.json()
        
        # Update local collection
        local_collection.add(
            ids=remote_data['ids'],
            embeddings=remote_data['embeddings'],
            metadatas=remote_data['metadatas'],
            documents=remote_data['documents']
        )
        
        print(f"Synced collection: {collection_name}")

    print("ChromaDB sync completed")

def push_to_remote():
    local_client = chromadb.PersistentClient(path=LOCAL_CHROMA_PATH)
    
    for collection_name in local_client.list_collections():
        local_collection = local_client.get_collection(name=collection_name)
        local_data = local_collection.get()
        
        # Push to remote
        response = requests.post(
            f"{REMOTE_CHROMA_URL}/collections/{collection_name}/data",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json=local_data
        )
        
        if response.status_code == 200:
            print(f"Successfully pushed collection {collection_name} to remote")
        else:
            print(f"Failed to push collection {collection_name}. Status code: {response.status_code}")

if __name__ == "__main__":
    action = input("Enter 'sync' to pull from remote or 'push' to update remote: ").lower()
    if action == 'sync':
        sync_chroma()
    elif action == 'push':
        push_to_remote()
    else:
        print("Invalid action. Please enter 'sync' or 'push'.")