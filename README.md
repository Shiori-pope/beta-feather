# 最小复现 Skill

这个仓库用于最小化复现以下流程：

- 生成接口参数 encrypted
- 重放 gettaskbyTypeCursor 请求

## 文件说明

- SKILL.md：Skill 使用说明
- replay_min.py：最小可运行脚本
- requirements.txt：依赖列表

## 快速开始

```bash
pip install -r requirements.txt
python replay_min.py
```

## 复现内容

- 加密算法：AES-128-ECB + PKCS7
- 明文结构：{"verify":"zzyq","c_time":"..."}
- 密文输出：大写十六进制
- 请求方式：POST application/x-www-form-urlencoded
- 目标接口：https://www.yqtech.ltd:8802/gettaskbyTypeCursor
