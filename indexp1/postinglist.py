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
(venv) sunidhi_patange108@instance-chatbot-sp:~/chatbot-wiki/viz_app$ cat requirements.txt
cat: requirements.txt: No such file or directory
(venv) sunidhi_patange108@instance-chatbot-sp:~/chatbot-wiki/viz_app$ cd ..
(venv) sunidhi_patange108@instance-chatbot-sp:~/chatbot-wiki$ cat requirements.txt
streamlit
transformers
sentence-transformers
torch
numpy
pandas
altair
(venv) sunidhi_patange108@instance-chatbot-sp:~/chatbot-wiki$ cat postinglist_checkpoint.txt
618121(venv) sunidhi_patange108@instance-chatbot-sp:~/chatbot-wiki$ cd indexp1
(venv) sunidhi_patange108@instance-chatbot-sp:~/chatbot-wiki/indexp1$ ls
_pycache_  postinglist.py  preprocessing.py  utils.py
(venv) sunidhi_patange108@instance-chatbot-sp:~/chatbot-wiki/indexp1$ cat postinglist.py

import math


class PostingNode:
    def _init_(self, doc_id, tfidf=None):
        self.doc_id = doc_id
        self.tfidf = tfidf
        self.next = None
        self.skip = None


class PostingList:
    def _init_(self):
        self.head = None
        self.length = 0

    def insert(self, doc_id):
        
        new = PostingNode(doc_id)

        if self.head is None:
            self.head = new
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = new

        self.length += 1

    def to_list(self):
        out = []
        c = self.head
        while c:
            out.append(c.doc_id)
            c = c.next
        return out


def add_skip_pointers(pl: PostingList):
    L = pl.length
    if L <= 2:
        return

    skip_step = round(math.sqrt(L))
    if skip_step <= 1:
        return

    
    nodes = []
    curr = pl.head
    while curr:
        nodes.append(curr)
        curr = curr.next

    
    for i in range(0, L, skip_step):
        if i + skip_step < L:
