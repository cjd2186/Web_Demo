import streamlit as st
import pandas as pd
import numpy as np
from streamlit_tags import st_tags, st_tags_sidebar
import json

def main():
    #Load in JSON file
    with open("/Users/chrisd456/Documents/Columbia Work/Summer 2023/Yale_Research/Web_Demo/table7.json") as f:
        data = json.load(f)
        df = pd.DataFrame.from_dict(pd.json_normalize(data), orient='columns')
        cols = df.columns.tolist()

    mbpp_df = {}
    #Load in JSONL file (generated functions)
    with open("/Users/chrisd456/Documents/Columbia Work/Summer 2023/Yale_Research/Web_Demo/predictions_step_0_rank_0.jsonl") as f:

        for line in f:
            data = json.loads(line)
            for key in data.keys():
                if key not in mbpp_df:
                    mbpp_df[key] = [data[key]]
                else:
                    mbpp_df[key].append(data[key])

    st.set_page_config(
        page_title="NLP Paper", 
        layout="centered")

    st.title("StarCoder-15.5B Model")

#check box to load specific datapage
    st.sidebar.write("### :red[Select Dataset Examples:]")
    options = cols[2:]

    choice=st.sidebar.radio('Select Dataset Examples:', options)

    if choice == cols[2]:
        spider2()
    if choice == cols[3]:
        wikitq2()
    if choice == cols[4]:
        gsm8k8()
    if choice == cols[5]:
        mbpp3(mbpp_df)
    if choice == cols[6]:
        mwr()

def spider2():
    return None

def wikitq2():
    return None

def gsm8k8():
    return None

def mbpp3(mbpp_df):
    """tests=['passed tests only', 'failed tests only', 'all examples']
    choice=st.sidebar.radio('Select Dataset Examples:', tests)
    
    passed=True
    failed=True

    if choice== tests[0]:
        passed=True
        failed=False
    if choice== tests[1]:
        passed=False
        failed=True"""
    
    y=mbpp_df['metadata']
    x=mbpp_df["generated_program"]

    functions=[]
    prpts=[]
    func_sigs=[]
    
    #list of text and program as a string
    for i in range (0, len(mbpp_df['metadata'])):
        z="# "+ y[i]["text"]
        z+="\n"+ x[i]["program"]
        prpt= y[i]["prompt"]
        func_sig= y[i]["func_signature"]
        func_sigs.append(func_sig)
        functions.append(z)
        prpts.append(prpt)

    #list of test cases, and if they were passed
    
    current_page = st.session_state.get("current_page", 1)
    results_ppg=10
    total_pgs = (len(functions) + results_ppg - 1) // results_ppg


    #pagination navigation
    user_input= st.number_input(
        label= f"Enter page number between 1 and {total_pgs}",
        min_value=1,
        max_value=total_pgs,
        step=1
        )
    
    try:
        current_page=int(user_input)
    except ValueError:
        st.write("Input is not a valid integer.")

    start= (current_page -1) * results_ppg
    end= min(start+ results_ppg, len(functions))

    #display function definitions and prompts
    prmpt_funcs=[functions[start:end], prpts[start:end]]
    sigs=func_sigs[start:end]  
    for i in range(0, len(functions[start:end])):
        st.markdown(f"### Function {10*(current_page -1) + i}")
        with st.expander(f":red[Function {sigs[i]}]", expanded=True):
            st.code(body=prmpt_funcs[0][i],
                    language= "python")
        with st.expander(f":blue[Prompt {sigs[i]}]"):
            st.code(body=prmpt_funcs[1][i],
                    language= "python")
        
    st.session_state.current_page = current_page

def mwr():
    return None

if __name__ == "__main__":
    main()