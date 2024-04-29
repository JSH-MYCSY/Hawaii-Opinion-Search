import os, csv
import streamlit as st
import pandas as pd
from CourtOpinion_Hawaii_Website_Search import ChatGPTSubjectSearch

def setupAIon():
    global AIon
    try:
        if(st.session_state.AIExistence == 1):
            AIon = st.toggle("OpenAI Refined Search")
        else:
            AIon = False
    except:
        if(os.getenv('OPENAI_API_KEY')):
            AIon = st.toggle("OpenAI Refined Search")
        else:
            AIon = False
    else:
        AIon = False

def textSearch(userInput):
    SearchList = os.listdir("courtOpinionText/")
    returnList = []
    searchedList = []
    for searchItem in SearchList:
        with open("courtOpinionText/" + searchItem, "r", encoding="utf") as txtObj:
            txtRead = txtObj.read()
            if(userInput.lower() in txtRead.lower()):
                inputLength = len(userInput)
                if(AIon == True):
                    startingLine = 0
                    endchecker = inputLength
                    while(endchecker < len(txtRead)):
                        if(userInput.lower() == txtRead[startingLine:endchecker].lower()):
                            if(ChatGPTSubjectSearch(userInput, txtRead[startingLine-50:endchecker+50]) == "True"):
                                name = str(searchItem).split(".")[0]
                                returnList.append(name)
                                break
                            startingLine+=1
                            endchecker+=1
                        else:
                            startingLine+=1
                            endchecker+=1
                else:
                    name = str(searchItem).split(".")[0]
                    returnList.append(name)
    with open("CourtOpinion_Hawaii_New.csv", "r", encoding="utf-8") as csvObj:
        reader = csv.reader(csvObj)
        for row in reader:
            for name in returnList:
                if(name in row[1]):
                    searchedList.append(row)
    return(searchedList)

def main():
    st.title("Test Opinion Text Search")
    setupAIon()
    user_text2 = st.text_input("What text do you want to search for?")
    if st.button("Text Search"):
        print(user_text2)
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
    main()