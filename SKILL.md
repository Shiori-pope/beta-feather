# 北理贝塔驿站帖子浏览 Skill

## 目标

用于让 agent 通过北理贝塔驿站接口浏览帖子，支持：

- 列表浏览（分类 + 排序 + 翻页）
- 单帖详情查看

## 入口脚本

- replay_min.py

## 支持参数

- --tab：帖子板块，可选 all/tucao/qingsu/xinyuan/zhihu
- --sort：排序类型，默认 0
	- 0: 新发
	- 1: 新回
	- 2: 最热
	- 3: 精选
- --pages：连续拉取页数
- --start-cursor：起始游标，默认 9999999
- --detail-id：指定后走详情接口，忽略列表参数
- --insecure：关闭 TLS 证书校验

## 接口约定

1. 列表接口：POST /gettaskbyTypeCursor
2. 详情接口：GET /gettaskbyId
3. encrypted 生成：
	 1. 构造对象 {"verify":"zzyq","c_time":"<ISO时间>"}
	 2. JSON 紧凑序列化
	 3. AES-128-ECB + PKCS7
	 4. 转大写十六进制

## 输出建议

- 列表模式默认输出精简字段：id、时间、板块、标题、作者、互动计数
- 详情模式输出完整 JSON，便于 agent 深入分析内容
