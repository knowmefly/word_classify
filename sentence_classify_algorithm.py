#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import numpy as np
import re
import string
import all_function as P
import matplotlib.pyplot as plt


if __name__ == "__main__":
	COUNT = 0
	#处理文本数据
	dict = P.load_csv("HSK词汇表.txt")
	lines = P.load_data("train.txt")[1:]
	lines = sorted(lines, key=lambda elem: elem[0])
	index = ['1', '2', '3', '4', '5', '6']  #index为难度等级排列

	re_result = []
	#假设验证

	# 句子转一维数组
	for x in lines:
		x[0] = re.sub("\D", "", x[0])
		result = []
		re_word = []
		word = P.sentence_word(x[2])
		#去除符号
		for i in word:
			re_word.extend(re.findall(u'[\u4e00-\u9fff]+', i))
		#单词转数组
		num = P.word_num(re_word, dict)
		#统计index元素个数 并降序排列
		tmp = P.index_list(num,index)
		result = sorted(tmp.items(), key=lambda e: e[0], reverse=True)

		re_result = []
		for i in range(len(result)):
			if result[i][1]>0:
				re_result.append(result[i])
				if i<5 :
					re_result.append(result[i+1])
			if len(re_result) == 1:
				re_result.append(['0',0])
			if len(re_result)>1:
				break

		a = []
		b = []
		for j in range(len(re_result)):
			if j % 2 == 0:
				a.append(re_result[j])
			else:
				b.append(re_result[j])
		#print(a,b, re_result, x[0])
		for k in range(len(a)):
			r = 0
			num_1 = int(a[k][0])  # index末尾难度等级
			num_2 = int(b[k][0])  # index次末未难度等级
			m = a[k][1]  # num_1个数
			n = b[k][1]  # num_2个数
			r_1 = num_1 * m * 5.5 #在[5.0,6.2]区间上权重系数等效 此处取5.5
			r_2 = num_2 * n * 1   #基准权重系数
			if r_1 >= r_2:
				r = num_1
			else:
				r = num_2
			# print(x[0],r)
			if r == int(x[0]):
				COUNT = COUNT + 1
		accuracy = COUNT / len(lines)
	print(accuracy)
