from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import UnstructuredURLLoader, SeleniumURLLoader
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
import os
import json

os.environ["OPENAI_API_KEY"] = "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"

class RequestHandler(BaseHTTPRequestHandler):
    def send_json_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response_body = json.dumps(data)
        self.wfile.write(response_body.encode('utf-8'))

    def do_POST(self):
        # 获取 POST 请求中的数据
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = json.loads(post_data)
        
        if not ('uid' in params):
            self.send_json_response(400, {'error': 'Bad Request: uid null'})
            return
        if (type(params['uid']) != str):
            self.send_json_response(400, {'error': 'Bad Request: uid type err'})
            return
        if (not 'urls' in params or type(params['urls']) != list):
            self.send_json_response(400, {'error': 'Bad Request: urls type err'})
            return
        if (len(params['urls']) == 0):
            self.send_json_response(400, {'error': 'Bad Request: urls empty'})
            return

        loader = SeleniumURLLoader(urls=params['urls'])
        # 将数据转成 document 对象，每个文件会作为一个 document
        documents = loader.load()
        print(f'documents:{len(documents)}')
        print(documents)
        # 初始化加载器
        text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
        # 切割加载的 document
        split_docs = text_splitter.split_documents(documents)
        # 初始化 openai 的 embeddings 对象
        embeddings = OpenAIEmbeddings()

        print(f'documents:{len(split_docs)}')
        # llm
        llm = ChatOpenAI(temperature=0)
        docsearch = Chroma.from_documents(split_docs, embeddings, persist_directory="G:/code/langchain/vector/"+params['uid'])
        docsearch.persist()
        # docsearch = Chroma(persist_directory="G:/code/langchain/vector/"+params['uid'], embedding_function=embeddings)
        qa = RetrievalQA.from_chain_type(llm, chain_type="map_reduce", retriever=docsearch.as_retriever(),verbose=True)
        # 进行问答
        result = qa({"query": "总结4月12日east的突破"})
        print(result["result"])
        data = {"test": 1}

        # 返回响应
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), RequestHandler)
    print('开始监听 8000 端口...')
    server.serve_forever()