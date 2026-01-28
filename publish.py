import json
import os
from datetime import datetime

# 1. 读取“囤货库”
with open('queue.json', 'r', encoding='utf-8') as f:
    queue = json.load(f)

# 检查还有没有存货
if len(queue) == 0:
    print("没有存货了！请补货！")
    exit()

# 2. 取出第一篇 (Pop the first item)
todays_article = queue.pop(0)

# 给它打上今天的日期戳 (可选，如果你想强制覆盖日期)
todays_article['publishDate'] = datetime.now().strftime("%Y-%m-%d")

# 3. 写入“前台文件” (daily.json)
with open('daily.json', 'w', encoding='utf-8') as f:
    json.dump(todays_article, f, indent=2, ensure_ascii=False)

# 4. 更新“囤货库” (把发过的删掉)
with open('queue.json', 'w', encoding='utf-8') as f:
    json.dump(queue, f, indent=2, ensure_ascii=False)

print(f"成功发布: {todays_article['title']}")
