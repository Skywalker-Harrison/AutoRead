from stardict import DictCsv,DictHelper,LemmaDB
import os
from tqdm import tqdm
import json
import csv
import re
import argparse

### Load Lemma ###
class GetImportantWords(object):
    def __init__(self,lemma, dc, args):
        self.lemma = lemma
        self.dc = dc
        self.level_above = True #是否查找在所需要水平之上的单词，False:只查找该水平的单词
        self.level_dict = {'zk':0,'gk':1,'cet4':2,'cet6':3,'ky':4,'toefl':5,'ielts':5,'gre':6}
        self.min_sen_len = 4
        self.original_txt_path = args.input_txt_file

    def get_words(self,file_name):
        words = []
        with open(file_name,'r') as f:
            lines = f.readlines()
            for line in lines:
                words.append(line.strip())
        return words

    def is_sentence(self, text):
        pattern = r'^[A-Z][^.!?]*[.!?]$'
        if re.match(pattern, text):
            return True
        return False 
    
    def get_sentences(self,file_name): #从一个txt文件当中获得句子
        output_sentences = []
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()
            # 使用正则表达式进行句子分割
            sentences = re.split(r'(?<=[.!?])\s+', content)
            
            # 判断并输出符合条件的句子
            for sentence in sentences:
                sentence=sentence.replace('\n','')
                sentence_len = len(sentence.split(' '))
                if self.is_sentence(sentence) and sentence_len>=self.min_sen_len:
                    output_sentences.append(sentence)
        return output_sentences
    
    def clean_data(self, words):
        # 查找单词
        cleaned_words = []
        query_results = []
        print('---Lemmatizing---')
        for word in tqdm(words):
            try:
                cleaned_words.append(self.lemma.word_stem(word)[0])
            except:
                cleaned_words.append(word)
        print('---Searching---')
        for word in tqdm(cleaned_words):
            query_results.append(self.dc.query(word))
        return query_results
    
    def clean_context(self,contexts):
        output_contexts=[]
        for context in contexts:
            formatted_sentence = re.sub(r'\s+', ' ', context.strip())
            formatted_sentence = re.sub(r'([.?!])\s+', r'\1 ', formatted_sentence) 
            output_contexts.append(formatted_sentence)
        return output_contexts

    def get_tag_number_range(self,tags):
        tag_numbers = []
        for tag in tags:
            if tag in self.level_dict.keys():
                tag_numbers.append(self.level_dict[tag])
        min_level = min(tag_numbers)
        max_level = max(tag_numbers)
        return min_level, max_level
    
    def get_context(self,sentences,word):
        all_forms = self.lemma.get(word) # A list which contain all the forms of  word
        context = []
        if all_forms == None:
            all_forms = [word]
        else:
            all_forms.append(word)
        for form in all_forms:
            for sentence in sentences:
                if form in sentence:
                    context.append(sentence)
        return context
    def to_add_word(self,result,level):
        to_add = False
        tags = result['tag']
        if tags != '':
            tags = tags.split(' ')
            min_level,max_level = self.get_tag_number_range(tags)
            if min_level>level:
                to_add = True
        else:
            #可能是专有名词等
            word = result['word']
            if len(word)<=5:
                to_add = False
            elif any(key in result['translation'] for key in ['人名', '姓名', '男子名', '女子名', '男名', '女名', '姓氏']):
                to_add = False
            else:
                to_add = True
        return to_add

    def get_output(self,query_results,level):
        '''
        获取输出结果,根据读者水平需要
        '''
        sentences = get_important_words.get_sentences(self.original_txt_path)
        output_words =  {}
        print('---Finding Words matching your level ---')
        for result in tqdm(query_results):
            if result == None:
                continue
            id = result['id']
            word = result['word']
            phonetic = result['phonetic']
            definition = result['definition']
            translation = result['translation']
            collins = result['collins']
            oxford = result['oxford']
            bnc = result['bnc']
            frq = result['frq']
            tags = result['tag']
            to_add = self.to_add_word(result=result,level=level)
            if to_add:
                contexts = self.get_context(sentences=sentences,word=word)
                contexts = self.clean_context(contexts)
                output_words.update({id:{'word':word,
                                         'phonetic':phonetic,
                                         'definition':definition,
                                         'translation':translation,
                                         'tag':tags,
                                         'context':'\n'.join(contexts[:1]), #最多展示三句话
                                         'collins':collins,
                                         'oxford':oxford,
                                         'bnc':bnc,
                                         'frq':frq}})
        return output_words


    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_vocab_file',required=True,help='Your vocab file')
    parser.add_argument('--user_level', default=5, help='User\'s level')
    parser.add_argument('--output_csv_file', help='output path of csv file', required=True)
    parser.add_argument('--output_json_file', help='output path of json file',required=True)
    parser.add_argument('--input_txt_file',help='txt file of the original pdf',required=True)
    args = parser.parse_args()
    lemma = LemmaDB()
    lemma.load('lemma.en.txt')
    csvname = os.path.join(os.path.dirname(__file__), 'ecdict.csv')
    dc = DictCsv(csvname)
    get_important_words = GetImportantWords(lemma=lemma,dc=dc, args=args)

    words = get_important_words.get_words(args.input_vocab_file)
    query_results = get_important_words.clean_data(words)
    output_words = get_important_words.get_output(query_results=query_results,level=int(args.user_level))

    with open(args.output_json_file, "w",encoding='utf-8') as file:
        json.dump(output_words, file, ensure_ascii=False, indent=4)
    field_names = list(output_words[next(iter(output_words))].keys())
    with open(args.output_csv_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(output_words.values())
