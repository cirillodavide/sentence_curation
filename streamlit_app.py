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


seed(1)
N = 12

# Create a connection object.
conn = connect()

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
#@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["public_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

subset = sample(range(0,len(rows)), N)
#st.write("Subset")
#subset

# Print results.
#for row in rows:
#    st.write(f"{row.Sentence} has :{row.N_women}: number of women")

pages = range(1,N+1)

st.title("Dear #Biohackathon2022,")
st.subheader("Please evaluate the number of males and females in the following sentences:")
#st.write("Please evaluate the number of males and females in the following sentences:")
st.write("- If you are in doubt, put NA:")
st.write("- If there is a percentage, add % at the end of the number (e.g. 5%)")
#st.write("Thanks!")
    
df = pd.DataFrame(columns = ['ID', 'Nfemale', 'Nmale'] )

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
    
    new_row = [crow.ID, Nfemale, Nmale]
#    new_row
#    df = df.append(new_row, ignore_index=True)
    
    df.loc[len(df)] = new_row
#    df

    
if st.button('Send'):
    outfile = os.path.join(setupBaseDir, "output.csv")
    df.to_csv(outfile, mode='a', index=False, header=False) 
    st.write('Thank you for your help!')
#df.columns = ['ID', 'Nfemale', 'Nmale']  

#df.to_csv('output.csv', mode='a', index=False, header=False) 
    

    
    

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
