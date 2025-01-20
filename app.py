import streamlit as st
import pymongo
import pandas as pd
from urllib.parse import quote_plus
import certifi

# Configuration
def get_database_connection():
    # MongoDB connection details
    username = "admin"
    password = "Welcome#12345W#"
    host = "G33EE83CE279BB9-TATAJSONDB.adb.ap-mumbai-1.oraclecloudapps.com"
    port = "27017"
    
    # Create the connection URI with properly escaped credentials
    uri = f"mongodb://{quote_plus(username)}:{quote_plus(password)}@{host}:{port}/admin?authMechanism=PLAIN&authSource=$external&ssl=true&retryWrites=false&loadBalanced=true"
    
    try:
        # Create a connection using pymongo with SSL configuration
        client = pymongo.MongoClient(
            uri,
            tlsCAFile=certifi.where(),  # Use certifi's SSL certificates
            ssl=True,
            ssl_cert_reqs='CERT_REQUIRED'
        )
        # Test the connection
        client.admin.command('ping')
        return client
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
