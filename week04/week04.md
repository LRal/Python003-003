# SQL 语句转换成 pandas 语句

1. `SELECT * FROM data;`

    ```python
    data
    ````

2. `SELECT * FROM data LIMIT 10;`

    ```python
    data[:10]
    ```

3. `SELECT id FROM data;`

   ```python
   data['id']
   ```

4. `SELECT COUNT(id) FROM data;`

    ```python
    data['id'].count()
    ```

5. `SELECT * FROM data WHERE id<1000 AND age>30;`

    ```python
    data[(data['id'] < 1000) & (data['age'] > 30)]
    ```

6. `SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;`

    ```python
    table1.groupby('id')['order_id'].nunique()
    ```

7. `SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;`

    ```python
    pd.merge(table1, table2, on='id')
    ```

8. `SELECT * FROM table1 UNION SELECT * FROM table2;`

    ```python
    pd.concat([table1, table2]).drop_duplicates()
    ```

9. `DELETE FROM table1 WHERE id=10;`

    ```python
    table1 = table1[~(table1['id'] == 10)]
    ```

10. `ALTER TABLE table1 DROP COLUMN column_name;`

    ```python
    table1.drop(columns='column_name', inplace=True)
    ```
