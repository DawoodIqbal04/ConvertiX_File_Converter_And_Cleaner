# Imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Streamlit Page Configuration
st.set_page_config(page_icon="💱", page_title="ConvertiX", layout="centered")


# Streamlit Page UI
st.title('💿 ConvertiX')

col1, col2 = st.columns([1, 6], vertical_alignment='center')

with col1:
    st.image('icons/convert.png', width=100)
with col2:
    st.markdown('### Effortlessly Convert and Clean Your Files Between CSV and Excel with Our Built-In Data Visualizer')
    
uploaded_files = st.file_uploader('Upload CSV or Excel File', type=['csv', 'xlsx'], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_extension = os.path.splitext(file.name)[-1].lower()

        if file_extension == '.csv':
            df = pd.read_csv(file)
        elif file_extension == '.xlsx':
            df = pd.read_excel(file)
        else:
            st.error(f'Invalid File Format: {file_extension}. Please Upload a CSV or Excel File.')
            continue

        st.write(f'**File Name:** {file.name}')
        st.write(f'**File Size:** {file.size/1024}')

        st.write('**Data Preview:**')
        st.dataframe(df.head())

        st.subheader('Data Cleaning and Visulization Options')
        if st.checkbox(f'Clean Data for {file.name}'):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f'Remove Duplicates from {file.name}'):
                    df.drop_duplicates(inplace=True)
                    st.write('Duplicates Removed Successfully!')
            with col2:
                if st.button(f'Fill Missing Values in {file.name}'):
                    numeric_cols = df.select_dtypes(include='number').columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write('Missing Values Filled Successfully!')

        st.subheader('Select Columns to Convert')
        columns = st.multiselect(f'Select Columns Form {file.name}', df.columns, default=df.columns)
        df = df[columns]

        st.subheader('📈 Data Visualization')
        if st.checkbox(f'Visualize Data from {file.name}'):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])


        st.subheader('💱 Conversion Options')
        conversion_type = st.radio(f'Convert {file.name} to:', ['CSV', 'Excel'], key=file.name)

        if st.button(f'Convert {file.name}'):
            buffer = BytesIO()
            if conversion_type == 'CSV':
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_extension, '.csv')
                mime_type = 'text/csv'

            elif conversion_type == 'Excel':
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_extension, '.xlsx')
                mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            buffer.seek(0)


            st.download_button(
                label=f'🔽 Download {file.name} as {conversion_type}',
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )


st.success('🎉 All Files Processed. \n Thank You for Using ConvertiX!')
