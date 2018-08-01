#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import jieba
import string
import re
import all_function as P

if __name__ == "__main__":
	dict = P.load_csv("HSK词汇表.txt")
	index = ['1', '2', '3', '4', '5', '6']  # index为难度等级排列
	lines = P.load_data("test.txt")
	#lines = np.array(lines)
	# for i in range(len(lines)):
	# 	lines[i].append(i)
	for x in lines:
		num = P.word_num(P.sentence_word(x[1]),dict)
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
		# print(a,b, re_result, x[0])
		for k in range(len(a)):
			r = 0
			num_1 = int(a[k][0])  # index末尾难度等级
			num_2 = int(b[k][0])  # index次末未难度等级
			m = a[k][1]           # num_1个数
			n = b[k][1]           # num_2个数
			r_1 = num_1 * m * 5.5 #训练后权重系数
			r_2 = num_2 * n * 1	  #基准权重系数
			if r_1 >= r_2:
				r = num_1
			else:
				r = num_2
			print('HSK',r, x[0], x[1])

