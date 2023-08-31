import streamlit as st
import pandas as pd
import numpy as np
from streamlit_tags import st_tags, st_tags_sidebar
from streamlit_extras.switch_page_button import switch_page

import json

#Load in JSON file
with open("/Users/chrisd456/Documents/Columbia Work/Summer 2023/Yale_Research/Web_Demo/table7.json") as f:
    data = json.load(f)
    df = pd.DataFrame.from_dict(pd.json_normalize(data), orient='columns')
    #df = df[1:]
    cols = df.columns.tolist()


data2_new = {}

#Load in JSONL file (generated functions)
with open("/Users/chrisd456/Documents/Columbia Work/Summer 2023/Yale_Research/Web_Demo/predictions_step_0_rank_0.jsonl") as f:

    for line in f:
        data = json.loads(line)
        for key in data.keys():
            if key not in data2_new:
                data2_new[key] = [data[key]]
            else:
                data2_new[key].append(data[key])

st.set_page_config(
    page_title="NLP Paper", 
    layout="wide")

st.title("Few-shot Learning Results")

orgs = df[cols[0]].tolist()

data_new = {}

data_new["tags"]=[]
#arrange table 7 by model name, add org as a tag
for i in range(1, len(cols)):
    temp = []

    for n in df[cols[i]].tolist():
        for m in n:
            temp.append(m)
    data_new[cols[i]] = temp

#add Organization tag to each model
tags=[]
orgs_mods=[]
for i in range(0, len(df[cols[0]])):
    print(df[cols[0]][i])
    org_names=[df[cols[0]][i]]
    model_names=df[cols[1]].tolist()[i]
    orgs_mods.append(org_names + model_names)

for model in data_new[cols[1]]:
    for i in range(0, len(orgs_mods)):
        if model in orgs_mods[i]:
            tags.append(orgs_mods[i][0])

data_new["tags"]=tags



df = pd.DataFrame(data_new)
df2 = pd.DataFrame(data2_new)


#Sidebar
keywords = st_tags_sidebar(
    label='Type which Organization(s) you would like to view:',
    text='Enter new Organizaiton name ',
    value=orgs,
    suggestions= orgs,
    key='1')

for i in range (0, len(tags)):
    if (tags[i] not in keywords):
        df = df.drop(df.index[df["tags"] == tags[i]])


#checkboxes for datasets
st.sidebar.write("### :red[Select Datasets To Show:]")

options = cols[2:]
checks = []
for opt in options:
    checks.append(st.sidebar.checkbox(opt, value=True))

#orgnaization list
bullets="### :red[Organizations:] \n"
for i in orgs:
    bullets+=("* " + i + "\n")
st.sidebar.write(bullets)


#show selected rows and columns
for i in range(len(checks)):
    if checks[i] == False:
        df = df.drop(cols[i+2], axis=1)

st.dataframe(df, hide_index=True)
st.dataframe(data2_new)

#buttons to switch to each model
starcoder = st.button("StarCoder-15.5B")
if starcoder:
    switch_page("StarCoder-15.5B")