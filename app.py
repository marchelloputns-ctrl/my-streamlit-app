import streamlit as st
import pandas as pd
import plotly.express as px
st.title("Excel datu apskate ar filtriem un diagrammām")

# =============================
# 1) Augšupielāde
# =============================
uploaded = st.file_uploader("Augšupielādē Excel failu:", type=["xlsx"])

if uploaded:
    df = pd.read_excel(uploaded)
    st.success("Fails ielasīts!")

    st.subheader("Oriģinālie dati:")
    st.dataframe(df)

    # =============================
    # 2) Dinamiskie filtri
    # =============================

    # izvēlamies kolonnu, pēc kuras filtrēt
    filter_col = st.selectbox("Izvēlies kolonnu filtrēšanai:", df.columns)

    # vērtību saraksts kolonnā
    unique_values = df[filter_col].dropna().unique()

    # multiselect filtrs
    selected_values = st.multiselect(
        f"Izvēlies {filter_col} vērtības:", 
        options=unique_values,
        default=unique_values  # sākumā izvēlēti visi
    )

    # reālais filtrs
    filtered_df = df[df[filter_col].isin(selected_values)]

    st.subheader("Filtrētie dati:")
    st.dataframe(filtered_df)

    # =============================
    # 3) Diagrammas
    # =============================

    st.subheader("Diagramma no filtrētajiem datiem")

    # izvēlas diagrammas tipu
    chart_type = st.radio(
        "Izvēlies diagrammas veidu:",
        ["Līniju", "Stabiņu", "Area"],
        horizontal=True
    )

    # izvēlas kolonnu uz x ass un y ass
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns

    x_axis = st.selectbox("X ass kolonna:", df.columns)
    y_axis = st.selectbox("Y ass kolonna (skaitliska):", numeric_cols)

    if chart_type == "Līniju":
        st.line_chart(filtered_df.set_index(x_axis)[y_axis])
    elif chart_type == "Stabiņu":
        st.bar_chart(filtered_df.set_index(x_axis)[y_axis])
    elif chart_type == "Area":
        st.area_chart(filtered_df.set_index(x_axis)[y_axis])
        st.subheader("Papildu diagrammas")

    extra_chart = st.selectbox(
        "Izvēlies papildu diagrammas veidu:",
        ["Neviena", "Sektoru diagramma (Pie Chart)", "Histogramma", "Scatter (Izkliedes)"]
    )

    if extra_chart == "Sektoru diagramma (Pie Chart)":
        pie_column = st.selectbox("Izvēlies kolonnu sektoru diagrammai:", df.columns)

        fig = px.pie(df, names=pie_column, title=f"Sektoru diagramma: {pie_column}")
        st.plotly_chart(fig, use_container_width=True)

    elif extra_chart == "Histogramma":
        num_col = st.selectbox("Izvēlies skaitlisku kolonnu histogrammai:", numeric_cols)

        fig = px.histogram(df, x=num_col, nbins=20, title=f"Histogramma: {num_col}")
        st.plotly_chart(fig, use_container_width=True)

    elif extra_chart == "Scatter (Izkliedes)":
        x_col = st.selectbox("X ass:", numeric_cols)
        y_col = st.selectbox("Y ass:", numeric_cols)

        fig = px.scatter(df, x=x_col, y=y_col, title=f"Izkliedes diagramma: {x_col} vs {y_col}")
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Lūdzu augšupielādē Excel failu, lai turpinātu!")

