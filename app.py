import streamlit as st

# Set page configurations once
st.set_page_config(page_title="Beazley Snowflake",
                     page_icon="",
                     layout="centered",
                     initial_sidebar_state="collapsed",
                     menu_items={
                        "Get Help":"mailto:dougal.toms@beazley.com",
                        "About":"Snowflake made easy"
                     })

def homepage():

    with open("style/style.css") as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)

    st.header("Welcome to Beazley Snowflake")


if __name__ == "__main__":
    homepage()