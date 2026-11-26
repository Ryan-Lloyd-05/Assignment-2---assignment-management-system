import streamlit as st
import sqlite3
import pandas as pd
import json

#if your not running the code through streamlit community cloud
#to run the code you have to enter the file loction into command prompt by dragging in and typing streamlit run before it
#(example) C:\Users\Ryanw>streamlit run "C:\Users\Ryanw\Stuff\Uni stuff\Assignmnet 2 code.py"
def create_account():
  
  user = st.text_input("create a username:")
  password = st.text_input("create a password:", type="password")
  if st.button("Create account"):
    with open("accounts.txt", "a") as file:
      file.write(f"{user},{password}\n")
      st.session_state["current_user"] = user
    st.session_state["account"] = True
    st.toast("account created")
    st.session_state["menu"] = False

 
def login_account():
  
  user_check = st.text_input("enter username:")
  password_check = st.text_input("enter password:", type="password")
  if st.button("Login"):
    with open("accounts.txt") as file:
      for line in file:
        user, password = line.strip().split(",")

        if user == user_check and password == password_check:
          st.toast("login successful")
          st.session_state["current_user"] = user_check
          st.session_state["log_in"] = True
          st.session_state["menu"] = False
          return
    st.toast("login failed")
  
def upload_file():
  uploaded_file = st.file_uploader("select the file you want to upload")

  if uploaded_file is None:
    
    st.session_state["file_name"] = []
    st.session_state["file_data"] = []
  
  
  if uploaded_file is not None:

    st.session_state["file_name"] = uploaded_file.name
    st.session_state["file_data"] = uploaded_file.getvalue()
    
    st.session_state["file"] = True

  if st.session_state.get("file"):
    st.download_button(st.session_state["file_name"],st.session_state["file_data"],st.session_state["file_name"])
    

def create_checklist():

  if "checklists" not in st.session_state:
    st.session_state["checklists"] = []
  
  task = st.text_input("write task", key="checklist")
  if st.button("create checklist"):
    st.session_state["checklists"].append(f"{task}")

  for i in range(len(st.session_state["checklists"])):
    
    st.checkbox(st.session_state["checklists"][i], key=f"checkbox_{i}")


def create_deadlines():
   
  if st.session_state["file"] == True:

    if "deadlines" not in st.session_state:
      st.session_state["deadlines"] = []
    
    file_list = (st.session_state["file_name"])
    tasks = st.selectbox("select file", file_list, key="deadline_task")
    deadline = st.text_input("enter a deadline:", key="deadline")
    if st.button("Add deadline"):
      st.session_state["deadlines"].append(f"{tasks}: {deadline}")
      
      st.write(st.session_state["deadlines"])
  
    
    


# main code

st.header ("Assignment management system")

if "menu" not in st.session_state:
  
  answer = st.radio("",["create account", "login"])


  if answer == "create account":
    create_account()
  elif answer == "login":
    login_account()



if st.session_state.get("log_in") or st.session_state.get("account"):
  

  choice_a = st.selectbox("what would you like to do?",["upload file", "create checklist", "create deadlines"])
  
  if choice_a == "upload file":
    upload_file()
  elif choice_a == "create checklist":
    create_checklist()
  elif choice_a == "create deadlines" and "file" not in st.session_state:
    st.write("please upload a file first")
  elif choice_a == "create deadlines":
    create_deadlines()

with open("accounts.txt") as file:
  for line in file:
    user, password = line.strip().split(",")

if "file_name" not in st.session_state:
  st.session_state["file_name"] = []
if "file_data" not in st.session_state:
  st.session_state["file_data"] = []
if "checklists" not in st.session_state:
  st.session_state["checklists"] = []
if "deadlines" not in st.session_state:
  st.session_state["deadlines"] = []



if "current_user" in st.session_state and st.button("Save"):

  conn = sqlite3.connect("info.db")
  
  conn.execute("""
  INSERT INTO info (user_1, file_name_1, file_data_1, checklist_1, deadline_1)
  VALUES (?, ?, ?, ?, ?)
  """, (st.session_state["current_user"], json.dumps(st.session_state["file_name"]), json.dumps(st.session_state["file_data"]), json.dumps(st.session_state["checklists"]), json.dumps(st.session_state["deadlines"])))
    
  conn.commit()
    
  data = pd.read_sql_query("SELECT * FROM info", conn)
    
  st.dataframe(data)
    
  conn.close()

  st.toast("Save complete")



