from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import sys
from huggingface_hub import login  # type: ignore


access_token_read = "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"
access_token_write = "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"
login(token = access_token_read)

def rag_chain():
    model = ChatOllama(model="llama3")
    #
    prompt = PromptTemplate.from_template(
        """
        <s> [Instructions] You are a friendly assistant. Answer the question based only on the following context.
        If you don't know the answer, then reply, No Context availabel for this question {input}. [/Instructions] </s>
        [Instructions] Question: {input}
        Context: {context}
        Answer: [/Instructions]
        """
    )
    #Load vector store
    embedding = FastEmbedEmbeddings()
    vector_store = Chroma(persist_directory="rag/sql_chroma_db", embedding_function=embedding)

    #Create chain
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": 3,
            "score_threshold": 0.5,
        },
    )

    document_chain = create_stuff_documents_chain(model, prompt)
    chain = create_retrieval_chain(retriever, document_chain)
    #
    return chain


def ask(query: str):
    #
    chain = rag_chain()
    # invoke chain
    result = chain.invoke({"input": query})
    # print results
    print(result["answer"])
    for doc in result["context"]:
        print("Source: ", doc.metadata["source"])

# ask("Какая тема работы Сбитнева?")

# ask("Меня зовут Семен")

# ask("Как меня зовут?")