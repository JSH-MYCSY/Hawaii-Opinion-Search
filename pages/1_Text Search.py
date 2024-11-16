import streamlit as st
import pandas as pd
#from openai import OpenAI
import os, csv

# sets the page configurations, visually the same as the home page, but with a different page title.
st.set_page_config(
    page_title="Text Search",
    page_icon="🏛️",
    layout="centered",
    menu_items={
        'Report a bug': "mailto:caseyjos@hawaii.edu?subject=Reporting a Bug for: CourtOpinionSearch&body=I have found a bug on your website's name search page. The bug is: . Please fix this bug as your website is awesome and I really want to continue using it."  # This menu option will allow someone to report a bug to me using their email client.
    }
)

# This function is used later to provide users with a more focused and refined search results using ChatGPT.
# def ChatGPTSubjectSearch(userInput, opinionExcerpt):
#     client = OpenAI(api_key = st.secrets['OPENAI_API_KEY'])
#     completion = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are being passed a keyword and an excerpt from a court opinion. Determine if the keyword is the subject of the sentence it is used in. If the keyword is the subject, return only True. Otherwise, return only False."},
#             {"role": "user", "content": "keyword:" + "\n" + userInput + "\n" + "excerpt:" + "\n" + opinionExcerpt}
#         ]
#     )
#     return(completion.choices[0].message.content)

# This functions sets up a toggle that is saved to a global boolean in order to function as an on/off switch for the ChatGPT search function.
# def setupAIon():
#     global AIon
#     #AIon = st.toggle("OpenAI Refined Search")
#     AIon = False

# Copy of function from Home Page because streamlit does not like it when you import from other pages.
# @st.cache
# def loadData():
#     if('OpinionText' not in st.session_state or 'NameList' not in st.session_state):
#         loadList = os.listdir("courtOpinionText/")
#         OpinionText = []
#         NameList = []
#         for item in loadList:
#             with open("courtOpinionText/" + item, "r", encoding="utf-8") as txtObj:
#                 OpinionText.append([str(item).split(".")[0], txtObj.read().lower()])
#         with open("CourtOpinion_Hawaii_New.csv", "r", encoding="utf-8") as csvObj:
#             reader = csv.reader(csvObj)
#             for row in reader:
#                 NameList.append(row)
#         st.session_state['OpinionText'] = OpinionText
#         st.session_state['NameList'] = NameList

# This is the search function for the program.
@st.cache_data(ttl="1d", max_entries=10)  # This function is meant to cache the last 10 search results for 1 day so that they can be pulled up faster.
def textSearch(userInput, AISearch=False):  # This has two inputs in order to tell the cache to treat a ChatGPT search differently from a normal search.
    returnList = []
    searchedList = []
    loadList = os.listdir("courtOpinionText/")
    for searchItem in loadList:
        with open("courtOpinionText/" + searchItem, "r", encoding="utf-8") as txtObj:
            txtRead = txtObj.read().lower()
            if(userInput.lower() in txtRead):  # txtRead was already made lower when initially loaded.
                    # inputLength = len(userInput)
                    # if(AISearch == True):  # This is the toggle for the AI search feature.
                    #     startingLine = 0
                    #     endchecker = inputLength
                    #     while(endchecker < len(txtRead)):
                    #         if(userInput.lower() == txtRead[startingLine:endchecker].lower()):
                    #             if(ChatGPTSubjectSearch(userInput, txtRead[startingLine-50:endchecker+50]) == "True"):  # provides ChatGPT with a snippet of the text 100 characters long to determine if the inputted word or phrase is the subject of the sentence it is used in.
                    #                 name = searchItem[0]
                    #                 returnList.append(name)
                    #                 break
                    #             startingLine+=50
                    #             endchecker+=50
                    #         else:
                    #             startingLine+=1
                    #             endchecker+=1
                    #else:
                name = str(searchItem).split(".")[0]
                returnList.append(name)
    with open("CourtOpinion_Hawaii_New.csv","r",encoding="utf-8") as csvObj:
        reader = csv.reader(csvObj)
        for row in reader:
            for name in returnList:
                if(name in row[1]):
                    searchedList.append(row)
    return(searchedList)

# This is the main function for this page.
def main():
    st.title("Test Opinion Text Search")
    #setupAIon()
    #loadData()
    user_text2 = st.text_input("What text do you want to search for?")
    if st.button("Text Search"):
        print(user_text2)
        try:  # the try/except pattern is to catch the error when the searchList returns nothing.
            new_list = textSearch(user_text2)
            df1 = pd.DataFrame({  # using this data frame to pull out some of the case information to display in a table.
                "Case Name": [sublist[0] for sublist in new_list],
                "Case Date": [sublist[2][0:10] for sublist in new_list],
                "Case Url": [sublist[1] for sublist in new_list]
            })
            st.data_editor(df1, column_config={"Case Url": st.column_config.LinkColumn(label="Case Url", display_text="Case Link")}, hide_index=True)  # used streamlit's table because I liked the way it displayed the results, and also allows a user to download the table for themselves. The column config is just to display the case text information as a hyperlink.
        except:
            st.write("I'm sorry, we could not find any opinions with the provided search term.")

# loads the main function.
if(__name__ == "__main__"):
    main()

# The code below this was the initial search function that individually opened up each txt file to search through it.

# import os, csv
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