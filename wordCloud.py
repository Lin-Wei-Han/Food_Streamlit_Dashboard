import json
from datetime import datetime
from collections import OrderedDict

# 轉換日期格式
def process_time(time_str):
    output_format = "%Y年%m月"
    if '年' in time_str:
        time_str = time_str.replace("上午", "AM").replace("下午", "PM")
        time_obj = datetime.strptime(time_str, "%Y年%m月%d日%p%I:%M")
        formatted_time = time_obj.strftime(output_format)
    elif "上午" in time_str or "下午" in time_str:
        time_str = time_str.replace("上午", "AM").replace("下午", "PM")
        time_obj = datetime.strptime(time_str, "%m月%d日%p%I:%M")
        time_obj = time_obj.replace(year=2023)
        formatted_time = time_obj.strftime(output_format)
    else:
        formatted_time = f"{datetime.now().year}年{datetime.now().month}月"
    return str(formatted_time)

# 計算詞頻
def wordFrequency(text):
    words = text.split()
    word_count = {}

    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    word_count_list = [(word, count) for word, count in word_count.items()]
    word_count_list.sort(key=lambda x: x[1], reverse=True)
    return word_count_list

with open('data/club_posts.json', 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

for row in json_data:
    row['createAt'] = process_time(row['createAt'])

grouped_text = {}

for item in json_data:
    createAt = item["createAt"]
    word = item["word"]
    if createAt in grouped_text:
        grouped_text[createAt] += " " + word
    else:
        grouped_text[createAt] = word


for item in grouped_text:
    grouped_text[item] = wordFrequency(grouped_text[item])

# 依日期排序字典順序
grouped_text = OrderedDict(sorted(grouped_text.items(), key=lambda x: datetime.strptime(x[0], "%Y年%m月"), reverse=True))

with open('data/wordCloud.json', 'w', encoding='utf-8') as json_file:
    json.dump(grouped_text, json_file, ensure_ascii=False, indent=4) 