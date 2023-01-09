import streamlit as st

#Set page configurations once
st.set_page_config(page_title="Beazley Snowflake",
                     page_icon="https://www.pikpng.com/pngl/b/124-1245406_periscope-data-partners-snowflake-computing-logo-clipart.png",
                     layout="centered",
                     initial_sidebar_state="collapsed",
                     menu_items={
                        "Get Help":"mailto:dougal.toms@beazley.com",
                        "About":"Snowflake made easy"
                     })

from utils import snowflake_connector as sf
from style import custom_header

def homepage():

    # Ensure session state is preserved
    for key in st.session_state:
        st.session_state[key] = st.session_state[key]

    # Custom css for page
    with open("style/style.css") as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)

    st.header("Welcome to Beazley Snowflake")

    account_params = sf.query_to_df('''select current_user(), current_role();''')
    user = account_params['CURRENT_USER()'][0]
    role = account_params['CURRENT_ROLE()'][0]

    st.success(f"Logged in as: {user} ({role})", icon="ℹ️")

    st.subheader('• Easily add comments to tables')

    # Get list of accessible DBs
    db = sf.query_to_df('''show databases in account;''')
    db = db['name'].to_list()

    # Allow user to choose which DB to work in
    col1, col2, col3 = st.columns(3)

    with col1:
        db_selection = st.multiselect('Select Database', db)
    
        if db_selection:

            # Get list of accessible Schemas
            schemas = sf.query_to_df(f'''show schemas in database {db_selection[0]};''')
            schemas = schemas['name'].to_list()

            # Allow user to choose which Schema to work in
            with col2:
                schema_selection = st.multiselect('Select Schema', schemas)

                if schema_selection:

                    # Get list of accessible Tables/Views
                    tables = sf.query_to_df(f'''show tables in {db_selection[0]}.{schema_selection[0]}''')
                    tables = tables['name'].to_list()

                    # Allow user to choose which Table to work in
                    with col3:
                        table_selection = st.multiselect('Select Table / View', tables)

                        if table_selection:

                            # Display info about table
                            df = sf.query_to_df(f'''select * 
                                                from {db_selection[0]}.{schema_selection[0]}.{table_selection[0]};''')

                            if 'df' not in st.session_state:
                                st.session_state['df'] = df
                            
    # Number of rows to display
    if 'df' in st.session_state:
                                
        limit = st.number_input('Select number of rows to display', min_value=1, value=5,max_value=1000, format='%i')

        if limit:
            st.table(st.session_state.df[1:limit+1])

    #     with st.form('comment_form'):

    #         column = st.selectbox('Column to comment on', st.session_state.df.columns)
    #         st.text_area('Add comment to table')

    #         submitted = st.form_submit_button('Add comment')

    #         if submitted:
    #             st.write('Snowflake working...')

    # else:
    #     pass

        st.subheader('• Geospatial data analysis')

        if 'LATITUDE' and 'LONGITUDE' in st.session_state.df.columns:
            
            df = st.session_state.df[['LATITUDE', 'LONGITUDE', 'REGION']]
            df['lat'] = df['LATITUDE']
            df['lon'] = df['LONGITUDE']

            checkbox = st.checkbox('Filter by Region')

            if checkbox:

                region = st.selectbox('Filter by Region', df['REGION'])
                df = df.loc[df['REGION'] == region]

                st.map(df)

            else:

                st.map(df)

if __name__ == "__main__":
    homepage()