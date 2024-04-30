import streamlit as st
import csv, os
from openai import OpenAI

st.set_page_config(
    page_title="Home",
    page_icon=":Classical_Building:",
    layout="centered",
    menu_items={
        'Report a bug': 'mailto:caseyjos@hawaii.edu'
    }
)

def ChatGPTSubjectSearch(userInput, opinionExcerpt):
    client = OpenAI(api_key = st.secrets['OPENAI_API_KEY'])
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are being passed a keyword and an excerpt from a court opinion. Determine if the keyword is the subject of the sentence it is used in. If the keyword is the subject, return only True. Otherwise, return only False."},
            {"role": "user", "content": "keyword:" + "\n" + userInput + "\n" + "excerpt:" + "\n" + opinionExcerpt}
        ]
    )
    return(completion.choices[0].message.content)

def nameSearch(userInput):
    name_list = []
    with open("CourtOpinion_Hawaii_New.csv","r",encoding='utf-8') as csvObj:
        read = csv.reader(csvObj)
        for row in read:
            if userInput.lower() in str(row[0]).lower():
                name_list.append(row)
    return(name_list)

# def textSearch(userInput):
#     AIon = False
#     SearchList = os.listdir("courtOpinionText/")
#     returnList = []
#     searchedList = []
#     for searchItem in SearchList:
#         with open("courtOpinionText/" + searchItem, "r", encoding="utf") as txtObj:
#             txtRead = txtObj.read()
#             if(userInput.lower() in txtRead.lower()):
#                 inputLength = len(userInput)
#                 if(AIon == True):
#                     startingLine = 0
#                     endchecker = inputLength
#                     while(endchecker < len(txtRead)):
#                         if(userInput.lower() == txtRead[startingLine:endchecker].lower()):
#                             if(ChatGPTSubjectSearch(userInput, txtRead[startingLine-50:endchecker+50]) == "True"):
#                                 name = str(searchItem).split(".")[0]
#                                 returnList.append(name)
#                                 break
#                             startingLine+=1
#                             endchecker+=1
#                         else:
#                             startingLine+=1
#                             endchecker+=1
#                 else:
#                     name = str(searchItem).split(".")[0]
#                     returnList.append(name)
#     with open("CourtOpinion_Hawaii_New.csv", "r", encoding="utf-8") as csvObj:
#         reader = csv.reader(csvObj)
#         for row in reader:
#             for name in returnList:
#                 if(name in row[1]):
#                     searchedList.append(row)
#     return(searchedList)

def appBody():
    st.sidebar.success("Choose a Search Option.")
    st.title("Post-2010 Hawaii Appellate Court Opinion Search")
    st.markdown('''
    This is a coding project by Joshua Casey for a grade in **Coding for Lawyers**.
    Please choose a search method from the sidebar to begin searching.

    The search directory should be updated every Tuesday and Friday around 00:00 HST.
    ''')

def main():
    appBody()
    st.session_state.AIExistence = 1
if(__name__ == "__main__"):
    main()
