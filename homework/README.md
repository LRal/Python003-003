# 作业完成情况

- [x] **正确使用 Scrapy 框架获取评论，如果评论有多页，需实现自动翻页功能。**
  - 通过爬取评论总数, 计算评论总页数, 获得评论 url
- [x] **评论内容能够正确存储到 MySQL 数据库中，不因表结构不合理出现数据截断情况。**
  - 数据表评论字段数据类型为 VARCHAR(1000), 与网站评论字数上限一致
- [x] **数据清洗后，再次存储的数据不应出现缺失值。**
  - 数据表所有字段设置 NOT NULL 属性, 无缺失值
- [x] **Django 能够正确运行，并展示采集到的数据，数据不应该有乱码、缺失等问题。**
  - Django 展示页采用与数据表相同的 utf8mb4 字符集, 能正常显示 emoji
- [x] **在 Django 上采用图表方式展示数据分类情况。**
  - 结合 Bootstrap Table 以表格形式展示评论数据
  - 使用 Chart.js 以线形图形式展示产品每日评论数量
- [x] **舆情分析的结果存入到 MySQL 数据库中。**
  - 在 pipeline 中实现
- [x] **在 Django 上采用图表方式展示舆情分析的结果。**
  - 结合 Bootstrap Table 展示舆情分析结果, 包括评价总数、积极评价数量及比例, 所有数据支持排序
- [ ] **可以在 Web 界面根据关键字或关键词进行搜索，并能够在页面展示正确的搜索结果。**
  - 引入 Bootstrap Table 搜索框, 实现搜索功能
- [ ] **支持按照时间（录入时间或评论时间）进行搜索，并能够在页面展示正确的搜索结果。**
  - 表格引入高级搜索插件, 支持所有字段搜索
  - 线型图与毕业项目参考示例大致一样
- [ ] **符合 PEP8 代码规范，函数、模块之间的调用高内聚低耦合，具有良好的扩展性和可读性。**
  - 使用 pylint, autopep8 辅助检查代码, 代码质量待老师检查。

## 部分截图

![评论数据][comments]
![评论数量][chart]  
![舆情分析][sentiments]

[comments]: https://github.com/LRal/Pics/blob/master/%E8%AF%84%E8%AE%BA%E6%95%B0%E6%8D%AE.png?raw=true
[chart]: https://github.com/LRal/Pics/blob/master/%E8%AF%84%E8%AE%BA%E6%95%B0%E9%87%8F.png?raw=true
[sentiments]: https://github.com/LRal/Pics/blob/master/%E8%88%86%E6%83%85%E5%88%86%E6%9E%90.png?raw=true
