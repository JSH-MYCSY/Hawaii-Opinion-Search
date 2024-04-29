import streamlit as st
import csv, os
from openai import OpenAI
client = OpenAI(api_key = st.secrets['OPENAI_API_KEY'])

st.set_page_config(
    page_title="Home",
)

def APIVerification():
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "This is a test. Return True."}
        ]
    )
    return(completion.choices[0].message.content)

def ChatGPTSubjectSearch(userInput, opinionExcerpt):
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
    st.text("This is a coding project by Joshua Casey for a grade in Coding for Lawyers.")
    st.text("Please choosea search method from the sidebar.")
    st.text("This search directory should be updated every Tuesday and Friday around 00:00 HST")

def api_key_form():
    with st.form("openai_key_form"):
        openai_api_key = st.text_input("Please enter your OpenAI API Key")
        submitted = st.form_submit_button("Submit")
        if submitted:
            if openai_api_key:
                os.environ['OPENAI_API_KEY'] == str(openai_api_key)
                try:
                    testBoolean = APIVerification()
                    if(testBoolean):
                        st.session_state.AIExistence = 1
                except:
                    st.error("Your API Key was invalid.")
                    st.session_state.AIExistence = 0
            else:
                st.error("You have not entered an OpenAI API Key, proceeding will not give you access to the gpt refined search.")
                st.session_state.AIExistence = 0
            

def main():
    if(os.getenv('OPENAI_API_KEY')):
        appBody()
        st.session_state.AIExistence = 1
    else:
        api_key_form()
if(__name__ == "__main__"):
    main()
