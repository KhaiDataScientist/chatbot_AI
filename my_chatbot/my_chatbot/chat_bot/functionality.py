from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from deep_translator import GoogleTranslator
from langchain.document_loaders import Docx2txtLoader, PyMuPDFLoader
from queries import simple_queries


def translate_to_english(text):
    translated = GoogleTranslator(source='vietnamese', target='en').translate(text=text)
    return translated


def translate_to_vietnamese(text):
    translated = GoogleTranslator(source='en', target='vietnamese').translate(text=text)
    return translated


def load_document(file):
    """ This function is used to load the text inside the document
     and return the data as a list(text) """

    print('Loading ', file)
    if 'docx' in file:
        # Create loader
        loader = Docx2txtLoader(file_path=file)

    elif 'pdf' in file:
        # Create loader
        loader = PyMuPDFLoader(file_path=file)

    else:
        return "File not supported"
    data = loader.load()

    return data


def chunk_data(data, chunk_size=256):
    # This function breaks data into chunks for better management and split them into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=0)
    chunks = text_splitter.split_documents(data)
    list_chunks = [chunk.page_content for chunk in chunks]
    return list_chunks


def create_vector_store(index, embeddings):
    """ Create a vector store for working with Vector Database """
    vector_store = Pinecone(index, embeddings.embed_query, "text")
    return vector_store


def insert_data(texts: list[str], embeddings_model, index_name, **kwargs):  # Use namespace if you have money
    """Use to insert data to the vector database with namespace"""

    store = Pinecone.from_texts(
        texts,
        embeddings_model,
        index_name=index_name,
    )

    return None


def should_augment_prompt(query):
    """ Used to check whether to use augmented prompt or not"""
    if 'test' in query.lower().strip():
        return 'bai_test', None
    for pattern, response in simple_queries.items():
        if pattern in query.lower():
            return None, response
    return None, None


cache = {}


def augment_prompt(query, vector_store, contain_key=None):
    """Used the augmented prompt to better the response"""
    # Check if query is in the cache or not, if Yes return it
    if query.strip() in cache:
        return cache[query]
    if contain_key:
        results = vector_store.similarity_search(query, k=7)
        augmented_prompt = f'Bài test {translate_to_vietnamese(results)}, sử dụng nó để test cho người dùng,sau khi người dùng làm xong thì tính tổng điểm và đưa kết quả cho họ.Nhớ là hỏi một cách tự nhiên, đừng có máy móc'
    else:
        # Get top three most relevant knowlede
        results = vector_store.similarity_search(query, k=3)

        # Get text from the result
        resource_knowledge = '/n'.join([x.page_content for x in results])
        # Feed into the prompt knowledge resources
        augmented_prompt = f""" Additional Knowledge: {resource_knowledge} if necessary. Query: {query} """
    # Store the prompt for the  query
    cache[query] = augmented_prompt
    return augmented_prompt

def recognize_test(query):

    pass
