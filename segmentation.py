import streamlit as st
from streamlit import caching

from ui.customer import upload_ui
from ui.customer import export_ui

from processing.customer import (
    create_rfm_dataset,
    rfm_processing,
    find_k,
    kmeans_clustering
)

from plot.customer import (
    rfm_plot,
    k_plot,
    cluster_plot,
    cluster_graph_plot,
)

# Set page configuration
st.set_page_config(page_title="Statistical Customer Segmentation",
                   initial_sidebar_state="expanded",
                   layout='wide',
                   page_icon="🛒")


# Set up the page
@st.cache(persist=False,
          allow_output_mutation=True,
          suppress_st_warning=True,
          show_spinner=True)
# Preparation of data
def prep_data(data_frame):
    col = data_frame.columns
    return col


# -- Page
caching.memo.clear()
caching.singleton.clear()
caching.suppress_cached_st_function_warning()

if 'local' not in st.session_state:
    st.session_state['local'] = False

if 'upload' not in st.session_state:
    st.session_state['upload'] = False

if 'start' not in st.session_state:
    st.session_state['start'] = False

c1, c2, c3 = st.columns(3)
# Information about the Dataset
c2.title("**Customer Segmentation**")

# Upload Data Set
dataset_type, df = upload_ui()

# Start Calculation ?
if st.button('Start Calculation?'):
    st.session_state['start'] = True

# Start Calculation after parameters fixing
if st.session_state['start']:
    with st.expander("RFM Dataset"):
        rfm = create_rfm_dataset(df)
        st.write(rfm.head())
        st.subheader("Distribution of the Features")
        rfm_plot(rfm)

        rfm = rfm_processing(rfm)
        st.subheader("Distribution of the Features after Logarithm Transformation")
        rfm_plot(rfm)

    with st.expander("K values"):
        k_values = find_k(rfm)
        k_plot(k_values)

    st.header("**KMeans Clustering**")

    col1, col2 = st.columns(2)
    rfm = kmeans_clustering(rfm)
    with col1:
        st.subheader("**3D Cluster graph**")
        cluster_plot(rfm)

    with col2:
        st.subheader("**Cluster graph as customer groups**")
        cluster_graph_plot(rfm)

    # Part 5: Export Results
    export_ui(rfm)
