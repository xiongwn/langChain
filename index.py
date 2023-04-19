import os
os.environ["OPENAI_API_KEY"] = "sk-"

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI,VectorDBQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.chains import RetrievalQA

# 加载文件夹中的所有txt类型的文件
loader = DirectoryLoader('./doc/', glob='**/*.txt')
# 将数据转成 document 对象，每个文件会作为一个 document
documents = loader.load()
print(f'documents:{len(documents)}')
# 初始化加载器
text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=0)
# 切割加载的 document
split_docs = text_splitter.split_documents(documents)

# 初始化 openai 的 embeddings 对象
embeddings = OpenAIEmbeddings()

# 将 document 通过 openai 的 embeddings 对象计算 embedding 向量信息并临时存入 Chroma 向量数据库，用于后续匹配查询
print(f'documents:{len(split_docs)}')
docsearch = Chroma.from_documents(split_docs, embeddings, persist_directory="G:/code/langchain/vector")
docsearch.persist()
# docsearch = Chroma(persist_directory="G:/code/langchain/vector", embedding_function=embeddings)

# 创建问答对象
# qa = VectorDBQA.from_chain_type(llm=OpenAI(temperature=0), chain_type="stuff", vectorstore=docsearch,return_source_documents=True,verbose=True)
qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(temperature=0), chain_type="map_reduce", retriever=docsearch.as_retriever(),verbose=True)
# 进行问答
result = qa({"query": "总结4月12日east的突破"})
print(result["result"])

# docsearch.delete_collection()
# docsearch.persist()
