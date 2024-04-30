import streamlit as st
import pandas as pd

# sets the page configurations, visually the same as the homepage but with a different page title.
st.set_page_config(
    page_title="Name Search",
    page_icon="🏛️",
    layout="centered",
    menu_items={
        'Report a bug': 'mailto:caseyjos@hawaii.edu?subject=Reporting a Bug for: CourtOpinionSearch'
    }
)

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