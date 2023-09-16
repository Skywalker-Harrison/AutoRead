#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#本脚本参考自[使用python提取英文文章中的单词及出现的次数(原创)](http://www.51testing.com/html/53/61753-154953.html)
import re
import string
import argparse

def get_word_list(input_file,output_file):
    #输出文件
    f = open(output_file,"w")
    #输入文件
    r = open(input_file,"r")
    strs =r.read()
    ##使用正则表达式，把单词提出出来，并都修改为小写格式
    s = re.findall("\w+",str.lower(strs))
    #去除列表中的重复项，并排序
    l = sorted(list(set(s)))
    #去除字母数字下划线,并保留长度大于3的单词
    for i in l:
        p = re.search("[^a-z]",i)
        if not p and len(i)>3 and len(i)<15:
            f.write(i+"\n")
    r.close()
    f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', required=True, help='input txt file')
    parser.add_argument('--output_file', required=True, help='output txt file')
    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file
    get_word_list(input_file=input_file,output_file=output_file)


