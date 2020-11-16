"""
使用 pandas 代替 Django ORM, 以便处理数据
"""

import json
import pandas as pd


def df_to_json(df):
    """
    将 df 转化为 json 格式, 以便于渲染到模板中
    """

    json_records = df.to_json(orient='records')
    json_data = json.loads(json_records)
    data = {'data': json_data}
    return data


def analyse_sentiments(df):
    """
    分析舆情数据, 获取评论总数、正向评价数量及比例
    （由于正负评论处理方法基本相同, 这里只处理正向评论）

    返回: 处理好的 df
    """

    # 获取各产品的评论总数和正向评价数
    df_with_total_num = df['name'].value_counts().rename_axis(
        'name').reset_index(name='total_num')
    df_with_positive_num = df[df['stmscore'] >= 0.5]['name'].value_counts(
    ).rename_axis('name').reset_index(name='positive_num')

    # 数据处理
    new_df = pd.merge(df_with_total_num, df_with_positive_num, how='outer')
    new_df['positive_pct'] = new_df['positive_num'] / new_df['total_num']
    new_df['positive_pct'] = new_df['positive_pct'].apply(
        lambda x: format(x, '.2%')
    )

    return df_to_json(new_df)


def get_chart_params(df):
    """
    获取线型图数据(横坐标、纵坐标、数据集)

    返回: [日期, 产品名称, 各产品每日评论数]
    """

    name_list = list({df['name'][i] for i in range(1, len(df))})
    date_list = sorted(list({df['date'][i] for i in range(1, len(df))}))

    counted_df = df.groupby(
        ['name', 'date'], as_index=False)['comment'].count()
    empty_df = pd.DataFrame({
        'name': [name for name in name_list for i in range(len(date_list))],
        'date': [date for i in range(len(name_list)) for date in date_list]
    })  # empty_df 用于处理 0 评论情况

    comment_count = list(pd.merge(
        empty_df, counted_df, how='outer', on=['name', 'date']
    ).fillna(0)['comment'])

    comment_num_list = [
        comment_count[i * len(date_list): (i + 1) * len(date_list)]
        for i in range(len(name_list))
    ]

    return [date_list, name_list, comment_num_list]
