import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def select_columns(df):
    return df[['Country', 'EdLevel', 'YearsCodePro', 'Employment', 'ConvertedCompYearly']]

def rename_columns(df):
    return df.rename(columns={'EdLevel': 'Education', 'ConvertedCompYearly': 'Salary'})

def drop_na(df):
    return df.dropna()

def identify_countries(df, cutoff=400):
    # Count the registers per country
    country_counts = df['Country'].value_counts()
    countries_to_combine = country_counts[country_counts < cutoff].index
    df['Country'] = df['Country'].apply(lambda x: 'Other' if x in countries_to_combine else x)
    return df

def map_countries(df):
    # Map long country names to shorter versions
    country_mapping = {
        "United States of America": "United States",
        "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
        # Add more mappings as needed
    }
    return df.replace({'Country': country_mapping})

def filter_salary_range(df):
    return df[(df['Salary'] >= 10000) & (df['Salary'] <= 250000)]

def clean_experience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

def clean_years_code_pro(df):
    # Clean 'YearsCodePro' column
    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_experience)
    return df

def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

def clean_education_level(df):
    # Clean 'Education' column
    df['Education'] = df['Education'].apply(clean_education)
    return df

def dataframe_preprocessing(df):
    df = select_columns(df)
    df = rename_columns(df)
    df = drop_na(df)
    df = identify_countries(df)
    df = map_countries(df)
    df = filter_salary_range(df)
    df = clean_years_code_pro(df)
    df = clean_education_level(df)
    df = df[df['Employment'].str.contains('full-time', case=False, na=False)]
    return df


def show_explore_page():

    df = pd.read_csv('survey_results_public.csv')

    df = dataframe_preprocessing(df)


    # Grouping and aggregating by Country
    agg_df = df.groupby(['Country']).size().reset_index(name='Count')
    # Create a pie plot using Plotly Express
    fig1 = px.pie(agg_df, values='Count', names='Country', title='Software developers by Country')
    # Display the pie plot in Streamlit
    st.plotly_chart(fig1)

    # Grouping and aggregating by Education
    agg_df = df.groupby(['Education']).size().reset_index(name='Count')
    # Create a pie plot using Plotly Express
    fig2 = px.pie(agg_df, values='Count', names='Education', title='Software developers by Education')
    # Display the pie plot in Streamlit
    st.plotly_chart(fig2)

    # Create a boxplot using Plotly
    fig = px.box(df, x='Country', y='Salary', title='Boxplot of Salary by Country', height=500, width=800)
    fig.update_layout(xaxis_tickangle=-90)
    st.plotly_chart(fig)




    #################################################################3

    # Add a country filter using Streamlit
    all_countries_option = 'All Countries'
    selected_country = st.selectbox('Select a country', [all_countries_option] + list(df['Country'].unique()))

    # Filter the dataframe based on the selected country or all countries
    if selected_country == all_countries_option:
        filtered_df = df  # Show data for all countries
        country_title = 'All Countries'
    else:
        filtered_df = df[df['Country'] == selected_country]
        country_title = selected_country

    # Create a boxplot using Plotly for the filtered data
    fig3 = px.box(filtered_df, x='Education', y='Salary', title=f'Boxplot of Salary by Education in {country_title}',
                  height=500, width=800)
    fig3.update_layout(xaxis_tickangle=-90)

    # Display the Plotly chart using Streamlit
    st.plotly_chart(fig3)

    ######################################################################3
