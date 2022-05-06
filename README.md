# sentence_parser-to-Knowledge_Graph_
利用pyltp进行语义角色构建，并设计规则进行关系抽取

**sentence_parser：主要是进行了分词、词性标注、句法分析、语义角色标注。
                   分词 + 词性标注 ---> 句法分析
                   分词 + 词性标注 + 句法分析 ---> 语义角色标注**
                   

**triple_extraction：主要利用语义角色标注(主要利用了主谓关系，定中关系等)，构建三元组。**


整个过程需要利用已经训练好的模型，具体安装配置过程可以查看https://github.com/HIT-SCIR/pyltp
