import streamlit as st
import pandas as pd
from processing.customer import (
    load_data,
    create_rfm_dataset
)
import base64


def upload_ui():
    st.subheader('Load a Dataset 💾')
    input_file = st.file_uploader(label="Upload your dataset (.xlsx)")
    # Upload
    if st.button("Load Example") or st.session_state['local'] and not input_file:
        st.session_state['local'] = True
        st.session_state['upload'] = False
        dataset_type = 'LOCAL'
        with st.spinner('Loading data..'):
            df = load_data(dataset_type)
            st.write(df.head())
        list_var, df = dataset_ui(df)

        # Process filtering
        st.write("\n")
        st.subheader('''📊 Your dataset with the final version of the features''')
        df_sample = df[list_var].copy()

        st.write(df_sample.head(2))
        return dataset_type, df
    elif input_file or st.session_state['upload']:
        st.session_state['upload'] = True
        st.session_state['local'] = False
        dataset_type = 'UPLOADED'
        with st.spinner('Loading data..'):
            df = load_data(dataset_type, input_file)
            st.write(df.head())
        list_var, df = dataset_ui(df)

        # Process filtering
        st.write("\n")
        st.subheader('''📊 Your dataset with the final version of the features''')
        df_sample = df[list_var].copy()

        st.write(df_sample.head(2))
        return dataset_type, df
    else:
        st.stop()


def dataset_ui(df):
    # SHOW PARAMETERS
    # expander_default = (dataset_type=='UPLOADED')

    st.subheader('🛎️ Please choose from the following features in your dataset')
    with st.expander("FEATURES TO USE FOR THE ANALYSIS"):
        st.markdown('''
        _Select the columns that you want to include in the analysis of your sales records._
    ''')
        dict_var = {}
        for column in df.columns:
            dict_var[column] = st.checkbox("{} (IN/OUT)".format(column), value=1)
    filtered = filter(lambda col: dict_var[col] == 1, df.columns)
    list_var = list(filtered)

    return list_var, df


def export_ui(rfm):
    st.header('**Export results ✨**')
    st.write("_Finally you can export the results of your segmentation with all the parameters calculated._")
    if st.checkbox('Export Data', key='show'):
        with st.spinner("Exporting.."):
            st.write(rfm.head())
            rfm = rfm.to_csv(decimal=',')
            b64 = base64.b64encode(rfm.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a>'
            st.markdown(href, unsafe_allow_html=True)
