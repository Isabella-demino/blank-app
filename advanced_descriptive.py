import streamlit as st
import pandas as pd


st.set_page_config(page_title="advanced_descriptive.py", layout="centered")

st.title("📊 Descriptive Statistics Calculator")

st.markdown("""
Upload your data (CSV or Excel) and get basic descriptive statistics.
""")

uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

st.button('Click me', on_click=click_button)

if st.session_state.clicked:
    # The message and nested widget will remain on the page
    st.write('Button clicked!')
    st.slider('Select a value')

if uploaded_file is not None:
    try:
        # Determine file type and read accordingly
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file type. Please upload a CSV or XLSX file.")
            st.stop() # Stop execution if file type is unsupported

        st.success("File uploaded successfully!")
        st.write("### Data Preview:")
        st.dataframe(df.head())

        # Select columns for analysis
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if not numeric_cols:
            st.warning("No numeric columns found for descriptive statistics. Please check your data.")
        else:
            selected_test = st.select(
                "Select the test you would like to run",

            )
            selected_columns = st.multiselect(
                "Select columns for descriptive statistics:",
                numeric_cols,
                default=[] # Select all numeric by default
            )

            if selected_columns:
                st.write("### Data Types:")
                data_desc = df[selected_columns].dtypes
                st.write("please confirm that the data types listed for your variables match the type of analysis you would like to conduct")
                st.dataframe(data_desc)

                st.write("### Descriptive Statistics:")
                # Compute descriptive statistics
                desc_stats = df[selected_columns].describe()
                st.dataframe(desc_stats)
            else:
                st.info("Please select at least one numeric column to compute statistics.")

    except Exception as e:
        st.error(f"An error occurred: {e}. Please check your file format and data.")

st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and Pandas.")