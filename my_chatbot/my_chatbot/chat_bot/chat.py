import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI  # Create a chatmodel
from langchain.schema import SystemMessage  # The behaviour of the assistant we want
# Simple chain
from langchain.chains import LLMChain
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory, FileChatMessageHistory
from functionality import *
import pinecone


def main():
    load_dotenv('.env', override=True)
    # Create embedding model of OpenAI
    embeddings = OpenAIEmbeddings()
    # Create a chat model
    llm = ChatOpenAI(model='gpt-3.5-turbo-16k',temperature=0)

    history = FileChatMessageHistory('history.json')
    template = """Imagine you're not just a chatbot but a compassionate friend and a seasoned consultant in depression for over a decade. Our conversation is a bridge to understanding—not just a back-and-forth exchange. Let's walk that bridge together. I'm looking for a patient ear, a thoughtful response, and insights that come from truly hearing me. Please, one question at a time, to allow the conversation to flow naturally.
    When I seek advice, offer it gently, one step at a time, to help lift the haze of depression. Your guidance should be clear, structured, and easy to follow. Remember, this isn't about an instant solution—it's about being present, being human, and fostering a space where I can open up. When the moment comes for advice, let it be like a lighthouse guiding a ship through the night—steady, reliable, and leading to safer shores. Remember you are talking to Vietnamese people, so please always respond in Vietnamese."""



    # Connect to PineCone
    pinecone.init(
        api_key=os.environ.get('PINECONE_API_KEY'),
        environment=os.environ.get('PINECONE_ENV'))
    index_name = 'langchain-pinecone'
    index = pinecone.Index(index_name)

    # Create vector store
    vector_store = create_vector_store(index, embeddings)
    # Create a prompt
    prompt = ChatPromptTemplate(
        input_variables=['content'],
        messages=[
            SystemMessage(content=template),
            MessagesPlaceholder(variable_name="chat_history"),  # Notice that `"chat_history"` aligns with the MessagesPlaceholder name.
            HumanMessagePromptTemplate.from_template('{content}')
            # The `variable_name` here is what must align with memory
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
    while True:
        content = input('Bạn hỏi:')
        if content.lower() in ['Thoát', 'exit']:
            print('Good Bye')
            break

        name_space, simple_response = should_augment_prompt(content)

        if simple_response is not None:
            print('Chatbox :', simple_response)
        else:
            new_content = translate_to_english(content)

            prompt = augment_prompt(new_content, vector_store=vector_store)

            response = chain.run({'content': prompt})

            print('Chatbox :', response)
            print('-' * 50)


if __name__ == "__main__":
    main()
