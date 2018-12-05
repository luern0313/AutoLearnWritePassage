#!/usr/bin/python3
# 写文件
import json
import random
import jieba

# 连续储存两个词语，理论上生成文章更流畅
'''
txt
i:am_0.65|have_0.2|will_0.25/you:are_0.85|like_0.15

zishi
[0]i:am_0.65|have_0.2|will_0.25
[1]you:are_0.85|like_0.15

zishi 2
[0][0]i
   [1]'
   
json zishi
{
	"i am" : {"$" : 20, "a" : 0.65, "working" : 0.2, "an" : 0.15},
	"you are" : {"$" : 20, "a" : 0.85, "an" : 0.15}
	
}
'''

PUNCTUATION = ['，', '。', '？', '！', '：', '；']


# 拿到之前学习过的数据
def learned():
    try:
        with open("z知识库.txt", "rt") as zishi_file:
            zishi = eval(zishi_file.read())
            return zishi
    except IOError:
        zishi = {}
        print('11223333333')
        # open("知识库.txt", "w")
        return zishi


# 储存学习数据
def write():
    with open("z知识库.txt", "wt") as out_file:
        out_file.write(str(zishi))


# 遍历整个文章的学习
def learns():
    i = -1
    while i < len(textarray) - 2:
        i = i + 1
        learn(textarray[i], textarray[i + 1])


# 单个的词语学习
def learn(word, nword):
    zikey = zishi.keys()
    if word in zikey:
        zishikey = zishi[word].keys()
        if nword in zishikey:
            for j in zishikey:
                if j != '$':
                    if j != nword:
                        zishi[word][j] = zishi[word][j] / (1 + 1 / zishi[word]['$'])
            zishi[word][nword] = (zishi[word][nword] + 1 / zishi[word]['$']) / (1 + 1 / zishi[word]['$'])
            zishi[word]['$'] = zishi[word]['$'] + 1
        else:
            for j in zishikey:
                if j != '$':
                    zishi[word][j] = zishi[word][j] / (1 + 1 / zishi[word]['$'])
            zishi[word][nword] = (1 / zishi[word]['$']) / (1 + 1 / zishi[word]['$'])
            zishi[word]['$'] = zishi[word]['$'] + 1
    else:
        zishi[word] = {'$': 1, nword: 1}


# 分词，以及对标点符号和换行、空格的预处理
def screen(text):
    global PUNCTUATION
    textarray = jieba.cut(text)  # 分词
    textarray = '[~]'.join(textarray).split('[~]')  # 分词出来的数组好像不是标准的数组。。用这个方法转换成标准的数组
    ii = -1
    while ii < len(textarray) - 1:  # 预学习，主要处理空行，空格
        ii = ii + 1
        textarray[ii].lower()
        textarray[ii] = textarray[ii].strip()
        if textarray[ii] == '\n':
            if textarray[ii + 1] == '\n':
                ii = ii + 2  # 学习样本里有空行，代表学习到了下一个文章，下一个文章不应和上一个建立关系
            else:
                learn(textarray[ii - 1] + ' ', textarray[ii + 1])
                ii = ii + 1
        elif textarray[ii] in PUNCTUATION:
            learn(textarray[ii - 1] + textarray[ii], textarray[ii + 1])
            ii = ii + 1
    return textarray


# 根据现有词语和随机数得到下一个词语
def ran(w, r):
    zikey = zishi.keys()
    if w in zikey:
        zishikey = zishi[w].keys()
        for i in zishikey:
            if i != '$':
                if r < float(zishi[w][i]):
                    print(i)
                    if i == '\n':
                        return ''
                    else:
                        return i
                else:
                    r = r - float(zishi[w][i])
                    print(r)
    else:
        return ' '


# 生成文章
def sen(a):
    global PUNCTUATION
    sent = []
    sent.append(a)
    while len(sent) < 5000:  # 修改左侧数值可限定文章<词语>数
        b = ran(sent[-1], random.random())
        if b in PUNCTUATION:  # 标点符号的检测
            if ran(sent[-1] + b, random.random()) != ' ':
                sent.append(b)
            else:
                if ran(b, random.random()) != ' ':
                    sent.append(b)
                else:
                    break
        elif b != ' ':
            sent.append(b)
        else:
            break
    return ''.join(sent)


while 1:
    print('中文v2版本哦')
    print('学习/写作/关闭')
    choose = input('')
    text = 0
    if choose == '学习':
        try:
            input('在同目录下创建“zbook.txt”')
            with open("zbook.txt", "rt", encoding="utf-8") as in_file:
                text = in_file.read()
        except IOError:
            print('没有找到书本')
            input('')
        finally:
            if text == 0:
                input('未发现')
                exit();
            zishi = learned()  # 可以继续学习
            textarray = screen(text)
            print(textarray)
            print('一共有' + str(len(textarray)) + '个词。。学习中。。。。')
            learns()
            input('学习完成')
            write()
    elif choose == '写作':
        zishi = learned()
        while 1:
            print('钦定第一个词')
            print('输入列表查看所有词')
            word = input()
            if word == '列表':
                for i in zishi.keys(): print(i)
            else:
                if word in zishi.keys():
                    print(' ')
                    print(sen(word))
                    print(' ')
                    break
    elif choose == '关闭':
        exit();
    elif choose == '调试':
        while True:
            print(ran(input(), random.random()))
# print(text)
# with open("test.txt", "wt") as out_file:
#	out_file.write("该文本会写入到文件中\n看到我了吧！")

# Read a file
