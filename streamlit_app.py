# streamlit_app.py

import streamlit as st
from gsheetsdb import connect
from random import seed, sample
import pickle as pkle
import os.path
import pandas as pd
import os
import sys
setupBaseDir = os.path.dirname(__file__)
sys.path.insert(0, setupBaseDir)


#seed(1)
N = 12

# Create a connection object.
conn = connect()

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
#@st.cache(ttl=600)
#@st.cache
#@st.experimental_memo(suppress_st_warning=True)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["public_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

#@st.experimental_memo(suppress_st_warning=True)
def get_sample():
    subset = sample(range(0,len(rows)), N)
    #st.write("Subset")
    #subset
    return(rows,subset)
    
#def save_df(df):
#    outfile = os.path.join(setupBaseDir, "output.csv")
#    df.to_csv(outfile, mode='a', index=False, header=False)
#    st.write("Thank you!")
#    

if 'state' not in st.session_state:
    st.session_state.state = 'init'
    rows,subset = get_sample()
else:
    rows = rows
    subset = subset

"SUBSET"    
subset

    
st.title("Dear #Biohackathon2022,")
st.subheader("Please evaluate the number of males and females in the following sentences:")
#st.write("Please evaluate the number of males and females in the following sentences:")
st.write("- If you are in doubt, put NA:")
st.write("- If there is a percentage, add % at the end of the number (e.g. 5%)")
#st.write("Thanks!")
df = pd.DataFrame(columns = ['ID', 'Nfemale', 'Nmale'] )    
        
with st.form(key='my_form', clear_on_submit=True):

    for k in range(1,N+1):
        st.title(str(k))
        crow = rows[subset[k-1]]
        #subset[choice-1]
        st.subheader(crow.Sentence)
        
        st.write("Number of females")
        Nfemale = st.text_input("Insert a number or NA", value="", key="female"+str(k))
    #    st.write('The current number is ', Nfemale)
        
        st.write("Number of males")
        Nmale = st.text_input("Insert a number or NA", value="", key="male"+str(k))
    #    st.write('The current number is ', Nmale)
        
        new_row = [str(int(crow.PreID)) + str(crow.ID), Nfemale, Nmale]

        st.write(str(int(crow.PreID)) + str(crow.ID))
        st.write(new_row)
        
        df.loc[len(df)] = new_row
          
    #    df
    submit_button = st.form_submit_button(label='Submit') # submit_button = st.form_submit_button(label='Submit', on_click=save_df, args=(df,))
    if submit_button:
        outfile = os.path.join(setupBaseDir, "output.csv")
        df.to_csv(outfile, mode='a', index=False, header=False)
        st.write("Thank you!")
    
#if submit_button:
#        outfile = os.path.join(setupBaseDir, "output.csv")
#        df.to_csv(outfile, mode='a', index=False, header=False)
#        st.write("Thank you!")

with open("output.csv") as f:
       st.download_button('', f)  # Defaults to 'text/plain' 

#if st.button('Send'):
#    df.to_csv(outfile, mode='a', index=False, header=False) 
    
#df.columns = ['ID', 'Nfemale', 'Nmale']  
   
# Try again
#You can check .empty documentation
placeholder = st.empty()

# Refresh
with placeholder.container():
    st.title("Would you like to try again?")
    btn = st.button("Go!")

if btn:
    #This would empty everything inside the container
    placeholder.empty()
    

st.write("\n\n"); st.write("\n\n"); st.write("\n\n"); st.write("\n\n")



    

    
    

#if os.path.isfile('next.p'):
#    next_clicked = pkle.load(open('next.p', 'rb'))
#    if next_clicked == len(pages):
#        next_clicked = 0 
#else:
#    next_clicked = 0  
#
#if next:
#    next_clicked = next_clicked+1
#    if next_clicked == len(pages):
#        next_clicked = 0
#
#
#choice = st.sidebar.radio("Pages",range(1,N+1), index=next_clicked)
#pkle.dump(pages.index(choice), open('next.p', 'wb'))
#
#st.title(str(choice))
##subset[choice-1]
#st.write("Evaluate the number of males and females in the following sentences:")
#st.subheader(rows[subset[choice-1]].Sentence)
##if choice == 1:
##    st.write("Number of females")
##    number = st.text_input("Insert a number or NA", value="", key="female")
##    st.write('The current number is ', number)
##    
##    st.write("Number of males")
##    number = st.text_input("Insert a number or NA", value="", key="male")
##    st.write('The current number is ', number)
##elif choice == 2:
##    st.write("Number of females")
##    number = st.text_input("Insert a number or NA", value="", key="female")
##    st.write('The current number is ', number)
##    
##    st.write("Number of males")
##    number = st.text_input("Insert a number or NA", value="", key="male")
##    st.write('The current number is ', number)
#
#
#st.write("Number of females")
#number = st.text_input("Insert a number or NA", value="", key="female")
#st.write('The current number is ', number)
#
#st.write("Number of males")
#number = st.text_input("Insert a number or NA", value="", key="male")
#st.write('The current number is ', number)
#
#def clear_text():
#    st.session_state["female"] = ""
#    st.session_state["male"] = ""
#
#next = st.button('Go to next page', on_click=clear_text)
#
#
#    
#
#
