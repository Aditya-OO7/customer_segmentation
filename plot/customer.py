import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def rfm_plot(rfm):
    fig = make_subplots(rows=3, cols=1,
                        subplot_titles=("Frequency",
                                        "Recency",
                                        "Monetary"))

    fig.append_trace(go.Histogram(x=rfm.Frequency),
                     row=1, col=1)

    fig.append_trace(go.Histogram(x=rfm.Recency),
                     row=2, col=1)

    fig.append_trace(go.Histogram(x=rfm.Monetary),
                     row=3, col=1)

    fig.update_layout(height=800, width=800)

    st.write(fig)


def rfm_log_plot(rfm):
    fig = make_subplots(rows=3, cols=1,
                        subplot_titles=("log_Frequency",
                                        "log_Recency",
                                        "log_Monetary"))

    fig.append_trace(go.Histogram(x=rfm.log_Frequency),
                     row=1, col=1)

    fig.append_trace(go.Histogram(x=rfm.log_Recency),
                     row=2, col=1)

    fig.append_trace(go.Histogram(x=rfm.log_Monetary),
                     row=3, col=1)

    fig.update_layout(height=800, width=800)

    st.write(fig)


def k_plot(k_values_distances):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=k_values_distances["clusters"],
                             y=k_values_distances["within cluster sum of squared distances"],
                             mode='lines+markers'))
    fig.update_layout(xaxis=dict(
        tickmode='linear',
        tick0=1,
        dtick=1),
        title_text="Within Cluster Sum of Squared Distances VS K Values",
        xaxis_title="K values",
        yaxis_title="Cluster sum of squared distances")
    st.write(fig)


def cluster_plot(rfm):
    fig = px.scatter_3d(rfm,
                        x="log_Frequency",
                        y="log_Recency",
                        z="log_Monetary",
                        color='cluster_name',
                        hover_data=["Frequency",
                                    "Recency",
                                    "Monetary"],
                        category_orders={"cluster_name": ["0", "1", "2", "3"]},
                        symbol="is_center"
                        )

    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    st.write(fig)


def cluster_graph_plot(rfm):
    cardinality_df = pd.DataFrame(
        rfm.cluster_name.value_counts().reset_index())

    cardinality_df.rename(columns={"index": "Customer Groups",
                                   "cluster_name": "Customer Group Magnitude"},
                          inplace=True)

    fig = px.bar(cardinality_df, x="Customer Groups",
                 y="Customer Group Magnitude",
                 color="Customer Groups",
                 category_orders={"Customer Groups": ["0", "1", "2", "3"]})
    fig.update_layout(xaxis=dict(
        tickmode='linear',
        tick0=1,
        dtick=1),
        yaxis=dict(
            tickmode='linear',
            tick0=1000,
            dtick=1000))

    st.write(fig)
