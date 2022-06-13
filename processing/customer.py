import pandas as pd
import datetime as dt
import streamlit as st
import numpy as np
from sklearn.cluster import KMeans


# Load data from user upload
@st.cache(allow_output_mutation=True)
def load_data(dataset_type, input_file=None):
    if dataset_type == "LOCAL":
        # Create Data Frame from local dataset
        df = pd.read_excel('data/Online_Retail_II_sample.xlsx')
    else:
        # Create Data Frame from uploaded dataset
        df = pd.read_excel(input_file)

    if 'Customer ID' not in df.columns:
        st.error("Main attributes of dataset are not present: Customer ID and Quantity")

    if 'Quantity' not in df.columns:
        st.error("Main attributes of dataset are not present: Customer ID and Quantity")

    df = df[pd.notnull(df['Customer ID'])]
    if (df['Quantity'] < 0).values.any():
        df = df[(df['Quantity'] > 0)]

    if (df['Price'] < 0).values.any():
        df = df[(df['Quantity'] > 0)]

    df = df.drop('StockCode', 1)

    return df


def create_rfm_dataset(df):
    df['TotalPrice'] = df['Quantity'] * df['Price']
    max_date = df['InvoiceDate'].max()
    present = dt.datetime(max_date.year, max_date.month, max_date.day + 1)
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    rfm = df.groupby('Customer ID').agg({'InvoiceDate': lambda date: (present - date.max()).days,
                                         'Invoice': lambda num: len(num),
                                         'TotalPrice': lambda price: price.sum()})

    rfm.columns = ['Frequency', 'Recency', 'Monetary']
    rfm['Recency'] = rfm['Recency'].astype(int)
    return rfm


def apply_log1p_transformation(dataframe, column):
    dataframe["log_" + column] = np.log1p(dataframe[column])
    return dataframe["log_" + column]


def rfm_processing(rfm):
    apply_log1p_transformation(rfm, "Frequency")
    apply_log1p_transformation(rfm, "Recency")
    apply_log1p_transformation(rfm, "Monetary")

    return rfm


def make_list_of_k(K, dataframe):
    cluster_values = list(range(1, K + 1))
    inertia_values = []

    for c in cluster_values:
        model = KMeans(
            n_clusters=c,
            init='k-means++',
            max_iter=500,
            random_state=42
        )
        model.fit(dataframe)
        inertia_values.append(model.inertia_)

    return inertia_values


def find_k(rfm):
    results = make_list_of_k(15, rfm.iloc[:, 3:])
    k_values_distances = pd.DataFrame({"clusters": list(range(1, 16)),
                                       "within cluster sum of squared distances": results})
    return k_values_distances


def kmeans_clustering(rfm):
    updated_kmeans_model = KMeans(n_clusters=4, init='k-means++', max_iter=500, random_state=42)
    updated_kmeans_model.fit_predict(rfm.iloc[:, 3:])
    cluster_centers = updated_kmeans_model.cluster_centers_
    actual_data = np.expm1(cluster_centers)
    add_points = np.append(actual_data, cluster_centers, axis=1)
    add_points = np.append(add_points, [[0], [1], [2], [3]], axis=1)
    rfm["clusters"] = updated_kmeans_model.labels_
    centers_df = pd.DataFrame(data=add_points, columns=["Frequency", "Recency", "Monetary", "log_Frequency",
                                                        "log_Recency", "log_Monetary", "clusters"])
    centers_df["clusters"] = centers_df["clusters"].astype("int")

    rfm["is_center"] = 0
    centers_df["is_center"] = 1
    rfm = rfm.append(centers_df, ignore_index=True)
    rfm["cluster_name"] = rfm["clusters"].astype(str)

    return rfm
