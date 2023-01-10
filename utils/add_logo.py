def add_logo():

    import streamlit as st

    return st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://www.beazley.com/themes/custom/beazley_default/logo.svg);
                background-repeat: no-repeat;
                padding-top: 5px;
                background-position: 125px 30px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )