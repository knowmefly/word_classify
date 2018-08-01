#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#这个文件里包含了所有
import numpy as np
import jieba
import string
import re

#字典制作
def load_csv(file_path):
	f = open(file_path)
	dict = {}
	for line in f.readlines():
		row = {}
		lines = line.strip().split(",")
		row[lines[1]] = lines[0]
		# for x in lines:
		# 	row.append(x)
		dict.update(row)
	f.close()
	return dict

#加载数据
def load_data(file_path):
	f = open(file_path)
	data = []
	for line in f.readlines():
		row = []
		lines = line.strip().split("\t")
		for x in lines:
			row.append(x)
		data.append(row)
	f.close()
	return data

#句子切片 句子转单词
def split_sentence(sentence):
	cut = jieba.cut(sentence)
	return cut
def sentence_word(data):
	cut = split_sentence(data)
	cut= list(cut)
	return cut
#句子转词向量,词向量中的数字为train数据jieba分词后每个词汇匹配到HSK5000词汇后对应的HSK词汇难度等级
def word_num(word,dict):

	tmp = []
	fail = []
	for x in word:
		if dict.__contains__(x):    #这里的匹配为全匹配,只有词汇完全一样时才能匹配成功
			tmp.append(dict[x])
		else:
			tmp.append('0')         #如果没有匹配到,则置为0
	return tmp

#统计个数（此个数为上面词向量中相同难度等级数字的个数,这里是为了向量统一降维降到六个维度,以便之后更好的数据分析）
def index_list(arr,index):
    result = {}
    for i in index:
        result[i] = arr.count(i)
    return result


if __name__ == "__main__":                            #此处为函数入口
	dict = load_csv("HSK词汇表.txt")                   #把HSK词汇表转化为字典型数据
	lines = load_data("train.txt")                    #加载train数据
	lines = sorted(lines, key=lambda elem:elem[0])    #按照句子难度等级排序
	# for x in lines[:-1]:
		# num = word_num(sentence_word(x[2]),dict)
		# q = 0
		# for i in num:
		# 	q += (int(i)*int(i)/36)/len(num)
		#print(num[1])
	# for x in lines:
	# 	print(x)
	# word = sentence_word(lines)词汇表
	# print(word[0])
	# for x in dict:
	# 	print(x, ":", dict[x])

	'''
		测试数据与训练数据、字典单词匹配分析,这些是构建句子等级算法前对测试数据在训练数据中的词汇匹配度做一个估计
		意外地发现训练数据集大概有一半jieba分词之后都不在HSK5000中,而test测试数据集也大概有一半不在HSK5000中
		所以可以大胆地假设,拿训练数据去做句子分级算法后,再用test数据集做分类（分级）,其效果可以令人接受

	'''
	train = []
	test = []
	test_w = load_data("test.txt")
	for x in lines:
		 train.extend(sentence_word(x[2]))
	for x in test_w:
		test.extend(sentence_word(x[1]))
	text_1 = []
	for x in test:
		text_1.extend(re.findall(u'[\u4e00-\u9fff]+', x))
	text_0 = []
	for x in train:
		text_0.extend(re.findall(u'[\u4e00-\u9fff]+', x))

	#测试数据集不在训练数据集
	t_tr = [x for x in text_1 if x not in text_0]
	#测试与字典匹配
	t_d = [x for x in text_1 if dict.__contains__(x)]
	#train与字典匹配
	tr_d = [x for x in text_0 if dict.__contains__(x)]

	#测试数据集在训练数据集中但不在字典数据中（HSK5000词汇）
	n = [x for x in t_tr if dict.__contains__(x)==False]
	m = t_tr
	#print(m)
	# print(np.mat(m))
	# print(len(m))
	# print(np.mat(n))
	# print(len(n))
	# print("test与train匹配词数：",len(t_tr),'\n',
	# 	"test与dict匹配词数",len(t_d),'\n',
	# 	"test词数：", len(test),'\n',
	# 	"train与dict匹配词数:", len(tr_d),'\n',
	# 	"train词数：",len(train))
