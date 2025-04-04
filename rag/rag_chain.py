import asyncio
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from huggingface_hub import login  # type: ignore

# access_token_read = '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'
# access_token_write = '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'
access_token_read = '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'
access_token_write = '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'
login(token=access_token_read)

async def rag_chain():
    model = ChatOllama(model="llama3")

    prompt = PromptTemplate.from_template(
        """
        <s> [Instructions] You are a classifier model.
        Based on the following question, determine the category it belongs to from the list: "благоустройство", "образование", "молодежная политика", "социальные вопросы", "здравоохранение".
        Structure your response in the following format:
        [Only category from the list in lower: "благоустройство", "образование", "молодежная политика", "социальные вопросы", "здравоохранение"]
        If you cannot determine the category, reply with "unknown"." [/Instructions] </s>
        [Instructions] Question: {input}
        Context: {context}
        Answer: [/Instructions]
        """
    )

    # Загрузка векторной БД
    embedding = FastEmbedEmbeddings()
    vector_store = Chroma(persist_directory="rag/sql_chroma_db", embedding_function=embedding)

    # Создание цепи
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": 3,
            "score_threshold": 0.5,
        },
    )

    document_chain = create_stuff_documents_chain(model, prompt)
    chain = create_retrieval_chain(retriever, document_chain)

    return chain

async def ask(query: str):
    chain = await rag_chain()
    # invoke chain
    result = await chain.ainvoke({"input": query})
    return result["answer"]

async def main():
    while True:
        user_input = input("Введите ваш вопрос (или 'stop' для выхода): ")
        if user_input.lower() == 'stop':
            print("Завершение работы.")
            break
        print(await ask(user_input))

if __name__ == '__main__':
    asyncio.run(main())
