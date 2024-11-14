import streamlit as st
import pandas as pd
import os, csv

# sets the page configurations, visually the same as the home page, but with a different page title.
st.set_page_config(
    page_title="Advanced Text Search",
    page_icon="🏛️",
    layout="centered",
    menu_items={
        'Report a bug': "mailto:caseyjos@hawaii.edu?subject=Reporting a Bug for: CourtOpinionSearch&body=I have found a bug on your website's name search page. The bug is: . Please fix this bug as your website is awesome and I really want to continue using it."  # This menu option will allow someone to report a bug to me using their email client.
    }
)

# Copy of function from Home Page because streamlit does not like it when you import from other pages.
def loadData():
    if('OpinionText' not in st.session_state or 'NameList' not in st.session_state):
        loadList = os.listdir("courtOpinionText/")
        OpinionText = []
        NameList = []
        for item in loadList:
            with open("courtOpinionText/" + item, "r", encoding="utf-8") as txtObj:
                OpinionText.append([str(item).split(".")[0], txtObj.read().lower()])
        with open("CourtOpinion_Hawaii_New.csv", "r", encoding="utf-8") as csvObj:
            reader = csv.reader(csvObj)
            for row in reader:
                NameList.append(row)
        st.session_state['OpinionText'] = OpinionText
        st.session_state['NameList'] = NameList

# This is the search function for the program.
@st.cache_data(ttl="1d", max_entries=10)  # This function is meant to cache the last 10 search results for 1 day so that they can be pulled up faster.
def advancedTextSearch(mustUserArray,mayUserArray):  # This has two inputs in order to tell the cache to treat a ChatGPT search differently from a normal search.
    returnList = []
    searchedList = []
    for searchItem in st.session_state['OpinionText']:
        searchedList.append([searchItem[0],searchItem[1],0,0])
    t = 0
    
    for row1 in searchedList:
        for row in mustUserArray:
            if row.lower() in row1[1].lower():
                row1[2]+=1
    for row1 in searchedList:
        for row in mayUserArray:
            if row.lower() in row1[1].lower():
                row1[3]+=1
                t+=1
    
    
    for row in st.session_state['NameList']:
        for row1 in searchedList:
            if(t > 0):
                if(row1[2] == len(mustUserArray) and row1[0] in row[1] and row1[3] > 0):
                    returnList.append(row)
            else:
                if(row1[2] == len(mustUserArray) and row1[0] in row[1]):
                    returnList.append(row)
    return(returnList)

# This is the main function for this page.
def main():
    st.title("Test Opinion Text Search")
    loadData()
    st.text("separate each search term with a comma (ex. 'Honolulu, OVUII' for Honolulu and OVUII)")
    user_text2 = st.text_input("Text must include:")
    user_text3 = st.text_input("Text may include:")
    user_array_must = user_text2.split(",")
    user_array_may = user_text3.split(",")
    if st.button("Advanced Text Search"):
        print(user_text2)
        try:  # the try/except pattern is to catch the error when the searchList returns nothing.
            new_list = advancedTextSearch(user_array_must,user_array_may)
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
