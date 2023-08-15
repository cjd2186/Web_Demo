import streamlit as st
import pandas as pd
import numpy as np

import json

#Load in JSON file
with open("C:\\Users\\vedan\\Yale\\College Research Work\\LILY Research\\Data\\table7.json") as f:
    data = json.load(f)
    df = pd.DataFrame.from_dict(pd.json_normalize(data), orient='columns')
    #df = df[1:]
    cols = df.columns.tolist()


st.title("Few-shot Learning Results")


print(df[cols[0]])


orgs = df[cols[0]].tolist()
# orgs.insert(0, ' ')

data_new = {}

for i in range(1, len(cols)):
    temp = []

    for n in df[cols[i]].tolist():
        for m in n:
            temp.append(m)
    
    data_new[cols[i]] = temp

print(data_new)

df = pd.DataFrame(data_new)



# option = st.selectbox(
#     'What organization would you like to look at?',
#     tuple(orgs))


options = cols[2:]
checks = []

for opt in options:
    checks.append(st.checkbox(opt))

# print(cols)

# print(cols)
# print(orgs) 



# df[cols[1]] = models


for i in range(len(checks)):
    if checks[i] == False:
        df = df.drop(cols[i+2], axis=1)

st.dataframe(df, hide_index=True)
#df.drop(cols)


