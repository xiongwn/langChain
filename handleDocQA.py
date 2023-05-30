from http.server import BaseHTTPRequestHandler, HTTPServer
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import DirectoryLoader
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
import os
import json
import requests

BASE_DIR = 'G'
# os.environ["OPENAI_API_KEY"] = "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"

def handleDoc(self):
    try:
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = json.loads(post_data)
    except Exception as e:
        # 捕获并处理所有异常
        print("错误信息：", e)
        self.send_json_response(501, {'error': self.headers}) 
        return
    
    # 参数校验
    if not ('key' in params):
        self.send_json_response(403, {'error': 'Bad Request: key null'})
        return
    if (type(params['key']) != str):
        self.send_json_response(403, {'error': 'Bad Request: key type err'})
        return
    if not ('comment' in params):
        self.send_json_response(403, {'error': 'Bad Request: comment null'})
        return
    if (type(params['comment']) != str):
        self.send_json_response(403, {'error': 'Bad Request: comment type err'})
        return
    if not ('uid' in params):
        self.send_json_response(403, {'error': 'Bad Request: uid null'})
        return
    if (type(params['uid']) != str):
        self.send_json_response(403, {'error': 'Bad Request: uid type err'})
        return
    if (not 'urls' in params or type(params['urls']) != list):
        self.send_json_response(403, {'error': 'Bad Request: urls type err'})
        return
    if (len(params['urls']) == 0):
        self.send_json_response(403, {'error': 'Bad Request: urls empty'})
        return

    os.environ["OPENAI_API_KEY"] = params['key']
    try :
        save_directory = os.path.join("doc", params['uid'])
        # 检查路径
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        directory = "doc/" + params['uid'] # 目录路径
        # 获取现有文件列表
        webDocNameList = [x.split("/")[-1].split("?")[0] for x in params['urls']]
        file_names = os.listdir(directory)
        createNewSplitter = 0
        # print(file_names)
        # print(webDocNameList)
        for url in webDocNameList:
            if url not in file_names:
                createNewSplitter = 1
        print("createNewSplitter", createNewSplitter)
        
        
        # 下载文件
        if createNewSplitter == 1:
            for url in params['urls']:
                response = requests.get(url)
                if response.status_code == 200:
                    file_name = url.split("/")[-1].split("?")[0]  # 提取文件名
                    save_path = os.path.join(save_directory, file_name)
                    with open(save_path, "wb") as file:
                        file.write(response.content)
                    print(f"文件 {file_name} 下载完成，保存路径：{save_path}")
                else:
                    print(f"下载 {url} 失败")
                    self.send_json_response(401, {'error': f"下载 {url} 失败"})
                    return
            print("批量下载完成")
        
        # loader = SeleniumURLLoader(urls=params['urls'])
        loader = DirectoryLoader('./doc/', glob = params['uid'] + '/*.txt')
        # 将数据转成 document 对象，每个文件会作为一个 document
        documents = loader.load()
        print(f'documents:{len(documents)}')
        # print(documents)
        # 初始化加载器
        text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=0)
        # 切割加载的 document
        split_docs = text_splitter.split_documents(documents)
        # 初始化 openai 的 embeddings 对象
        embeddings = OpenAIEmbeddings()

        print(f'documents:{len(split_docs)}')

        # llm
        llm = ChatOpenAI(temperature=0)
        
        if createNewSplitter == 1:
            docsearch = Chroma.from_documents(split_docs, embeddings, persist_directory=BASE_DIR+":/code/langchain/vector/"+params['uid'])
            docsearch.persist()
        else :
            docsearch = Chroma(persist_directory=BASE_DIR+":/code/langchain/vector/"+params['uid'], embedding_function=embeddings)
        qa = RetrievalQA.from_chain_type(llm, chain_type="map_reduce", retriever=docsearch.as_retriever(),verbose=True)
        # 进行问答
        result = qa({"query": params["comment"]})
        content = result["result"]
        print(content)
        data = {"result": content}

        # 返回响应
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    except Exception as e:
        # 捕获并处理所有异常
        print("错误信息：", e)
        self.send_json_response(501, {'error': "check your request"})
    
def handleTools(self):
    def postToolApi(paramString, url):
        response = requests.post(url = url, data = {"params": paramString}).json()
        return response
    try:
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = json.loads(post_data)
    except Exception as e:
        # 捕获并处理所有异常
        print("错误信息：", e)
        self.send_json_response(501, {'error': "bad request"}) 
        return
    
    # 参数校验
    if not ('key' in params):
        self.send_json_response(403, {'error': 'Bad Request: key null'})
        return
    if (type(params['key']) != str):
        self.send_json_response(403, {'error': 'Bad Request: key type err'})
        return
    if not ('comment' in params):
        self.send_json_response(403, {'error': 'Bad Request: comment null'})
        return
    if (type(params['comment']) != str):
        self.send_json_response(403, {'error': 'Bad Request: comment type err'})
        return
    if (not 'tools' in params or type(params['tools']) != list):
        self.send_json_response(403, {'error': 'Bad Request: tools type err'})
        return
    if (len(params['tools']) == 0):
        self.send_json_response(403, {'error': 'Bad Request: tools empty'})
        return

    os.environ["OPENAI_API_KEY"] = params['key']
    try :
        llm = ChatOpenAI(temperature=0)
        # llm = Cohere()
        # llm = HuggingFaceHub(repo_id="google/flan-t5-xl", model_kwargs={"temperature":0, "max_length":64})
        
        tools = []
        for obj in params['tools']: 
            if obj["toolType"] == 1:
                func = postToolApi(obj["paramString"], obj["url"])
            else:
                func = lambda x: obj["content"]
            tool = Tool(
            name=obj["title"],
            func=func, #Mock Function
            description=obj["description"],
            )
            tools.append(tool)
        
        # agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        agent = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)
        # agent.run("what is the most famous song of christmas")
        result = agent.run(input=params['comment'])

        
        print(result)
        data = {"result": result}

        # 返回响应
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    except Exception as e:
        # 捕获并处理所有异常
        print("错误信息：", e)
        self.send_json_response(501, {'error': "bad request"})
    

class RequestHandler(BaseHTTPRequestHandler):
    def send_json_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response_body = json.dumps(data)
        self.wfile.write(response_body.encode('utf-8'))

    def do_POST(self):
        if self.path == "/handleDoc":
            handleDoc(self)
        elif self.path == "/handleTools":
            handleTools(self)
        else:
            self.send_json_response(404, {'error': 'path not found'})

    def do_GET(self):
        self.send_response(403)
        self.end_headers()
        self.wfile.write(b'fuck you son of bitch, do you wanna get this mother fucker')
        # self.send_json_response(403, {'error': 'fuck you son of bitch, do you wanna get this mother fucker'})
        

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 3000), RequestHandler)
    print('开始监听 3000 端口...')
    server.serve_forever()

