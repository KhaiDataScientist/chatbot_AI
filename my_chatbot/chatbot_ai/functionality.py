from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from deep_translator import GoogleTranslator
from langchain.document_loaders import Docx2txtLoader, PyMuPDFLoader

simple_queries = {
    'hello':'Xin chào! Tôi có thể giúp gì cho bạn hôm nay?',
    'chào bạn' : 'Xin chào! Tôi có thể giúp gì cho bạn hôm nay?',
    'xin chào': 'Xin chào! Tôi có thể giúp gì cho bạn hôm nay?',
    'tạm biệt': 'Tạm biệt! Mong được phục vụ bạn lần sau.',
    'cảm ơn': 'Không có gì, rất vui được giúp bạn!',
    'bạn khỏe không?': 'Tôi khỏe, cảm ơn bạn! Bạn thì sao?',
    'tôi cần trợ giúp': 'Tất nhiên, bạn cần hỗ trợ về vấn đề gì?',
    'hôm nay bạn thế nào?': 'Tôi tốt, cảm ơn bạn đã hỏi.',
    'tôi không hiểu': 'Tôi có thể giải thích lại hoặc giúp gì cho bạn?',
    'bạn tên là gì?': 'Tên tôi là Chatbot, rất hân hạnh!',
    'bạn bao nhiêu tuổi?': 'Tôi là một chương trình máy tính nên không có tuổi.',
    'bạn đến từ đâu?': 'Tôi được tạo ra trên internet!',
    'tôi có thể làm gì ở đây?': 'Bạn có thể hỏi tôi bất cứ điều gì bạn muốn biết!',
    'làm thế nào để đăng ký?': 'Tôi có thể hướng dẫn bạn cách đăng ký.',
    'làm thế nào để đăng nhập?': 'Bạn chỉ cần nhập thông tin tài khoản của mình.',
    'tôi quên mật khẩu': 'Đừng lo, tôi có thể giúp bạn lấy lại mật khẩu.',
    'bạn có thể giúp tôi không?': 'Chắc chắn rồi, bạn cần giúp đỡ về điều gì?',
    'tôi muốn đặt câu hỏi': 'Hãy đặt câu hỏi của bạn, tôi ở đây để trả lời.',
    'có ai ở đó không?': 'Có, tôi ở đây để phục vụ bạn.',
    'làm thế nào để hủy?': 'Bạn cần hướng dẫn để hủy dịch vụ nào?',
    'bạn có thể nói Tiếng Việt không?': 'Tất nhiên, tôi có thể giao tiếp bằng Tiếng Việt.',
    'đây là gì?': 'Đây là dịch vụ chatbot, tôi có thể giúp gì cho bạn?',
    'tôi muốn biết thêm thông tin': 'Bạn muốn biết thông tin gì? Tôi sẽ cung cấp cho bạn.',
    'làm thế nào tôi có thể liên hệ với bạn?': 'Bạn có thể để lại tin nhắn ở đây và tôi sẽ phản hồi.',
    'tôi muốn phản hồi': 'Tôi rất mong nhận được phản hồi của bạn!',
    'tôi cần thông tin về': 'Về vấn đề gì bạn cần thông tin? Tôi sẽ giúp bạn.',
    'tôi có thể mua ở đâu?': 'Bạn muốn mua sản phẩm hoặc dịch vụ gì? Tôi có thể tư vấn cho bạn.',
# Additional simple queries for common greetings and questions in Vietnamese
    'chào buổi sáng': 'Chào buổi sáng! Bạn cần tôi giúp đỡ điều gì không?',
    'chào buổi trưa': 'Chào buổi trưa! Bạn có muốn biết về những ưu đãi hôm nay không?',
    'chào buổi tối': 'Chào buổi tối! Tôi có thể giúp bạn thế nào trong tối nay?',
    'chúc ngủ ngon': 'Cảm ơn! Chúc bạn có một giấc ngủ thật ngon.',
    'bạn là ai?': 'Tôi là chatbot được thiết kế để hỗ trợ và trả lời các câu hỏi của bạn.',
    'tôi muốn tìm hiểu': 'Bạn muốn tìm hiểu về chủ đề nào? Tôi sẽ cung cấp thông tin cho bạn.',
    'giờ mấy rồi?': 'Tôi không xem được giờ, nhưng bạn có thể kiểm tra trên thiết bị của mình.',
    'hôm nay thời tiết thế nào?': 'Tôi không thể cập nhật thời tiết, nhưng bạn có thể kiểm tra trên các ứng dụng thời tiết.',
    'bạn có khỏe không?': 'Tôi là chatbot nên luôn "khỏe". Còn bạn thì sao?',
    'có gì mới không?': 'Hôm nay chúng tôi có một số cập nhật thú vị! Bạn muốn nghe về điều gì?',
    'tôi muốn phàn nàn': 'Tôi rất tiếc khi nghe điều đó. Hãy cho tôi biết vấn đề bạn gặp phải.',
    'làm thế nào để thay đổi thông tin cá nhân?': 'Bạn có thể thay đổi thông tin cá nhân trong phần cài đặt tài khoản.',
    'tôi cần đổi mật khẩu': 'Bạn có thể đổi mật khẩu bằng cách vào phần quản lý tài khoản.',
    'bạn có thể giúp tôi học tiếng Việt không?': 'Tôi có thể giới thiệu cho bạn một số nguồn học tiếng Việt.',
    'tôi muốn đặt một cuộc hẹn': 'Bạn muốn đặt cuộc hẹn vào thời gian nào?',
    'tôi có thể đặt câu hỏi ngay bây giờ không?': 'Chắc chắn rồi, hãy đặt câu hỏi của bạn.',
    'bạn có thể hát không?': 'Tôi không thể hát, nhưng tôi có thể giới thiệu cho bạn một số bài hát hay.',
    'bạn có thể đọc thơ không?': 'Tôi có thể chia sẻ với bạn một số bài thơ hay nếu bạn muốn.',
    'bạn có thể kể chuyện cười không?': 'Tôi có một vài mẩu chuyện cười ngắn, bạn muốn nghe không?',
    'bạn có thể đề xuất một quyển sách hay không?': 'Tôi có thể giới thiệu cho bạn một số sách hay theo thể loại bạn thích.',
    'làm thế nào để tiếp tục?': 'Bạn muốn tiếp tục với bước tiếp theo của quy trình nào?',
    'tôi cần thông tin về sản phẩm': 'Bạn muốn biết thông tin về sản phẩm nào? Tôi sẽ cung cấp cho bạn.',
}



def translate_to_english(text):
    translated = GoogleTranslator(source='vietnamese', target='en').translate(text=text)
    return translated


def translate_to_vietnamese(text):
    translated = GoogleTranslator(source='en', target='vietnamese').translate(text=text)
    return translated


def load_document(file):
    """ This function is used to load the text inside the document
     and return the data as a list(text) """

    # print('Loading ', file)
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
    for pattern, response in simple_queries.items():
        if pattern in query.lower().strip():
            return False, response
    return True, None

cache = {}


def augment_prompt(query,vector_store,contain_key=None):
    """Used the augmented prompt to better the response"""
    # Check if query is in the cache or not, if Yes return it
    if query.strip() in cache:
        return cache[query]

    # Get top three most relevant knowlede
    results= vector_store.similarity_search(query,k=3)
    # Get text from the result
    resource_knowledge = '/n'.join([x.page_content for x in results])
    # Feed into the prompt knowledge resources
    augmented_prompt = f""" Additional Knowledge: {resource_knowledge} if necessary. Query: {query} """
    # Store the prompt for the  query
    cache[query] = augmented_prompt
    return augmented_prompt


