import streamlit_echarts
import streamlit as st
from streamlit_option_menu import option_menu
from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.charts import Bar
from collections import Counter
import streamlit.components.v1 as components
from pyecharts.globals import SymbolType
import pandas as pd
import json

with open('data/wordCloud.json', 'r', encoding='utf-8') as json_file:
    data_by_month = json.load(json_file)

with open('data/club_posts_topic.json', 'r', encoding='utf-8') as json_file:
    club_posts_topic = json.load(json_file)

top_topics = [item["top_topic"] for item in club_posts_topic]
topic_counts = Counter(top_topics)
topic_df = pd.DataFrame({"Topic": list(topic_counts.keys()), "Count": list(topic_counts.values())})

average_likes = []
for topic in topic_df["Topic"]:
    likes = [int(str(item["like"]).replace(",", "")) for item in club_posts_topic if item["top_topic"] == topic]
    average_like = sum(likes) / len(likes) if len(likes) > 0 else 0
    average_likes.append(average_like)
topic_df["Average Likes"] = average_likes

def generate_wordcloud(text_data, num_words):
    c = (
        WordCloud()
        .add("", text_data, word_size_range = [20, num_words], shape = SymbolType.DIAMOND)
    )
    return c

def generate_barChart():
    bar = (
        Bar()
        .add_xaxis(topic_df["Topic"].tolist())
        .add_yaxis("Topic Count", topic_df["Count"].tolist())
        .add_yaxis("Average Likes", topic_df["Average Likes"].tolist())
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(is_show = False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title = None),
            xaxis_opts=opts.AxisOpts(name = None),
            yaxis_opts=opts.AxisOpts(name = None),
        )
    )
    return bar

# st.set_page_config(layout="wide")
st.set_page_config(layout = "centered")

st.title('Facebook 美食社團分析')

selected = option_menu(
    menu_title = None,
    options = ['Network', 'Text Cloud', 'Bar Chart'],
    icons = ['box-fill', 'cloud-fill', 'bar-chart-fill'],
    menu_icon = 'cast',
    default_index = 0,
    orientation = 'horizontal'
)

if selected == 'Network':
    st.markdown('### 關聯規則網路圖')
    HtmlFile = open("templates/restaurant_network.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height = 800)

if selected == 'Text Cloud':
    st.markdown('### 每月關鍵字文字雲')
    st.markdown('利用提取字無詞頻結果，顯示每月份的社團內討論度最高的關鍵字，並以文字雲呈現，幫助小明參考選擇。')
    
    selected_month = st.selectbox("選擇月份", list(data_by_month.keys()))
    num_words = st.slider("選擇要顯示的詞語數量", min_value = 10, max_value = 100, value = 100)

    wordcloud_chart = generate_wordcloud(data_by_month[selected_month], num_words)

    streamlit_echarts.st_pyecharts(wordcloud_chart, height = "500px")

if selected == 'Bar Chart':
    st.markdown('### 美食類型推薦貼文統計')
    barChart_chart = generate_barChart()
    streamlit_echarts.st_pyecharts(barChart_chart, height = "700px")
