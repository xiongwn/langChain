官方文档 [https://python.langchain.com/en/latest/](https://python.langchain.com/en/latest/)

基础知识库中文版（重要） [https://github.com/liaokongVFX/LangChain-Chinese-Getting-Started-Guide](https://github.com/liaokongVFX/LangChain-Chinese-Getting-Started-Guide)

代码 [https://github.com/xiongwn/langChain](https://github.com/xiongwn/langChain)

据说有隐患但是我没复现 [https://twitter.com/rharang/status/1641899743608463365](https://twitter.com/rharang/status/1641899743608463365)

# 怎么构建知识库

利用langchain提供的loader加载资源

将loader进行document解析

如果document过大则需要使用spliter对document进行分割

分割后利用embeding将每个片段的文档向量化，这个过程是llm负责的

向量化后利用向量数据库存储向量以便二次使用

远程调用llm进行知识库问答

# 怎么做知识库累加

只要向量存储在同一目录下，且之前的向量没有被删除。这时候可以删除之前训练的文档，添加新的文档，新文档向量化后，可以回答之前和新添加的文档。这样就避免了重复上传文档造成的成本消耗。

# 怎么理解agent

可以理解成工具集，里面有langchain封装的功能，也可以自定义功能。比如我想让llm帮我在谷歌上搜索结果，但是llm本身并没有直接联网的能力。agent就是提供这些能力的

# 如果用户加了一个文档，然后发现这个文档内容是假的没有参考意义，且会污染本地知识库的内容，这个情况有什么方法可以让这个文档从AI的参考库中移除呢？

本地向量库删了，然后把修改后完整的文档重新上传构建

# 如果像知识库那些，我第一次提问没有得到想要的结果，后面继续追问这些，那它联系上下文的能力一样是可用的么？怎么识别我这次的提问需不需要联系上下文，以及能联系多久的上下文？

langchain有memory组件可以构建对话上下文，这个自动完成的。

# 如果上传的文档里面知识是存在矛盾的地方，比如举的特朗普为什么被捕，有的说是封口费，有的说是之前泄密文件，那他有什么方式来校正呢？

文档本身信息矛盾就需要人为完善文档内容。如果文档的口径是模棱两可的，那基于llm，有可能给出提示说内容有待核实。这个具体要看llm的发挥。

