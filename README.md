# AutoRead 通过pdf直接生成你的词汇表

> “Life is difficult. This is a great truth, one of the greatest truths. It is a great truth because once we truly see this truth, we transcend it. Once we truly know that life is difficult-once we truly understand and accept it-then life is no longer difficult. Because once it is accepted, the fact that life is difficult no longer matters.” -M.Scott.Peck, The Road Less Travelled
> 

# 项目介绍

你是否因为文章太长， 单词不认识而发愁？

你是否因为不认识的单词太多，而找不到系统的整理方法？

你是否因为市面上的词汇表大而全，无法关注所需要的单词？

你是否想学会一本书当中的全部单词，流利阅读原版著作？

AutoRead这个项目可以满足你的需求！ 🥰 通过版面分析方法将PDF转化成txt，再从txt当中提取得到属于你水平等级的词汇！

本项目的优势有：

1. 高度集成，直接从pdf得到属于你的词汇表！
2. 可以根据英语水平等级（中考，高考，考研，托福雅思）等搜集对应的词汇！
3. 包含词汇原型，音标，英文释义，中文释义，Collins星级，bnc（历史文本数据库）词频以及frq（当代文本数据库）词频，让你对学习的单词有一个全面的了解！
4. 融合上下文语境记忆单词，更好用更高效！

# 使用方法

下载本git repo到你的目录

```python
git clone https://github.com/Skywalker-Harrison/AutoRead.git
```

下载所需要的安装包

```python
pip install -r requirements.txt
```
在[百度网盘](https://pan.baidu.com/s/1NR3u67o_TXHN12Lfwj3O2g) (提取码w0pe)下载`ecdict.csv`以及`stardict.7z`文件，并放置在`ECDICT\`目录下。
复制你的PDF文件路径，然后修改`pipeline.sh`中的参数`PDF_FILE_PATH`为你的pdf路径，`USER_LEVEL`为您希望搜集的词汇水平，从易到难依次编号（0-中考英语，1-高考英语，2-CET4, 3-CET6, 4-考研，5-TOEFL，IELTS，6-GRE）。本项目将为你总结您需要的难度及其难度以上的词汇。（注意，pdf文档必须是可以识别字符的）

随后在sh环境当中运行

```python
sh pipeline.sh
```

大功告成！本项目会同时生成json文件和csv文件，目录和源pdf的目录相同。

现在，可以打开csv文件看看生成的效果了。

注意：直接打开会导致乱码，需要先打开excel, 选择数据→从文本/csv导入。

# 效果展示

我选取的pdf是M.Scott.Peck的The Road Less Travelled (少有人走的路），提取难度大于等于TOEFL/IELTS的单词，因此设置`USER_LEVEL=5`

下面是得到的词汇表

![单词](https://github.com/Skywalker-Harrison/AutoRead/blob/main/Image/2.png)

![上下文](https://github.com/Skywalker-Harrison/AutoRead/blob/main/Image/1.png)

# 后续改进安排

- [ ]  加入同义词，反义词
- [ ]  加入Merriam Webster单词查询链接
- [ ]  允许用户自定义词表
- [ ]  加入context的翻译插件

# 应用场景分析

- 用于快速提取出pdf文档当中的生词，预先学习，提高效率
- 整理系统的单词表
- 结合语境记忆词汇

# 致谢

>我虽然行过死荫的幽谷， 也不怕遭害

本项目是我纯粹出于兴趣开发的，目的在于帮助英语学习者减少负担。相比在阅读的时候一个一个查词，在阅读之前整理出一个系统的词汇表有助于预习过程，同时阅读后也可以利用该词汇表进行复习，节省了大量时间！本项目参考了一些大佬的工作，例如[ECDICT](https://github.com/skywind3000/ECDICT),[txt2dic](https://github.com/cndaqiang/txt2dic)等，再次表示感谢！

