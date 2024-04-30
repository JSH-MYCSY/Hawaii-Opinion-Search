import os, csv
import streamlit as st
import pandas as pd
from openai import OpenAI

st.set_page_config(
    page_title="Text Search",
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


def setupAIon():
    global AIon
    AIon = st.toggle("OpenAI Refined Search")

# def loadData():
#     loadList = os.listdir("CourtOpinionText/")
#     global cachedOpinionText
#     cachedOpinionText = []
#     global cachedNameList
#     cachedNameList = []
#     for item in loadList:
#         with open("courtOpinionText/" + item, "r", encoding="utf-8") as txtObj:
#             cachedOpinionText.append([str(item).split(".")[0], txtObj.read().lower()])
#     with open("CourtOpinion_Hawaii_New.csv", "r", encoding="utf-8") as csvObj:
#         reader = csv.reader(csvObj)
#         for row in reader:
#             cachedNameList.append(row)

@st.cache_data(ttl="1d", max_entries=10)
def textSearch(userInput):
    returnList = []
    searchedList = []
    for searchItem in st.session_state['OpinionText']:
        txtRead = searchItem[1]
        if(userInput.lower() in txtRead):
                inputLength = len(userInput)
                if(AIon == True):
                    startingLine = 0
                    endchecker = inputLength
                    while(endchecker < len(txtRead)):
                        if(userInput.lower() == txtRead[startingLine:endchecker].lower()):
                            if(ChatGPTSubjectSearch(userInput, txtRead[startingLine-50:endchecker+50]) == "True"):
                                name = searchItem[0]
                                returnList.append(name)
                                break
                            startingLine+=50
                            endchecker+=50
                        else:
                            startingLine+=1
                            endchecker+=1
                else:
                    name = searchItem[0]
                    returnList.append(name)
    for row in st.session_state['NameList']:
        for name in returnList:
            if(name in row[1]):
                searchedList.append(row)
    return(searchedList)

# def textSearch(userInput):
#     SearchList = os.listdir("courtOpinionText/")
#     returnList = []
#     searchedList = []
#     for searchItem in SearchList:
#         with open("courtOpinionText/" + searchItem, "r", encoding="utf-8") as txtObj:
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

def Page1main():
    st.title("Test Opinion Text Search")
    setupAIon()
    #loadData()
    user_text2 = st.text_input("What text do you want to search for?")
    if st.button("Text Search"):
        print(user_text2)
        print(len(st.session_state['OpinionText']))
        print(len(st.session_state['NameList']))
        try:
            new_list = textSearch(user_text2)
            df1 = pd.DataFrame({
                "Case Name": [sublist[0] for sublist in new_list],
                "Case Date": [sublist[2][0:10] for sublist in new_list],
                "Case Url": [sublist[1] for sublist in new_list]
            })
            st.data_editor(df1, column_config={"Case Url": st.column_config.LinkColumn(label="Case Url", display_text="Case Link")}, hide_index=True)
        except:
            st.write("I'm sorry, we could not find any opinions with the provided search term.")

if(__name__ == "__main__"):
    Page1main()