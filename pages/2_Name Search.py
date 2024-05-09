import streamlit as st
import pandas as pd
import os, csv

# sets the page configurations, visually the same as the homepage but with a different page title.
st.set_page_config(
    page_title="Name Search",
    page_icon="🏛️",
    layout="centered",
    menu_items={
        'Report a bug': "mailto:caseyjos@hawaii.edu?subject=Reporting a Bug for: CourtOpinionSearch&body=I have found a bug on your website's name search page. The bug is: . Please fix this bug as your website is awesome and I really want to continue using it."  # This menu option will allow someone to report a bug to me using their email client.
    }
)

# Copy of function from Home Page because streamlit does not like you importing from other pages.
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

# name search function
@st.cache_data(ttl="1d", max_entries=10) # caches the last ten search results for one day in order to provide faster results upon searching again.
def nameSearch(userInput):
    name_list = []
    for row in st.session_state['NameList']:
        if userInput.lower() in str(row[0]).lower():
            name_list.append(row)
    return(name_list)

# this is the main function for this page.
def main():
    st.title("Test Opinion Name Search")
    loadData()
    user_text = st.text_input("What name do you want to search for?")
    if st.button("Name Search"):
        print(user_text)
        try:  # the try/except pattern is to catch the error when the searchList returns nothing.
            new_list = nameSearch(user_text)
            df1 = pd.DataFrame({  # using this data frame to pull out some of the case information to display in a table.
                "Case Name": [sublist[0] for sublist in new_list],
                "Case Date": [sublist[2][0:10] for sublist in new_list],
                "Case Url": [sublist[1] for sublist in new_list]
            })
            st.data_editor(df1, column_config={"Case Url": st.column_config.LinkColumn(label="Case Url", display_text="Case Link")}, hide_index=True)  # used streamlit's table because I liked the way it displayed the results, and also allows a user to download the table for themselves. The column config is just to display the case text information as a hyperlink.
        except:
            st.write("I'm sorry, we could not find any opinions with the provided search term.")

# this loads the main function.
if(__name__ == "__main__"):
    main()