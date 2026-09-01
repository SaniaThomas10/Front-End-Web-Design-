import streamlit as st

#name widget 
#name = st.text_input("What is your name?")
#st.write(f"Hello, {name}!")


#number input for age
#age = st.number_input("How old are you?", min_value=0, max_value=99, value=10)

#st.slider
#StressLevel = st.slider("Rate your stress level", min_value=0, max_value=10, value=5)


#st.selectbox
#subject = st.selectbox("What is your favorite subject?", ["Math", "Science", "History" ])

#st.radio 
#season = st.radio("what seasons do you like?", ["Winter", "Spring", "Summer", "Fall"])

#st.radio and st.selectbox together 
#st.write(f"Subject: {subject}, Season: {season}")


# st.checkbox
#Thrift = st.checkbox("Do you like to thrift stuff?")


#with st.form("About Me Form"):
 #   name = st.text_input("What is your name?")
  #  StressLevel = st.slider("Rate your stress level", min_value=0, max_value=10, value=5)
   # subject = st.selectbox("What is your favorite subject?", ["Math", "Science", "History" ])
    #season = st.radio("what seasons do you like?", ["Winter", "Spring", "Summer", "Fall"])
    #Thrift = st.checkbox("Do you like to thrift stuff?")
    #submitted = st.form_submit_button("Submit")

    #if submitted: write (f"Hello, {name}!")

st.title("Report a Parking Problem")

name = st.text_input("Your name")
st.write(f"Hello, {name}!")


minutes = st.number_input(
    "Minutes searching", min_value=0, max_value=60, value=10
)

frustration = st.slider(
    "Frustration (1-10)", 1, 10, value=5
)


lot = st.selectbox(
    "Which lot?", ["Lot A", "Lot B", "Lot C", "Lot D"]
)

time = st.radio(
    "What time?", ["Morning", "Midday", "Evening"]
)

would_use = st.checkbox(
    "I would use a real-time parking app")


st.divider()
who = name if name else "An anonymous student"
st.write(
    f"**{who}** spent **{minutes} min** in **{lot}** "
    f"during the **{time}**, frustration **{frustration}/10**."
)


with st.form("parking_form"):
    name = st.text_input("Your name")
    minutes = st.number_input("Minutes", 0, 60, 10)
    frustration = st.slider("Frustration", 1, 10, 5)
    submitted = st.form_submit_button("Submit report")

if submitted:
    st.write(f"Thanks, {name}!")

