import json
import os
from datetime import datetime

# =================配置区域=================
# 定义每日更新的主题 (0=周一, 6=周日)
# 必须和 queue.json 里的 "category" 字段完全匹配
WEEKLY_SCHEDULE = {
    0: "Training",    # Monday
    1: "Nutrition",   # Tuesday
    2: "Sleep",       # Wednesday
    3: "Recovery",    # Thursday
    4: "Mindset",     # Friday
    5: "Supplements", # Saturday
    6: None           # Sunday (Rest Day)
}
# =========================================

def publish_daily_issue():
    print("🚀 开始执行每日发布任务...")
    
    # 1. 获取今天是周几 (0-6)
    weekday = datetime.now().weekday()
    target_category = WEEKLY_SCHEDULE.get(weekday)
    
    if target_category is None:
        print(f"😴 今天是周日 (Rest Day)，不进行更新。")
        return

    print(f"📅 今天是周{weekday + 1}，目标分类: [{target_category}]")

    # 2. 读取囤货库 (Queue)
    if not os.path.exists('queue.json'):
        print("❌ 错误：找不到 queue.json 文件")
        return

    with open('queue.json', 'r', encoding='utf-8') as f:
        queue = json.load(f)

    if len(queue) == 0:
        print("⚠️ 警告：库存已空！")
        return

    # 3. 查找符合目标分类的第一篇文章
    article_to_publish = None
    remaining_queue = []
    
    # 遍历队列寻找匹配项
    for article in queue:
        # 如果还没找到匹配项，且分类符合 -> 选中它
        if article_to_publish is None and article.get('category') == target_category:
            article_to_publish = article
        else:
            # 其他文章放回剩余队列
            remaining_queue.append(article)

    # 4. 如果没找到对应分类的文章
    if article_to_publish is None:
        print(f"⚠️ 警告：库存里没有分类为 '{target_category}' 的文章！跳过今日更新。")
        # 这里我们选择不更新，保持 queue 不变（或者你可以逻辑改为随机发一篇）
        return

    # 5. 处理发布逻辑
    # 打上今天的发布日期
    today_str = datetime.now().strftime("%Y-%m-%d")
    article_to_publish['publishDate'] = today_str
    
    print(f"✅ 选中文章: {article_to_publish.get('title_en')} ({article_to_publish.get('title_zh')})")

    # 读取现有的 Feed
    if os.path.exists('feed.json'):
        with open('feed.json', 'r', encoding='utf-8') as f:
            current_feed = json.load(f)
    else:
        current_feed = []

    # 把新文章插入到最前面 (置顶)
    current_feed.insert(0, article_to_publish)

    # 6. 保存文件 (写入 Feed，更新 Queue)
    with open('feed.json', 'w', encoding='utf-8') as f:
        json.dump(current_feed, f, indent=2, ensure_ascii=False)

    with open('queue.json', 'w', encoding='utf-8') as f:
        json.dump(remaining_queue, f, indent=2, ensure_ascii=False)

    print(f"🎉 发布成功！feed.json 已更新，queue.json 已移除该文章。")

if __name__ == "__main__":
    publish_daily_issue()
