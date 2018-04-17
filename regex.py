#coding:utf-8
#description:采用正则表达式检索出文本中包含特定串（因为...所以）的句子,并对齐输出。
#确定中文范围 : [\u4e00-\u9fa5],python写的时候要写成u"[\u4e00-\u9fa5]"

import re
filename = input(u"请输入语料库txt名称:")
#filename = "corpus.txt"
fp = open(filename, 'r',encoding='gb2312') #读入文件
f = open("2015211700.txt", 'w') #输出文件
#pattern = re.compile(r'([^因为]*?)因为(.*?)所以([^因为]*)') #无法处理嵌套循环
pattern = re.compile(r'([^因为]*)因为(.*)所以([^所以]*)') #该pattern匹配句子中开头的因为和末尾的所以

#先对txt文档中的句子根据句号、感叹号、问号、换行符进行句子切分，切分好的句子放在seq中
seq = []
rows = [0];row = 0
for s in fp.readlines():
    row += 1
    pat = re.compile(r'([!。？.?!])')
    sequence = pat.split(s)
    i = 0
    while i< len(sequence):
        s = sequence[i]
        if s == '\n':
            break
        if i+1 <= len(sequence)-1 and sequence[i+1] == (u'。' or u'？' or u'！' or '.' or '?' or '!'):
            s += (sequence[i+1]);i += 1
        seq.append(s);i += 1;rows.append(row)

max_length = 0
count = 0 #输出句子计数
for s in seq:
    result = pattern.findall(s)
    count += 1
    for res in result:
        res = list(res) #必须改为list，因为链表无法修改
        if max_length < len(res[1]):
            max_length = len(res[1])
        # res[1]中存在还有因为...所有的情况，进行检验
        if len(pattern.findall(res[1])) != 0:
            seq.append(res[1]);rows.append(rows[count])

count = 0
for s in seq:
    result = pattern.findall(s)
    count += 1
    if len(result) == 0:
        continue
    sequence = []
    for res in result:
        res = list(res) #必须改为list，因为链表无法修改
        res[0] = res[0][-3:] + (3-len(res[0][-3:]))*chr(12288)
        sequence.append(str(rows[count]))
        sequence.append(res[0])
        sequence.append("*因为*")
        res[1] = res[1] + (max_length - len(res[1]))*chr(12288)
        sequence.append(res[1])
        sequence.append("&所以&")
        res[2] = res[2][:3] + (3 - len(res[2][:3]))*chr(12288)
        sequence.append(res[2])
    f.write("\t".join(sequence)+"\n")

f.close()



