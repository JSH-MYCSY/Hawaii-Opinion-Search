import streamlit as st
import csv, os

st.set_page_config(
    page_title="Home",
)

def nameSearch(userInput):
    name_list = []
    with open("CourtOpinion_Hawaii_New.csv","r",encoding='utf-8') as csvObj:
        read = csv.reader(csvObj)
        for row in read:
            if userInput.lower() in str(row[0]).lower():
                name_list.append(row)
    return(name_list)
    
def textSearch(userInput):
    SearchList = os.listdir("courtOpinionText/")
    returnList = []
    searchedList = []
    for searchItem in SearchList:
        with open("courtOpinionText/" + searchItem, "r", encoding="utf") as txtObj:
            if(userInput.lower() in txtObj.read().lower()):
                name = str(searchItem).split(".")[0]
                returnList.append(name)
    with open("CourtOpinion_Hawaii_New.csv", "r", encoding="utf-8") as csvObj:
        reader = csv.reader(csvObj)
        for row in reader:
            for name in returnList:
                if(name in row[1]):
                    searchedList.append(row)
    return(searchedList)


st.sidebar.success("Choose a Search Option.")

st.title("Post-2010 Hawaii Appellate Court Opinion Search")
st.text("This is a coding project by Joshua Casey for a grade in Coding for Lawyers.")

st.text("Please choosea search method from the sidebar.")

st.text("This search directory should be updated every Tuesday and Thursday at 10:00 a.m. UTC.")

# st.title("Test Opinion Name Search")
# user_text = st.text_input("What name do you want to search for?")
# if st.button("Name Search"):
#     print(user_text)
#     new_list = nameSearch(user_text)
#     for value, item in enumerate(new_list):
#         st.write(str(item[0]))
#         st.link_button("Name Link " + str(value), item[1])

# st.title("Test Opinion Text Search")
# user_text2 = st.text_input("What text do you want to search for?")
# if st.button("Text Search"):
#     print(user_text2)
#     new_list = textSearch(user_text2)
#     for number, item in enumerate(new_list):
#         st.write(str(item[0]))
#         st.link_button("Text Link " + str(number), item[1])