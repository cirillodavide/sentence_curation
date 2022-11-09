# streamlit_app.py

import streamlit as st
from gsheetsdb import connect
from random import seed, sample
import pickle as pkle
import os.path

seed(1)
N = 2

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

if os.path.isfile('next.p'):
    next_clicked = pkle.load(open('next.p', 'rb'))
    if next_clicked == len(pages):
        next_clicked = 0 
else:
    next_clicked = 0 
    
if next:
    next_clicked = next_clicked+1
    if next_clicked == len(pages):
        next_clicked = 0 
    

choice = st.sidebar.radio("Pages",range(1,N+1), index=next_clicked)
pkle.dump(pages.index(choice), open('next.p', 'wb'))

st.title(str(choice))
#subset[choice-1]
st.write("Evaluate the number of males and females in the following sentences:")
st.subheader(rows[subset[choice-1]].Sentence)

st.write("Number of females")
number = st.text_input("Insert a number or NA", value="", key="female")
#st.write('The current number is ', number)

st.write("Number of males")
number = st.text_input("Insert a number or NA", value="", key="male")
#st.write('The current number is ', number)



#if choice == 1:
#    st.title('Page 1')
#elif choice == 'Page2':
#    st.title('Page 2')
#elif choice == 'Page3':
#    st.title('Page 3')

next = st.button('Go to next page')
    


