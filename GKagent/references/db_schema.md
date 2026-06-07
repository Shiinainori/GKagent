# 数据库 Schema 参考

## 表：admission_data（录取数据表）

浙江省普通类"专业+学校"录取数据，每行代表一个可填报志愿单位。

| 字段 | 类型 | 说明 |
|------|------|------|
| province | VARCHAR(10) | 省份，固定为"浙江" |
| school_code | VARCHAR(10) | 学校代号 |
| school_name | VARCHAR(100) | 学校名称 |
| major_code | VARCHAR(10) | 专业代号 |
| major_name | VARCHAR(100) | 专业名称 |
| subject_requirement | VARCHAR(50) | 选考科目要求，如"物理必选"、"物理+化学"、"不限" |
| plan_count | INT | 计划招生数 |
| score | INT | 往年录取分数 |
| rank | INT | 往年录取位次 |

## 表：rank_table（一分一段表）

| 字段 | 类型 | 说明 |
|------|------|------|
| province | VARCHAR(10) | 省份，固定为"浙江" |
| year | INT | 年份 |
| score | INT | 分数 |
| rank | INT | 累计位次 |
| count | INT | 该分人数 |
