import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from loguru import logger

class DocumentProcessor:
    def __init__(self, chroma_db_directory: str, embedding_model_name: str):
        self.chroma_db_directory = chroma_db_directory
        self.embedding_model_name = embedding_model_name

        # Initialize embeddings once for the processor instance
        self.embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model_name)

        # Ensure ChromaDB directory exists. Chroma will create it if not, but explicit is fine.
        os.makedirs(self.chroma_db_directory, exist_ok=True)

        # Initialize ChromaDB here. If the directory exists, it will load it.
        # If it doesn't, a new empty collection is implicitly managed until add_documents is called.
        self.vectorstore = Chroma(
            persist_directory=self.chroma_db_directory,
            embedding_function=self.embeddings
        )
        logger.info(f"DocumentProcessor initialized. ChromaDB at '{self.chroma_db_directory}', "
                    f"Embedding model: '{self.embedding_model_name}'.")

    def process_and_store_document(self, file_path: str) -> int:
        """
        Loads a document, splits it, generates embeddings, and stores them in ChromaDB.
        Assumes file_path points to a locally accessible file.
        
        Args:
            file_path (str): The local path to the document file.

        Returns:
            int: The number of chunks processed and stored.

        Raises:
            FileNotFoundError: If the document file does not exist.
            Exception: For any other errors during document processing.
        """
        if not os.path.exists(file_path):
            logger.error(f"Document file not found at: {file_path}")
            raise FileNotFoundError(f"Document file not found: {file_path}")

        try:
            # 1. Load the document
            logger.info(f"Attempting to load document: {file_path}")
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            logger.info(f"Successfully loaded {len(documents)} pages from {file_path}")

            # 2. Split the document into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
                add_start_index=True,
            )
            chunks = text_splitter.split_documents(documents)
            logger.info(f"Split document into {len(chunks)} chunks.")

            # 3. Store chunks in ChromaDB
            # Add documents to the pre-initialized vectorstore instance
            self.vectorstore.add_documents(chunks)

            logger.info(f"Added {len(chunks)} chunks to ChromaDB.")

            return len(chunks) # Return count of chunks for confirmation

        except Exception as e:
            logger.error(f"Error processing document '{file_path}': {e}", exc_info=True)
            # Re-raise the exception for the caller (FastAPI endpoint) to handle
            raise
