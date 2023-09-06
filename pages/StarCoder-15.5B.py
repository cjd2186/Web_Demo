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

    mbpp_dict = {}
    #Load in JSONL file (generated functions)
    with open("/Users/chrisd456/Documents/Columbia Work/Summer 2023/Yale_Research/Web_Demo/predictions_step_0_rank_0.jsonl") as f:

        for line in f:
            data = json.loads(line)
            for key in data.keys():
                if key not in mbpp_dict:
                    mbpp_dict[key] = [data[key]]
                else:
                    mbpp_dict[key].append(data[key])

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
        mbpp3(mbpp_dict)
    if choice == cols[6]:
        mwr()

def spider2():
    return None

def wikitq2():
    return None

def gsm8k8():
    return None

def mbpp3(mbpp_dict):
    tests=['passed tests only', 'failed tests only', 'all examples']
    choice=st.sidebar.radio('Select Dataset Examples:', tests)
    
    passed=True
    failed=True

    x=mbpp_dict["generated_program"]
    y=mbpp_dict['metadata']


    passed_tests= mbpp_dict
    failed_tests= mbpp_dict

    assertions=[]
    results= []
    if choice == tests[0]:
        passed=True
        failed=False
        st.write("PASSED")

        i=0 
        length=len(passed_tests['metadata'])
        #iterate through the function examples
        while i < length:
            #determine which assertions to display, assume all passed
            tests=[1, 1, 1]

            #iterate through list of tests cases in exec_result
            exec_acc= x[i]["exec_acc"]
            
            #see if test failed, take out of passed tests dict
            #only want passed_tests to have function information for passed tests
            if (exec_acc == 0):
                del (passed_tests["generated_program"][i])
                del (passed_tests["metadata"][i])
            
            else:
                #compute which test cases were passed, want to show which assertions passed too
                for j in range(0,3):
                    result= x[i]["exec_result"][j]["result"]
                    #check for failed tests
                    if (result != "passed"):
                        tests[j] = 0  
                                      
                
                    #add passed result and assertion
                    if (tests[j]== 1):
                        assertion= y[i]["test_list"][j]
                        result= x[i]["exec_result"][j]["result"]
                        assertions.append(assertion)
                        results.append(result)
            
            length = len(passed_tests['metadata'])
            i+=1



    if choice== tests[1]:
        passed=False
        failed=True
        st.write("FAILED")

        i=0 
        length=len(failed_tests['metadata'])
        #iterate through the function examples
        while i < length:
            #determine which assertions to display, assume all failed
            tests=[0, 0, 0]

            #iterate through list of tests cases in exec_result
            exec_acc= x[i]["exec_acc"]
            
            #see if test failed, take out of passed tests dict
            #only want failed to have function information for failed tests
            if (exec_acc == 1):
                del (failed_tests["generated_program"][i])
                del (failed_tests["metadata"][i])
            
            else:
                #compute which test cases were failed, want to show which assertions failed too
                for j in range(0,3):
                    result= x[i]["exec_result"][j]["result"]                                    
                
                    #check for failed tests
                    if (result == "passed"):
                        tests[j] = 1

                    #add failed result and assertion
                    if (tests[j]== 0):
                        assertion= y[i]["test_list"][j]
                        result= x[i]["exec_result"][j]["result"]
                        assertions.append(assertion)
                        results.append(result)
            
            length = len(failed_tests['metadata'])
            i+=1

    functions=[]
    prpts=[]
    func_sigs=[]
    
    #list of text and program as a string
    for i in range (0, len(mbpp_dict['metadata'])):
        z="# "+ y[i]["text"]
        z+="\n"+ x[i]["program"]
        prpt= y[i]["prompt"]
        func_sig= y[i]["func_signature"]
        func_sigs.append(func_sig)
        functions.append(z) 
        prpts.append(prpt)
        if (choice == tests[2]):
            for j in range(0,3):
                assertion= y[i]["test_list"][j]
                result= x[i]["exec_result"][j]["result"]
                assertions.append(assertion)
                results.append(result)

    #list of test cases, and if they were passed
    
    current_page = st.session_state.get("current_page", 1)
    results_ppg=10
    #total_pgs = (len(functions) + results_ppg - 1) // results_ppg
    total_pgs = ((len(results))//3 + results_ppg - 1) // results_ppg


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
    tests_results= [assertions[start:end], results[start:end]]

    for i in range(0, len(functions[start:end])):
    #for i in range(0, len(tests_results[start:end])):
        st.markdown(f"### Function {10*(current_page -1) + i}")
        with st.expander(f":red[Function {sigs[i]}]", expanded=True):
            st.code(body=prmpt_funcs[0][i],
                    language= "python")
        with st.expander(f":blue[Prompt {sigs[i]}]"):
            st.code(body=prmpt_funcs[1][i],
                    language= "python")
        with st.expander(":violet[Tests and Results]"):
            for i in range(0, 3):
                st.markdown(f":green[Test] {i}")
                st.code(body=tests_results[0][i],
                        language="python")
                st.markdown(f":orange[Result] {i}")
                st.code(body=tests_results[1][i],
                        language="python")
            
    st.session_state.current_page = current_page

def mwr():
    return None

if __name__ == "__main__":
    main()