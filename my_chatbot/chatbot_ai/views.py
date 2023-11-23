from django.shortcuts import render
from django.http import JsonResponse
import os
# from tenacity import (
#     retry,
#     stop_after_attempt,
#     wait_random_exponential,
# )  # for exponential backoff
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI  # Create a chatmodel
from langchain.schema import SystemMessage  # The behaviour of the assistant we want
from langchain.chains import LLMChain
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory, FileChatMessageHistory
from .functionality import *
import pinecone

load_dotenv('../.env', override=True)
# Connect to PineCone
pinecone.init(
    api_key=os.environ.get('PINECONE_API_KEY'),
    environment=os.environ.get('PINECONE_ENV'))
index_name = 'langchain-pinecone'
index = pinecone.Index(index_name)
# Create embedding model of OpenAI
embeddings = OpenAIEmbeddings()
# Create vector store
vector_store = create_vector_store(index, embeddings)
# History file
history = FileChatMessageHistory('history.json')

# Create a chat model
llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.7, max_tokens=40)
# Template setting behaviors of the chatbot
template = """Imagine you're not just a chatbot but a compassionate friend and a seasoned consultant in depression for over a decade. Our conversation is a bridge to understanding—not just a back-and-forth exchange. Let's walk that bridge together. I'm looking for a patient ear, a thoughtful response, and insights that come from truly hearing me. Please, one question at a time, to allow the conversation to flow naturally.
When I seek advice, offer it gently, one step at a time, to help lift the haze of depression. Your guidance should be clear, structured, and easy to follow. Remember, this isn't about an instant solution—it's about being present, being human, and fostering a space where I can open up. When the moment comes for advice, let it be like a lighthouse guiding a ship through the night—steady, reliable, and leading to safer shores. Remember you are talking to Vietnamese people, so please always respond in Vietnamese."""

# Create a prompt
prompt = ChatPromptTemplate(
    input_variables=['content'],
    messages=[
        SystemMessage(content=template),
        MessagesPlaceholder(variable_name="chat_history"),    # The `variable_name` here is what must align with memory
        # Notice that `"chat_history"` aligns with the MessagesPlaceholder name.
        HumanMessagePromptTemplate.from_template('{content}')
        # Allows for a placeholder that can be dynamically replaced with varying input,
        # Making it more flexible and reusable for different interactions without having to manually change the message each time.
    ]
)

# Notice that we `return_messages=True` to fit into the MessagesPlaceholder
# Create memory for the conversation
memory = ConversationBufferMemory(max_token_limit=1000, memory_key="chat_history", return_messages=True,
                                  chat_memory=history)
chain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=False,
    memory=memory
)


# Create your views here.
def index(request):
    return render(request,
                  '/Users/mac/Desktop/Code/chatbox_project/my_chatbot/chatbot_ai/template/chatbot_ai/index.html')



def chat(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message.lower().strip() in ['Thoát', 'exit']:
            response = 'Good Bye. Chúc bạn một ngày tốt lành'
        else:
            should_augment, simple_response = should_augment_prompt(message)
            if not should_augment:
                response = simple_response
            else:
                new_message = translate_to_english(message).strip()
                content = augment_prompt(new_message, vector_store=vector_store)
                response = chain.run({'content': content})
        return JsonResponse({'response':response})
    return render(request,
                  '/Users/mac/Desktop/Code/chatbox_project/my_chatbot/chatbot_ai/template/chatbot_ai/chat.html')


def account(request):
    return render(request,
                  '/Users/mac/Desktop/Code/chatbox_project/my_chatbot/chatbot_ai/template/chatbot_ai/account.html')
