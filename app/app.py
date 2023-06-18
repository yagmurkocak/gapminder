import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

def main():
    st.title('Gapminder')
    st.write('Unlocking Lifetimes: Visualizing Progress in Longevity and Poverty Eradication')

    # Load data 
    population_df = pd.read_csv(r"pop.csv")
    life_df = pd.read_csv(r"lex.csv")
    gni_df = pd.read_csv(r"gnipercapita.csv")

    # Fill missing values
    population_df = population_df.fillna(method="ffill")
    life_df = life_df.fillna(method="ffill")
    gni_df = gni_df.fillna(method="ffill")

    # Transform df into tidy data format
    population = pd.melt(population_df,id_vars=["country"],var_name="year",value_name="population")
    life = pd.melt(life_df,id_vars=["country"],var_name="year",value_name="life expectancy")
    gni = pd.melt(gni_df,id_vars=["country"],var_name="year",value_name="gni per capita")

    # Merge data
    df = population.merge(life, on=['country', 'year']).merge(gni, on=['country', 'year'])

    # Change data types
    df["year"] = df["year"].astype(int)
    df["population"] = df["population"].str.replace("k","e3").str.replace("M","e6").str.replace("B","e9").astype(float)
    df["gni per capita"] = df["gni per capita"].str.replace("k","e3").astype(float)
    df["life expectancy"] = df["life expectancy"].astype(float)

    # Create a slider for selecting the year
    selected_year = st.slider("Select a year", min_value=int(df["year"].min()), max_value=int(df["year"].max()))

    # Create a multiselect for selecting countries
    countries = st.multiselect("Select countries", df["country"].unique())

    # Filter data
    filtered_df = df[(df["year"] == selected_year) & (df["country"].isin(countries))]

    # Apply logarithmic transformation to "gni per capita" column
    filtered_df["log_gni"] = np.log10(filtered_df["gni per capita"].replace(0, np.nan))

    # Create a bubble chart
    if filtered_df.empty:
        st.write("No data available for the selected countries in the selected year.")
    else:
        fig = px.scatter(filtered_df,
                    x="log_gni",
                    y="life expectancy",
                    size="population",
                    color="country",
                    range_x=[0, 6.5],
                    labels={"log_gni": "Logarithmic GNI per capita (PPP)", "life expectancy": "Life expectancy"}
                    )
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()