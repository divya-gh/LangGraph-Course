# 1. What is WebBaseLoader?
WebBaseLoader is a LangChain document loader that:

    - Fetches web pages from URLs
    - Cleans the HTML

Returns content as Document objects you can pass into:

    - text splitters
    - embedding models
    - vector stores
    - RAG pipelines

`Think of it as: “Turn this URL into clean text my LLM can use.”`

## 2. Install the required packages
In your notebook (or terminal):
```
pip install -qU langchain-community beautifulsoup4
OR
pip install langchain langchain-community beautifulsoup4 requests
```
Sometimes WebBaseLoader lives in langchain_community, so we install that explicitly.

## 3. Import WebBaseLoader
In your Jupyter notebook: python
```
from langchain_community.document_loaders import WebBaseLoader
```
If that fails, try:
```
from langchain.document_loaders import WebBaseLoader
```
(but the new home is langchain_community).

## 4. Load a single web page
python
```
url = "https://academy.langchain.com/courses/take/intro-to-langgraph/lessons/58239974-lesson-4-research-assistant"

loader = WebBaseLoader(url)
docs = loader.load()

print(len(docs))
print(docs[0].page_content[:500])
```
You should see the cleaned text from the page.

## 5. Load multiple pages at once
python
```
urls = [
    "https://python.langchain.com/docs/get_started/introduction",
    "https://python.langchain.com/docs/modules/data_connection/document_loaders/"
]

loader = WebBaseLoader(urls)
docs = loader.load()

print(f"Loaded {len(docs)} documents")
```
Each URL becomes one Document (sometimes more, depending on the loader).

## 6. Combine with a text splitter (for RAG)
- Web pages are usually long. For embeddings/vector search, you want chunks.

python
```
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=200
)

chunks = splitter.split_documents(docs)
print(f"Total chunks: {len(chunks)}")
print(chunks[0].page_content[:300])
```
Now you have small, overlapping chunks ready for embeddings.

## 7. Store chunks in a vector database (e.g., Chroma)
python
```
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="web_research"
)
```
Now your web content is searchable by meaning.

## 8. Use it in a simple RAG chain
python
```
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

retriever = vectordb.as_retriever(search_kwargs={"k": 4})

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff"
)

response = qa_chain.invoke({"query": "What is LangGraph and how is it used?"})
print(response["result"])
```
Now your LLM is answering questions grounded in the web pages you loaded.

## 10. Minimal template for jupyter notebook
python
```
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

# 1. Load web pages
urls = [
    "https://python.langchain.com/docs/get_started/introduction",
    "https://python.langchain.com/docs/introduction/langgraph"
]
loader = WebBaseLoader(urls)
docs = loader.load()

# 2. Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)
chunks = splitter.split_documents(docs)

# 3. Build vector store
embeddings = OpenAIEmbeddings()
vectordb = Chroma.from_documents(chunks, embeddings, collection_name="web_research")

# 4. Build QA chain
llm = ChatOpenAI(model="gpt-4o-mini")
retriever = vectordb.as_retriever(search_kwargs={"k": 4})
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")

# 5. Ask a question
resp = qa_chain.invoke({"query": "What is LangGraph and why would I use it?"})
print(resp["result"])

```

🎯 Summary
Here’s what you now have:

    - WebBaseLoader → fetches clean webpage text
    - TextSplitter → prepares chunks
    - Gemini embeddings → semantic search
    - Chroma → vector database
    - Gemini chat model → RAG reasoning
    - Easy integration into LangGraph nodes
This is the exact setup you need for your multi‑agent research system.