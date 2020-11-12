"""
使用 pandas 代替 django ORM 进行复杂处理
"""

import json
import pandas as pd


def process_data(df):
    """
    处理爬虫数据, 获取评论数量, 正向评价数量和比例
    由于正负评论处理方法基本相同, 这里只处理正向评论
    """
    total_num = df['name'].value_counts().rename_axis(
        'name').reset_index(name='total_num')
    positive_num = df[df['stmscore'] >= 0.5]['name'].value_counts(
    ).rename_axis('name').reset_index(name='positive_num')

    new_df = pd.merge(total_num, positive_num, how='outer')
    new_df['positive_pct'] = new_df['positive_num'] / new_df['total_num']
    new_df['positive_pct'] = new_df['positive_pct'].apply(
        lambda x: format(x, '.2%')
    )

    return df_to_json(new_df)


def df_to_json(df):
    """
    将 df 转化为 json 格式, 以便于渲染到模板中
    """
    data = []
    json_records = df.reset_index().to_json(orient='records')
    data = json.loads(json_records)
    return {'data': data}
