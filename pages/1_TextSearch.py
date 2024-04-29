import streamlit as st
from CourtOpinion_Hawaii_Website_Search import textSearch
import pandas as pd
from CourtOpinion_Hawaii_Website_Search import AIExistence


def main():
    st.title("Test Opinion Text Search")
    if(AIExistence == 1):
        AIon = st.toggle("OpenAI Refined Search")
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