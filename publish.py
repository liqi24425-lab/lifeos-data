import json
import os
from datetime import datetime

# 1. 读取“囤货库” (Queue)
with open('queue.json', 'r', encoding='utf-8') as f:
    queue = json.load(f)

if len(queue) == 0:
    print("没有存货了！")
    exit()

# 2. 取出最新的一篇
new_article = queue.pop(0)
new_article['publishDate'] = datetime.now().strftime("%Y-%m-%d") # 打上今天的时间戳

# 3. 读取“现有的信息流” (Feed)
# 如果文件不存在（第一次运行），就创建一个空列表
if os.path.exists('feed.json'):
    with open('feed.json', 'r', encoding='utf-8') as f:
        current_feed = json.load(f)
else:
    current_feed = []

# 4. 【关键步骤】把新文章插到最前面 (Prepend)
current_feed.insert(0, new_article)

# 5. 保存回 feed.json
with open('feed.json', 'w', encoding='utf-8') as f:
    json.dump(current_feed, f, indent=2, ensure_ascii=False)

# 6. 更新囤货库
with open('queue.json', 'w', encoding='utf-8') as f:
    json.dump(queue, f, indent=2, ensure_ascii=False)

print(f"成功发布并归档: {new_article['title']}")
