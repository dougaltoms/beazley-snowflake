def header(text,background_color='#c8c3cd', color='#dc199b', font_size='18px'):
    import streamlit as st
    header = st.markdown(f'''<p style="background-color:{background_color};
                                    color:{color};
                                    font-size:{font_size};
                                    border-radius:0%;"
                                    >{text}</p>''', unsafe_allow_html=True)
    
    return header