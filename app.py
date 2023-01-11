import streamlit as st

#Set page configurations once
st.set_page_config(page_title="Beazley Snowflake",
                     page_icon="https://www.pikpng.com/pngl/b/124-1245406_periscope-data-partners-snowflake-computing-logo-clipart.png",
                     layout="centered",
                     initial_sidebar_state="auto",
                     menu_items={
                        "Get Help":"mailto:dougal.toms@beazley.com",
                        "About":"Snowflake made easy"
                     })

from utils import snowflake_connector as sf

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

    st.info(f"Logged in as: {user} ({role})", icon="ℹ️")

    #------------------------------#
    # No code UI for executing SQL #
    #------------------------------#

    st.markdown("---")
    st.subheader("No code UI")
    st.markdown("Streamlit's UI makes it easy for a user to execute simple, no-code SQL statements e.g. adding comments to an object or altering tasks")

    left, right = st.columns(2)

    ##################
    # Altering Tasks #
    ##################
    with left:
        # Show tasks in account
        tasks = sf.query_to_df('''show tasks in account;''')
        tasks = tasks[['name', 'state']]
        st.dataframe(tasks)

        task_names = tasks['name'].to_list()

    ###################
    # Adding comments #
    ###################

    with right:
        # Get list of accessible DBs
        db = sf.query_to_df('''show databases in account;''')
        db = db['name'].to_list()

        # Allow user to choose which DB to work in
        col1, col2, col3 = st.columns(3)

        with col1:
            db_selection = st.multiselect('Select Database', db)
            
            if 'db_selection' not in st.session_state:
                st.session_state['db_selection'] = db_selection
            else:
                st.session_state['db_selection'] = db_selection
        
            if db_selection:

                # Get list of accessible Schemas
                schemas = sf.query_to_df(f'''show schemas in database {db_selection[0]};''')
                schemas = schemas['name'].to_list()

                # Allow user to choose which Schema to work in
                with col2:
                    schema_selection = st.multiselect('Select Schema', schemas)
            
                    if 'schema_selection' not in st.session_state:
                        st.session_state['schema_selection'] = schema_selection
                    else:
                        st.session_state['schema_selection'] = schema_selection

                    if schema_selection:

                        # Get list of accessible Tables/Views
                        tables = sf.query_to_df(f'''show tables in {db_selection[0]}.{schema_selection[0]}''')
                        tables = tables['name'].to_list()

                        # Allow user to choose which Table to work in
                        with col3:
                            table_selection = st.multiselect('Select Table / View', tables)

                            if 'table_selection' not in st.session_state:
                                st.session_state['table_selection'] = table_selection
                            else:
                                st.session_state['table_selection'] = table_selection                        
                
                            if table_selection:

                                # Display info about table
                                df = sf.query_to_df(f'''select * 
                                                    from {db_selection[0]}.{schema_selection[0]}.{table_selection[0]};''')

                                # Store in session_state
                                if 'df' not in st.session_state:
                                    st.session_state['df'] = df
                                else:
                                    st.session_state['df'] = df

                                
        # Number of rows to display
        if 'df' in st.session_state:

            with st.expander(f"View {st.session_state.table_selection[0]}"):
                                    
                limit = st.number_input('Select number of rows to display', min_value=1, value=5,max_value=1000, format='%i')

                if limit:
                    st.dataframe(st.session_state.df[1:limit+1], use_container_width=True)

            with st.expander(f"Add comments to {st.session_state.table_selection[0]}"):
                column_to_comment = st.selectbox("Select column", df.columns)
                if column_to_comment:
                    st.session_state['column_to_comment'] = column_to_comment

                comment = st.text_area("Comment text")
                if comment:
                    st.session_state['comment'] = comment
                
                button = st.button("Add comment")
                if button:
                    st.session_state['button'] = button

                if 'button' in st.session_state and st.session_state.button == True:
                
                    code = f'''COMMENT ON COLUMN {st.session_state.db_selection[0]}.{st.session_state.schema_selection[0]}.{st.session_state.table_selection[0]}.{st.session_state.column_to_comment} IS '{st.session_state.comment}'; '''
                    st.code(code, language='sql')

                    # Describe table before comment added
                    before_comments = sf.query_to_df(f'''describe table {st.session_state.db_selection[0]}.{st.session_state.schema_selection[0]}.{st.session_state.table_selection[0]}''')

                    if 'before_comments' not in st.session_state:
                        st.session_state['before_comments'] = before_comments
                    else:
                        st.session_state['before_comments'] = before_comments

                    # Add comment   
                    sf.run_query(code)

                    # Describe table after comment added
                    after_comments = sf.query_to_df(f'''describe table {st.session_state.db_selection[0]}.{st.session_state.schema_selection[0]}.{st.session_state.table_selection[0]}''')

                    if 'after_comments' not in st.session_state:
                        st.session_state['after_comments'] = after_comments
                    else:
                        st.session_state['after_comments'] = after_comments

                    # Turn button off    
                    st.session_state.button = False

                    # Display results of adding comment
                    before, after = st.columns(2)

                    with before:
                        st.write("Table description before")
                        st.dataframe(st.session_state.before_comments)

                    with after:
                        st.write("Table description after")
                        st.dataframe(st.session_state.after_comments)
            
        #---------------------------#
        # Geospatial analysis is easy
        #---------------------------#

        st.markdown("---")
        st.subheader('Geospatial data analysis')

        with st.expander("Geospatial analysis"):
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

    #--------------------------------#
    # Integrating PowerBI dashboards #
    #--------------------------------#

    st.markdown("---")
    st.subheader("Integrating PowerBI dashboards")
    st.write("Integrating dashboard can be done with one line of code using markdown")
    code = '''st.markdown("https:\\app.powerbi.com\\groups\\me\\reports\\cb2e2a2f-fe9a-4b29-b817-6d7119cd1487\\ReportSection?referrer=embed.appsource", unsafe_allow_html=True)'''
    st.code(code, language='python')
    st.write('''<iframe title= "Claims Dev Chart" width="700" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=cb2e2a2f-fe9a-4b29-b817-6d7119cd1487&autoAuth=true&ctid=9a50eba8-7568-447a-bcb9-27a0d464aa80" frameborder="0" allowFullScreen="true"></iframe>''',unsafe_allow_html=True)

    #------------------#
    #- Altering tasks -#
    #------------------#

    st.markdown("---")
    st.subheader("Altering Tasks")
    st.write("E")

if __name__ == "__main__":
    homepage()