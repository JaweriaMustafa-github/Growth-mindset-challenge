#Import 
import streamlit as st 
import pandas as pd
import os
from io import BytesIO 

#setup our app
st.set_page_config(page_title="🚀Data Sweeper🧹💾", layout="wide")
st.title("🚀Data Sweeper🧹💾")
st.write("Effortlessly convert CSV & Excel files with my built-in data cleaning and stunning visualizations!⬇️📊✨")

# Theme Selector
theme = st.sidebar.selectbox("Select Theme", ["Light Mode", "Dark Mode", "Golden-Yellow-->Cyan Gradient"])

# Apply custom CSS based on selected theme
if theme == "Dark Mode":
    st.markdown(
        """
        <style>
            .stApp {
                background-color: black;
                color: white;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
elif theme == "Golden-Yellow-->Cyan Gradient":
    st.markdown(
        """
        <style>
            .stApp {
                background: linear-gradient(90deg,rgb(226, 212, 11), #00bcd4);
                color: black;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    # Custom CSS for neon glow effect
st.markdown("""
    <style>
        div.stFileUploader > label {
            background: linear-gradient(90deg, rgb(226, 212, 11), #00bcd4);
            color:black;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 8px;
            
            transition: 0.3s ease-in-out;
            text-align: center;
            display: inline-block;
            cursor: pointer;
            border: none;
        }
        div.stFileUploader > label:hover {
            box-shadow: 0px 0px 15px #00bcd4, 0px 0px 25px rgb(226, 212, 11);
            transform: scale(1.05);
        }
    </style>
""", unsafe_allow_html=True)


uploaded_files = st.file_uploader("Upload your files (CSV or Excel):" , type=["csv","xlsx"],accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
                df = pd.read_excel(file)
        else:
            st.error (f"Unsupported file type:{file_ext}")
            continue

        # Display info about the file
        st.write(f"**File Name: **{file.name}")
        st.write(f"**File Size: **{file.size/1024}")

        # Show 5 rows of our data frame (df)
        st.write("Preview the Head of the DataFrame")
        st.dataframe(df.head())

        # Options for data cleaning:
        st.subheader("Data cleaning otions:")
        if st.checkbox(f"Clean data for:{file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed!")
            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols =  df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values have been filled!")

        #Choose specific columns to keep or convert
        st.subheader("Select columns to convert:")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns , default=df.columns)
        df = df[columns]

        #Create some Visualizations
        st.subheader("💾 Data Visualization")
        if st.checkbox(f"Show visualization for {file.name}"):
                    # Chart Customization
           st.subheader(f"Customize Chart for {file.name}")
        chart_type = st.selectbox(f"Select Chart Type for {file.name}", ["Bar Chart", "Line Chart", "Area Chart"])
        selected_columns = st.multiselect(f"Select numeric columns for visualization in {file.name}", df.select_dtypes(include="number").columns, default=df.select_dtypes(include="number").columns[:2])

        if selected_columns:
            if chart_type == "Bar Chart":
                st.bar_chart(df[selected_columns])
            elif chart_type == "Line Chart":
                st.line_chart(df[selected_columns])
            elif chart_type == "Area Chart":
                st.area_chart(df[selected_columns])
        else:
            st.warning("Please select at least one numeric column for visualization.")
            st.bar_chart(df.select_dtypes(include="number").iloc[:,:2])

        #Convert the file --> CSV into EXCEL & Vice Versa
        st.subheader("Conversion Options:")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV","Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()

            if conversion_type == "CSV":
              df.to_csv(buffer, index=False)
              file_name = file.name.replace(file_ext , ".csv")
              mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext , ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            # Download button
            st.download_button(
                label=f"⬇️ Download {file.name} as {conversion_type}",
                data=buffer, 
                file_name = file_name,
                mime=mime_type
            )

st.success("🎉 Hurray! All files are processed!!!")