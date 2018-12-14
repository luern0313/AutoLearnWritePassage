#!/usr/bin/python3
# 写文件
import json
import random
import jieba

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
	"i" : {"$" : 20, "am" : 0.65, "have" : 0.2, "will" : 0.15},
	"you" : {"$" : 20, "are" : 0.85, "like" : 0.15}
	
}
'''


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


def write():
    with open("z知识库.txt", "wt") as out_file:
        out_file.write(str(zishi))


def learn():
    i = -1
    while i < len(textarray) - 2:
        i = i + 1
        zikey = zishi.keys()
        if textarray[i] in zikey:
            zishikey = zishi[textarray[i]].keys()
            if textarray[i + 1] in zishikey:
                for j in zishikey:
                    if j != '$':
                        if j != textarray[i + 1]:
                            zishi[textarray[i]][j] = zishi[textarray[i]][j] / (1 + 1 / zishi[textarray[i]]['$'])
                zishi[textarray[i]][textarray[i + 1]] = (zishi[textarray[i]][textarray[i + 1]] + 1 /
                                                         zishi[textarray[i]]['$']) / (1 + 1 / zishi[textarray[i]]['$'])
                zishi[textarray[i]]['$'] = zishi[textarray[i]]['$'] + 1
            else:
                for j in zishikey:
                    if j != '$':
                        zishi[textarray[i]][j] = zishi[textarray[i]][j] / (1 + 1 / zishi[textarray[i]]['$'])
                zishi[textarray[i]][textarray[i + 1]] = (1 / zishi[textarray[i]]['$']) / (
                            1 + 1 / zishi[textarray[i]]['$'])
                zishi[textarray[i]]['$'] = zishi[textarray[i]]['$'] + 1
        else:
            zishi[textarray[i]] = {'$': 1, textarray[i + 1]: 1}


def scrlearn(word, nword):
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


def screen(text):
    textarray = jieba.cut(text)
    textarray = '[~]'.join(textarray).split('[~]')
    ii = -1
    while ii < len(textarray) - 1:
        ii = ii + 1
        textarray[ii].lower()
        textarray[ii] = textarray[ii].strip()
        if textarray[ii] == '\n':
            if textarray[ii + 1] == '\n':
                ii = ii + 2
            else:
                scrlearn(textarray[ii - 1] + ' ', textarray[ii + 1])
                ii = ii + 1
        if textarray[ii] == ' ':
            scrlearn(textarray[ii - 1] + ' ', textarray[ii + 1])
            ii = ii + 1
    return textarray


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


def sen(a):
    sent = []
    sent.append(a)
    while len(sent) < 1000:
        b = ran(sent[len(sent) - 1], random.random())
        if b == '，' or b == '。' or b == '？' or b == '！':
            if ran(sent[len(sent) - 1] + b, random.random()) != ' ':
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
    print('中文版本哦')
    print('学习/写作/关闭')
    choose = input('先')
    text = 0
    if choose == '学习':
        try:
            # zishi =
            input('在同目录下创建“zbook.txt”')
            with open("zbook.txt", "rt", encoding="utf-8") as in_file:
                text = in_file.read()
        except IOError:
            print('没有找到书本')
            input('创建完成按回车继续')
        finally:
            if text == 0:
                input('未发现')
                exit();
            # print(text)
            zishi = learned()
            textarray = screen(text)
            print(textarray)
            print('一共有' + str(len(textarray)) + '个词。。学习中。。。。')
            learn()
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
        print('→_→')
# print(text)
# with open("test.txt", "wt") as out_file:
#	out_file.write("该文本会写入到文件中\n看到我了吧！")

# Read a file
