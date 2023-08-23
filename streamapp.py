import streamlit as st
import pandas as pd
import numpy as np
from streamlit_tags import st_tags, st_tags_sidebar
import json

#Load in JSON file
with open("/Users/chrisd456/Documents/Columbia Work/Summer 2023/Yale_Research/Web_Demo/table7.json") as f:
    data = json.load(f)
    df = pd.DataFrame.from_dict(pd.json_normalize(data), orient='columns')
    #df = df[1:]
    cols = df.columns.tolist()


data2_new = {}

#Load in JSONL file (generated results)
with open("/Users/chrisd456/Documents/Columbia Work/Summer 2023/Yale_Research/Web_Demo/predictions_step_0_rank_0.jsonl") as f:

    for line in f:
        data = json.loads(line)
        for key in data.keys():
            if key not in data2_new:
                data2_new[key] = [data[key]]
            else:
                data2_new[key].append(data[key])
            
    # data2 = json.load(f)
    # df2 = pd.DataFrame.from_dict(pd.json_normalize(data2), orient='columns')
    # #df = df[1:]
    # cols2 = df2.columns.tolist()


st.set_page_config(
    page_title="NLP Paper", 
    layout="wide")

#st.title("Few-shot Learning Results")

orgs = df[cols[0]].tolist()

data_new = {}

data_new["tags"]=[]
#for i in range(0, len[cols]):
#    temp=[]
#    for j in df[cols[]]

st.code(body="def remove_Occ(str,ch):\n  return str[1:-1]\n",
        language='python')
st.code(body="## Given the natural language description and example assertion(s), write a python function.\n\n### Task Start ###\n# These are the assertions for your function:\nassert similar_elements((3, 4, 5, 6),(5, 7, 4, 10)) == (4, 5)\n\n\"\"\" Write a function to find the similar elements from the given two tuple lists. \"\"\"\ndef similar_elements(test_tup1, test_tup2):\n  res = tuple(set(test_tup1) & set(test_tup2))\n  return (res) \n### Task End ###\n\n### Task Start ###\n# These are the assertions for your function:\nassert is_not_prime(2) == False\n\n\"\"\" Write a python function to identify non-prime numbers. \"\"\"\nimport math\ndef is_not_prime(n):\n    result = False\n    for i in range(2,int(math.sqrt(n)) + 1):\n        if n % i == 0:\n            result = True\n    return result\n### Task End ###\n\n### Task Start ###\n# These are the assertions for your function:\nassert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],3)==[85, 75, 65] \n\n\"\"\" Write a function to find the largest integers from a given list of numbers using heap queue algorithm. \"\"\"\nimport heapq as hq\ndef heap_queue_largest(nums,n):\n  largest_nums = hq.nlargest(n, nums)\n  return largest_nums\n### Task End ###\n\n### Task Start ###\n# These are the assertions for your function:\nassert remove_Occ(\"hello\",\"l\") == \"heo\"\n\n\"\"\" Write a python function to remove first and last occurrence of a given character from the string. \"\"\"",
        language="python")
#data_new["tags"]=orgs_tags
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


bullets="### :red[Organizations:] \n"
for i in orgs:
    bullets+=("* " + i + "\n")

st.sidebar.write(bullets)


#col1, col2, col3= st.columns(3)
col2, col3= st.columns(2)

#Select organization tags 
'''with col1:
#Show all possible organizations
    bullets="### :red[Organizations:] \n"
    for i in orgs:
        bullets+=("* " + i + "\n")
    st.write(bullets)'''
    
with col2:
    keywords = st_tags(
        label='Type which Organization(s) you would like to view:',
        text='Enter new Organizaiton name ',
        value=orgs,
        suggestions= orgs,
        key='1')
    
    for i in range (0, len(tags)):
        if (tags[i] not in keywords):
            df = df.drop(df.index[df["tags"] == tags[i]])


with col3:
    st.write("### :red[Select Columns To Show:]")

    options = cols[2:]
    checks = []

    for opt in options:
        checks.append(st.checkbox(opt))



for i in range(len(checks)):
    if checks[i] == False:
        df = df.drop(cols[i+2], axis=1)

st.dataframe(df, hide_index=True)
st.dataframe(df2, hide_index=True)
#df.drop(cols)


