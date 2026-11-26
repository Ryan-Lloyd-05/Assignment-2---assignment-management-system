import streamlit as st
#to run the code you have to enter the file loction into command prompt by dragging in and typing streamlit run before it
#(example) C:\Users\Ryanw>streamlit run "C:\Users\Ryanw\Stuff\Uni stuff\Assignmnet 2 code.py"
def create_account():
  
  user = st.text_input("create a username:")
  password = st.text_input("create a password:", type="password")
  if st.button("Create account"):
    with open("accounts.txt", "a") as file:
      file.write(f"{user},{password}\n")
    st.session_state["account"] = True
    st.write("account created")

 
def login_account():
  
  user_check = st.text_input("enter username:")
  password_check = st.text_input("enter password:", type="password")
  if st.button("Login"):
    with open("accounts.txt") as file:
      for line in file:
        user, password = line.strip().split(",")

        if user == user_check and password == password_check:
          st.write("login successful")
          st.session_state["log_in"] = True
          return
    st.write("login failed")
  
def upload_file():
  uploaded_file = st.file_uploader("select the file you want to upload")
  
  
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
    task = st.selectbox("select file", file_list, key="deadline_task")
    deadline = st.text_input("enter a deadline:", key="deadline")
    if st.button("Add deadline"):
      st.session_state["deadlines"].append(f"{task}: {deadline}")
      
      st.write(st.session_state["deadlines"])
  
    
    


# main code

st.header ("Assignment management system")

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
  elif choice_a == "create deadlines" and "file" == False:
    st.write("please upload a file first")
  elif choice_a == "create deadlines":
    create_deadlines()
