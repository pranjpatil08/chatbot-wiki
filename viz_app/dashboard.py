import json
import pandas as pd
import streamlit as st
import altair as alt

LOG_FILE = "data/logs/chat_history.jsonl"

rows = []
with open(LOG_FILE) as f:
    for line in f:
        rows.append(json.loads(line))

df = pd.DataFrame(rows)

st.title("Chatbot Analytics Dashboard")

st.subheader("Messages over time")
st.line_chart(df["ts"])

st.subheader("Topic Frequency")
topic_counts = df["topics"].explode().value_counts()
st.bar_chart(topic_counts)

st.subheader("Sample Conversations")
st.dataframe(df[["user","bot","topics"]].tail(20))
