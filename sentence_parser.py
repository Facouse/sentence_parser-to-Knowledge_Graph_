import os
from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller

class LtpParser:
    def __init__(self):
        # 初始化模型
        LTP_DIR = "./ltp_data_v3.4.0"
        self.segmentor = Segmentor()
        self.segmentor.load(os.path.join(LTP_DIR, "cws.model"))

        self.postagger = Postagger()
        self.postagger.load(os.path.join(LTP_DIR, "pos.model"))

        self.parser = Parser()
        self.parser.load(os.path.join(LTP_DIR, "parser.model"))

        self.recognizer = NamedEntityRecognizer()
        self.recognizer.load(os.path.join(LTP_DIR, "ner.model"))

        self.labeller = SementicRoleLabeller()
        self.labeller.load(os.path.join(LTP_DIR, 'pisrl_win.model'))

    '''语义角色标注'''

    def format_labelrole(self, words, postags):
        arcs = self.parser.parse(words, postags)
        # 语义角色标注，三个输入（分词，词性标注，依存句法）
        roles = self.labeller.label(words, postags, arcs)
        roles_dict = {}
        for role in roles:
            roles_dict[role.index] = {arg.name: [arg.name, arg.range.start, arg.range.end] for arg in role.arguments}
        return roles_dict

    '''句法分析---为句子中的每个词语维护一个保存句法依存儿子节点的字典'''

    def build_parse_child_dict(self, words, postags, arcs):
        child_dict_list = []
        format_parse_list = []
        # 保存各个词之间的关系
        for index in range(len(words)):
            child_dict = dict()
            for arc_index in range(len(arcs)):
                # arcs的索引从1开始 arc. head 表示依存弧的父结点的索引。
                # ROOT 节点的索引是 0 。
                # 第一个词开始的索引依次为1，2，3，···arc. relation 表示依存弧的关系。
                if arcs[arc_index].head == index + 1:
                    if arcs[arc_index].relation in child_dict:
                        child_dict[arcs[arc_index].relation].append(arc_index)  # 添加
                    else:
                        child_dict[arcs[arc_index].relation] = []  # 新建
                        child_dict[arcs[arc_index].relation].append(arc_index)
            child_dict_list.append(child_dict)  # 每个词对应的依存关系父节点和其关系
        rely_id = [arc.head for arc in arcs]  # 提取依存父节点id
        relation = [arc.relation for arc in arcs]  # 提取依存关系
        heads = ['Root' if id == 0 else words[id - 1] for id in rely_id]  # 匹配依存父节点词语
        for i in range(len(words)):
            a = [relation[i], words[i], i, postags[i], heads[i], rely_id[i] - 1, postags[rely_id[i] - 1]]
            format_parse_list.append(a)

        return child_dict_list, format_parse_list

    '''parser主函数'''

    def parser_main(self, sentence):
        # 输入一句话，进行分词
        words = list(self.segmentor.segment(sentence))
        # 进行词性标注
        postags = list(self.postagger.postag(words))
        # 依存句法，两个输入（分词，词性标注）
        arcs = self.parser.parse(words, postags)

        child_dict_list, format_parse_list = self.build_parse_child_dict(words, postags, arcs)
        roles_dict = self.format_labelrole(words, postags)
        return words, postags, child_dict_list, roles_dict, format_parse_list


if __name__ == '__main__':
    parse = LtpParser()
    sentence = '中国一直贯彻清零防疫政策'
    words, postags, child_dict_list, roles_dict, format_parse_list = parse.parser_main(sentence)
    print(words, len(words))
    print(postags, len(postags))
    print(child_dict_list, len(child_dict_list))
    print(roles_dict)
    print(format_parse_list, len(format_parse_list))
