from apyori import apriori
import pandas as pd
import json

with open('data/club_posts_topic.json', 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

user_topics = {}

# 整理主題，每個用戶曾推薦過的主題
for entry in json_data:
    name = entry["name"]
    top_topic = entry["top_topic"]
    if name in user_topics:
        user_topics[name].add(top_topic)
    else:
        user_topics[name] = {top_topic}

result_data = [{"name": name, "topic": list(topics)} for name, topics in user_topics.items()]
result_data = [entry for entry in result_data if len(entry["topic"]) < 13]

# 建立關聯規則
dataset = [item['topic'] for item in result_data]
rules = apriori(transactions = dataset, min_support = 0.003, min_confidence = 0.2, min_lift = 3, min_length = 2, max_length = 2)
results = list(rules)

def inspect(results):
    lhs         = [tuple(result[2][0][0])[0] for result in results]
    rhs         = [tuple(result[2][0][1])[0] for result in results]
    supports    = [result[1] for result in results]
    confidences = [result[2][0][2] for result in results]
    lifts       = [result[2][0][3] for result in results]
    return list(zip(lhs, rhs, supports, confidences, lifts))
resultsinDataFrame = pd.DataFrame(inspect(results), columns = ['Left Hand Side', 'Right Hand Side', 'Support', 'Confidence', 'Lift'])

dataset = resultsinDataFrame.nlargest(n = 20, columns = 'Lift')
dataset.to_csv('data/associationRules.csv')