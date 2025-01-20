import streamlit as st
import pymongo
import pandas as pd

# Configuration
def get_database_connection():
    # MongoDB connection details
    username = "admin"
    password = "Welcome#12345W#"
    host = "129.154.246.136"  # Direct IP address
    port = 27017
    
    try:
        # Create a MongoClient with the direct IP connection
        client = pymongo.MongoClient(
            host=host,
            port=port,
            username=username,
            password=password,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000
        )
        
        # Test the connection
        client.admin.command('ping')
        return client
        
    except pymongo.errors.ServerSelectionTimeoutError as e:
        st.error(f"Timeout error: {str(e)}")
        return None
    except pymongo.errors.ConnectionFailure as e:
        st.error(f"Connection error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Error connecting to database: {str(e)}")
        return None

# Streamlit app
def main():
    st.title("MongoDB Data Viewer")
    
    try:
        # Connect to MongoDB
        client = get_database_connection()
        
        if client:
            # Get list of databases
            databases = client.list_database_names()
            
            # Database selector
            selected_db = st.selectbox("Select Database", databases)
            
            if selected_db:
                db = client[selected_db]
                # Get list of collections
                collections = db.list_collection_names()
                
                # Collection selector
                selected_collection = st.selectbox("Select Collection", collections)
                
                if selected_collection:
                    collection = db[selected_collection]
                    
                    # Get the first few documents
                    docs = list(collection.find().limit(5))
                    
                    if docs:
                        # Convert to DataFrame
                        df = pd.DataFrame(docs)
                        
                        # Display the data
                        st.subheader(f"First 5 records from {selected_collection}")
                        st.dataframe(df)
                    else:
                        st.info("No documents found in this collection.")
            
            # Close the connection
            client.close()
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
