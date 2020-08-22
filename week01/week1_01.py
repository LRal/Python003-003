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
data = []
for tag in soup.find_all('div', attrs={'class': 'movie-hover-info'}, limit=10):
    text = tag.get_text('|', strip=True)

    title = text.split('|')[0]
    genre = text.split('类型:|')[1].split('主演:|')[0][:-1]
    release_date = text.split('上映时间:|')[1]

    info = [title, genre, release_date]
    data.append(info)

# 导出内容
movie_data = pd.DataFrame(data)
movie_data.to_csv('data.csv', encoding='gbk', index=False, header=False)
