from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.llms import  HuggingFacePipeline
from transformers import pipeline
import bs4

loader = WebBaseLoader(
    web_paths=["https://en.wikipedia.org/wiki/OpenAI"],
    bs_kwargs=dict(parse_only=bs4.SoupStrainer())
)

text_documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=20)
documents = text_splitter.split_documents(text_documents)

embedding_model = SentenceTransformerEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

db = Chroma.from_documents(documents, embedding_model)


generator = pipeline("text-generation", model="google/flan-t5-base", max_new_tokens=200)
llm = HuggingFacePipeline(pipeline=generator)

query = "Who is founder of OpenAI?"
retrieved_docs = db.similarity_search(query)

context = retrieved_docs[0].page_content if retrieved_docs else "No relevant content found."
prompt = f"Based on the following context, answer the question. and give me only relevant ans\n\nContext: {context}\n\nQuestion: {query}\nAnswer:"

response = llm.invoke(prompt)

print(response)
