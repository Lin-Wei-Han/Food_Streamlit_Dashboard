from pyvis.network import Network
import pandas as pd

dataset = pd.read_csv('data/associationRules.csv')

net = Network(height="1200px", width="100%" )

left_items = set(dataset["Left Hand Side"])
right_items = set(dataset["Right Hand Side"])

lonely_item = ["飯店", "海港海鮮", "銅盤烤肉", "日式料理", "其他", "異國","鍋物燒肉","吃到飽"]

for item in lonely_item:
    net.add_node(item, title = item)

for item in left_items:
    net.add_node(item, title = item)

for item in right_items:
    net.add_node(item, title = item)


for index, row in dataset.iterrows():
    left = row["Left Hand Side"]
    right = row["Right Hand Side"]
    net.add_edge(left, right)

net.write_html("templates/restaurant_network.html")
