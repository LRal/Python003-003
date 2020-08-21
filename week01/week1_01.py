from bs4 import BeautifulSoup
import pandas as pd
import requests

# 获取网页
url = 'https://maoyan.com/films?showType=3'

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.61'

header = {'user-agent': user_agent}

response = requests.get(url, headers=header)

# 解析网页
soup = BeautifulSoup(response.text, 'html.parser')

# 提取内容（名称、类型、上映时间）
data = pd.DataFrame()

for tag in soup.find_all('div', attrs={'class':'movie-hover-info'}):
    
    # 获取所有文字内容
    text = tag.get_text('|',strip=True)

    # 信息提取
    title = text.split('|')[0]
    genre = text.split('类型:|')[1].split('主演:|')[0][:-1]
    release_date = text.split('上映时间:|')[1]

    # 信息整理
    info = {'title':title, 'genre':genre, 'release_date':release_date}
    data = data.append(info, ignore_index=True)
    
data = data.head(10)[['title', 'genre', 'release_date']]

data.to_csv('data.csv', encoding='gbk', index=False)