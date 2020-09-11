# 中文分词

主要涉及两个库。  
jieba 库主要用于分词；  
snownlp 库主要用于情感分析。  

## jieba 库

### 分词

```python
# pip install jieba
import jieba

text = '我们中出了叛徒'
seg_list = jieba.cut(
    text,
    cut_all=False,  # 默认精确模式
    HMM=True,  # 默认HMM模式，用于识别未收录词。如果设为False，会识别为“中, 出”，而不是“中出”
    use_paddle=False # 利用深度学习框架，需要先 pip install paddlepaddle-tiny
)

# .cut() 或 .cut_for_search() 方法返回一个可迭代的 generator
# 也可以使用 .lcut() 或 .lcut_for_search() 返回一个列表
```

- 四种搜索模式  
  - 精确模式：cut_all=False  
  - 全模式：cut_all=True  
  - 搜索引擎模式：使用 .cut_for_search() 方法。在精确模式的基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词  
  - paddle模式  

### 提取关键字

```python
import jieba.analyse
import pprint  # 可用于打印 Python 任何数据类型

text = '我们中出了叛徒'

# 基于TF-IDF算法（更准确）
tfidf = jieba.analyse.extract_tags(
    text,
    topK=20,  # 权重最大的topK个关键词
    withWeight=False,  # 返回每个关键字的权重值
    allowPOS=(),  # 仅包括指定词性的词，如：('ns', 'n', 'vn', 'v','nr')
    withFlag=False,  # 返回关键词时把词性也带上
)
pprint.pprint(tfidf)  # 输出：['中出', '叛徒', '我们']

# 基于TextRank算法（不那么准确，但可以通过自定义词典来改进）
textrank = jieba.analyse.textrank(
    text,
    topK=5,  # 权重最大的topK个关键词
    withWeight=True  # 返回每个关键字的权重值
    allowPOS=(),  # 仅包括指定词性的词，如：('ns', 'n', 'vn', 'v','nr')
    withFlag=False,  # 返回关键词时把词性也带上
)
pprint.pprint(textrank)  # 输出：[]
```

### 词典

#### 内置词典的动态修改

```python
# 动态删减词典
# add_word(word, freq=None, tag=None)
# del_word(word)
jieba.add_word('中出')
jieba.del_word('中出')

# 调节单个词语的词频，使其能（或不能）被分出来
# 在 HMM 模式下可能无效
# suggest_freq(segment, tune=True)
jieba.suggest_freq('中出', False)  # 降低“中出”的词频
jieba.suggest_freq(('中', '出'), True)  # 提高“中”和“出”的词频（也就是降低了“中出”的出现频率）
```

#### 自定义词典

##### jieba.analyse.set_stop_words()  

在进行**关键字提取**时，我们可以使用 .set_stop_words() 来去掉那些不要的词，使提取的关键字更准确。  

```python
jieba.analyse.set_stop_words(file_name)
# file_name 为文件类对象（如.txt）或自定义词典的路径
```

##### jieba.load_userdict()

虽然 jieba 有新词识别能力，但是自行添加新词可以保证更高的正确率。  

```python
jieba.load_userdict(file_name)
# file_name 为文件类对象或自定义词典的路径
# 词典格式和 dict.txt 一样，一个词占一行；每一行分三部分：词语、词频（可省略）、词性（可省略），用空格隔开，顺序不可颠倒。
# 如：中出 999 v（中出，词频999，动词）
```

> 词性网上查查就有  

## snownlp 库

snownlp 库主要用于情感分析，即用于分析评论内容倾向于积极的还是消极的。

### 情感分析

```python
from snownlp import SnowNLP

text = '我们中出了叛徒'
s = SnowNLP(text)
s.sentiments  # 返回 0 ~ 1 的值，越接近1，越积极；反之越消极。
```

### 其他功能

```python
# 1 中文分词
s.words

# 2 词性标注 (隐马尔可夫模型)
list(s.tags)

# 3 拼音（Trie树）
s.pinyin

# 4 繁体转简体
text3 = '後面這些是繁體字'
s3 = SnowNLP(text3)
s3.han

# 5 提取关键字
s.keywords(limit=5)

# 6 信息衡量
s.tf # 词频越大越重要
s.idf # 包含此条的文档越少，n越小，idf越大，说明词条t越重要

# 7 训练
from snownlp import seg
seg.train('data.txt')
seg.save('seg.marshal')
# 修改snownlp/seg/__init__.py的 data_path 指向新的模型即可
```
