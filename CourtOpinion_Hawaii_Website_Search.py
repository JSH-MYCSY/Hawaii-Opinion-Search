import streamlit as st
import requests, bs4, io, csv, requests, os, time, random
from pypdf import PdfReader
import pandas as pd

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

def Update():
    variableTest = []
    with open("CourtOpinion_Hawaii_New.csv","r",encoding='utf-8') as csvObj:
        reader = csv.reader(csvObj)
        for row in reader:
            variableTest = row[0]
    with open("CourtOpinion_Hawaii_New.csv","a",newline='', encoding='utf-8') as csvObj:
        res = requests.get('https://www.courts.state.hi.us/opinions_and_orders/opinions/')
        courtOpinions = bs4.BeautifulSoup(res.text, 'html.parser')
        courtList = courtOpinions.find('tbody', {'class': 'row-hover'})
        caseName = courtList.find('td', {'class': 'column-4'})
        opinionUrl = courtList.find('td',{'class': 'column-3'})
        opinionDate = courtList.find('td', {'class': 'column-1'})
        courtType = courtList.find('td', {'class': 'column-2'})
        courtAppealed = courtList.find('td', {'class': 'column-5'})
        write = csv.writer(csvObj)
        while_loop_boolean = 0
        tempList = []
        while(while_loop_boolean == 0):
            if(variableTest not in caseName.text):
                case_name = caseName.text
                if('ADA' in str(opinionUrl)):
                    opinionUrlText = opinionUrl.find('a', {'title': 'ADA'})['href']
                else:
                    opinionUrlText = ""
                tempList.append([case_name,opinionUrlText, opinionDate.text, courtType.text, courtAppealed.text])
                caseName = caseName.find_next('td', {'class': 'column-4'})
                opinionUrl = opinionUrl.find_next('td', {'class': 'column-3'})
                opinionDate = opinionDate.find_next('td', {'class': 'column-1'})
                courtType = courtType.find_next('td', {'class': 'column-2'})
                courtAppealed = courtAppealed.find_next('td', {'class': 'column-5'})
            else:
                while_loop_boolean = 1
        tempList.reverse()
        for row in tempList:
            write.writerow(row)
        for row in tempList:
            if(".pdf" in row[1]):
                try:
                    res2 = requests.get(row[1])
                    io1 = io.BytesIO(res2.content)
                    myReader = PdfReader(io1)
                    titleTemp = str(row[1]).split("/")[-1]
                    title = titleTemp.split(".")[0]
                    with open("courtOpinionText/" + title + ".txt", "w", encoding="utf-8") as f:
                        for page in myReader.pages:
                            f.write(page.extract_text())
                except:
                    print("failed")
                time.sleep(random.randint(2,3))
    
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

if st.button("Update"):
    Update()