import os, csv
import streamlit as st
import streamlit.components.v1 as components

# These are the page configs to setup some visual elements.
st.set_page_config(
    page_title="Court Opinion Search",
    page_icon="🏛️",
    layout="centered",
    menu_items={
        'Report a bug': "mailto:caseyjos@hawaii.edu?subject=Reporting a Bug for: CourtOpinionSearch&body=I have found a bug on your website's name search page. The bug is: . Please fix this bug as your website is awesome and I really want to continue using it."  # This menu option will allow someone to report a bug to me using their email client.
    }
)

# This function loads the search database from the csv and txt files, then saves them as a session state for faster access when searching.
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

# This specifies the body of the application for the homepage.
def appBody():
    st.sidebar.success("Choose a Search Option.")
    st.title("Post-2010 Hawaii Appellate Court Opinion Search")
    st.markdown('''
    This is a coding project by Joshua Casey for a grade in **Coding for Lawyers**.
    Please choose a search method from the sidebar to begin searching.

    The search directory should be updated every Tuesday and Friday around 00:00 HST.
                
    If you would prefer, please view the original source of all the opinions below.
    ''')
    components.iframe(src="https://www.courts.state.hi.us/opinions_and_orders/opinions", scrolling=True, height=500)  # The iframe is just to allow people to go directly to the site if they want.

# main function to load everything.
def main():
    loadData()
    appBody()

# calls the main function.
if(__name__ == "__main__"):
    main()
