#!/usr/bin/python3
# 写文件
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
        with open("zknow.txt", "rt", encoding='utf-8') as zishi_file:
            zishi = eval(zishi_file.read())
            return zishi
    except IOError:
        zishi = {}
        print('11223333333')
        # open("知识库.txt", "w")
        return zishi


# 储存学习数据
def write():
    with open("zknow.txt", "wt", encoding='utf-8') as out_file:
        out_file.write(str(zishi))


# 遍历整个文章的学习
def learns():
    i = 0
    while i < len(textarray) - 2:
        learn(textarray[i] + ' ' + textarray[i + 1], textarray[i + 2])
        learn(textarray[i], textarray[i + 1])
        i = i + 1


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
    '''ii = -1
    while ii < len(textarray) - 2:  # 预学习，主要处理空行，空格
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
            learn(textarray[ii], textarray[ii + 1])
            ii = ii + 1'''
    return textarray


# 根据现有词语和随机数得到下一个词语
def ran(w, w2, r):
    zikey = zishi.keys()
    # and random.random() < 0.98
    if w != '' and (w + ' ' + w2) in zikey:
        zishikey = zishi[w + ' ' + w2].keys()
        k = int(len(zishikey) == 2)
        for i in zishikey:
            if i != '$':
                if r < float(zishi[w + ' ' + w2][i]):
                    if i == '\n':
                        return '', True, k
                    else:
                        return i, True, k
                else:
                    r = r - float(zishi[w + ' ' + w2][i])
    else:
        if w2 in zikey:
            zishikey = zishi[w2].keys()
            for i in zishikey:
                if i != '$':
                    if r < float(zishi[w2][i]):
                        if i == '\n':
                            return '', False, -1
                        else:
                            return i, False, -1
                    else:
                        r = r - float(zishi[w2][i])
        else:
            return '~', False, -1


# 生成文章
def sen(a, s):
    global PUNCTUATION
    sent = []
    sent.append(a)
    sent.append(s)
    fin = ''
    double = doublet = kk = kkt = 0
    while len(sent) < 10000:  # 修改左侧数值可限定文章<词语>数
        b, d, k = ran(sent[-2], sent[-1], random.random())
        double += d
        doublet += 1
        if k != -1:
            kk += k
            kkt += 1
        if b == '':
            sent.append('\n')
        elif b != '~':
            if not ((b in PUNCTUATION) and (sent[-1] in PUNCTUATION)):
                # if b != sent[-1]:
                    sent.append(b)
        else:
            fin = sent[-2] + '，' + sent[-1]
            break
    return ''.join(sent), fin, double, doublet, kk, kkt


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
                exit()
            zishi = learned()  # 可以继续学习
            textarray = screen(text)
            print(textarray)
            print('一共有' + str(len(textarray)) + '个词。。学习中。。。。')
            learns()
            input('学习完成')
            write()
    elif choose == '写作':
        zishi = learned()
        while True:
            print('钦定第一个和第二个词')
            print('输入列表查看所有词')
            word = input()
            if word == '列表':
                for i in zishi.keys():
                    print(i)
            else:
                if sum([i.find(word + ' ') == 0 for i in zishi.keys()]) != 0:
                    while True:
                        print('输入第二个词语')
                        print('输入列表查看所有词')
                        word2 = input()
                        if word2 == '列表':
                            for i in zishi.keys():
                                if i.find(word + ' ') == 0:
                                    print(i[len(word) + 1:])
                        else:
                            senn, fin, d, dt, k, kt = sen(word, word2)
                            print(senn)
                            with open("result.txt", "wt", encoding='utf-8') as out_file:
                                out_file.write(str(senn))
                            print('----------------------------------------------')
                            print('本次生成报告：')
                            print('  生成文章结束原因：' + ('词数限制' if fin == '' else '无词语接龙：' + fin))
                            print('  词语由双词生成数量：' + str(d) + '/' + str(dt) + '，' + str(d * 100 / dt) + '%')
                            print('  词语由双词生成中单词生成数量：' + str(k) + '/' + str(kt) + '，' + str(k * 100 / kt) + '%')
                            print('')
                            print('文章已储存至 result.txt')
                            print('----------------------------------------------')
                            print('')
                            break
                break
    elif choose == '关闭':
        exit()
    elif choose == '调试':
        while True:
            print(ran(input(), input(), random.random()))
