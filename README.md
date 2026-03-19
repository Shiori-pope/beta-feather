# 北理贝塔驿站帖子浏览 Skill

这个仓库是一个可复用的 Skill，用于让 agent 浏览北理贝塔驿站帖子。

核心能力：

- 浏览帖子列表（按板块、排序、翻页）
- 查看单帖详情
- 自动生成接口所需 encrypted 参数

## 文件说明

- SKILL.md：Skill 说明与使用约定
- replay_min.py：帖子浏览脚本（列表 + 详情）
- requirements.txt：依赖列表

## 快速开始

```bash
pip install -r requirements.txt
python replay_min.py --tab all --sort 0 --pages 1
```

## 常用示例

1. 浏览全部帖子（新发）

```bash
python replay_min.py --tab all --sort 0 --pages 1
```

2. 浏览“倾诉”板块（最热）并拉取 2 页

```bash
python replay_min.py --tab qingsu --sort 2 --pages 2
```

3. 查看指定帖子详情

```bash
python replay_min.py --detail-id 797786
```

## 技术说明

- 接口域名：https://www.yqtech.ltd:8802
- 列表接口：POST /gettaskbyTypeCursor
- 详情接口：GET /gettaskbyId
- 加密算法：AES-128-ECB + PKCS7
- 密文格式：大写十六进制
