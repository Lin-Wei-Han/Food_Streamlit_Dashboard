#from bertopic import BERTopic
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import numpy as np
import json


with open('data/club_posts.json', 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

data = [item['word'] for item in json_data]

# 將文本轉換成 TF-IDF 特徵矩陣
tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(data)

# 使用 NMF 進行分解
num_topics = 18
nmf = NMF(n_components=num_topics, random_state=1)
nmf.fit(tfidf_matrix)

# 輸出個主題下的字詞
feature_names = tfidf_vectorizer.get_feature_names_out()
for topic_idx, topic in enumerate(nmf.components_):
    top_keywords_idx = topic.argsort()[:-10 - 1:-1]  # 取前 10 個詞
    top_keywords = [feature_names[i] for i in top_keywords_idx]
    all_keywords_idx = topic.argsort()[::-1] 
    all_keywords = [feature_names[i] for i in all_keywords_idx]
    topic_filename = f"topic/topic_{topic_idx + 1}.txt"
    with open(topic_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(all_keywords))
    print(f"主題 {topic_idx + 1}: {', '.join(top_keywords)}")

topic_distribution = nmf.transform(tfidf_matrix)
top_topic_indices = np.argmax(topic_distribution, axis=1)

# 根據主題下的字詞表現，調整主題名稱
topic_names = ["飯店", "火鍋", "海港海鮮", "燒肉", "牛排", "銅盤烤肉", "日式料理", "其他", "異國", "海鮮料理", "肉" ,"鍋物燒肉", "其他", "港式粵式", "拉麵", "韓式料理", "吃到飽", "泰式料理"]


for i, item in enumerate(json_data):
    item['top_topic'] = topic_names[top_topic_indices[i]]

with open('data/club_posts_topic.json', 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, ensure_ascii=False, indent=4)