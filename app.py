import streamlit as st
import pandas as pd
import numpy as np

import json

st.set_page_config(page_title="NLP 4 Code", layout="wide")

st.subheader("Table 7")
#Load in JSON file
with open("/Users/chrisd456/Documents/Columbia Work/Summer 2023/Yale_Research/Web_Demo/table7.json") as f:
    data = json.load(f)
    df = pd.DataFrame.from_dict(pd.json_normalize(data), orient='columns')
    columns=df.columns.tolist()
    st.dataframe(df, hide_index=True)

st.title("Few-shot Learning Results")

#checkboxes of relevance
orgs=df[columns[0]].tolist()
orgs.insert(0, '')
option = st.selectbox(
    'What organization would you like to look at?',
    (tuple(orgs)))

if option != ' ':
    #hardcoded?
    #list of bools
    options=[]
    for item in columns[2:]:
        options.append(st.checkbox(item))

    columns=columns[2:]
    for i in range(0, len(options)):
        if not options[i]:
            df=df.drop(columns[i], axis=1)
    st.dataframe(df, hide_index=True)