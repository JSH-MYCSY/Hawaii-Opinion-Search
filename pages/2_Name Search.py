import csv
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Name Search",
    page_icon=":Classical_Building:",
    layout="centered",
    menu_items={
        'Report a bug': 'mailto:caseyjos@hawaii.edu'
    }
)


@st.cache_data(ttl="1d", max_entries=10)
def nameSearch(userInput):
    name_list = []
    for row in st.session_state['NameList']:
        if userInput.lower() in str(row[0]).lower():
            name_list.append(row)
    return(name_list)

def main():
    st.title("Test Opinion Name Search")
    user_text = st.text_input("What name do you want to search for?")
    if st.button("Name Search"):
        print(user_text)
        try:
            new_list = nameSearch(user_text)
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