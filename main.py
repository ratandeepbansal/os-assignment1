import streamlit as st
import pandas as pd
from statistics import mean


st.set_page_config(layout="wide")

st.sidebar.title("Outskill Hub")
st.sidebar.link_button("By Ratandeep Singh Bansal", "https://github.com/ratandeepbansal/")
st.title("Assignment 1")
st.caption("Read the CSV file and do some operations via functions")

# df = pd.read_csv("./ai_job_dataset.csv")
# st.write(df)

# GET DATA FROM FILE 
def get_file(filename):
    df = pd.read_csv("./" + filename)
    # st.write(df)
    st.write(df.columns)
    return df
st.subheader("0. About data")
with st.expander("Columns of data"):
    df = get_file("ai_job_dataset.csv")

#ALL COUNTRIES
def get_company_location(df):
    countries = []
    for item in df['company_location']:
        if item in countries:
            continue
        else:
            countries.append(item)
    return countries

st.subheader("1. Countries")
with st.expander("All Countries", ):
    countries = get_company_location(df)
    st.write(countries)

#SALARY RANGE IN COUNTRY
def get_salary_range_per_emp_type(df, country):
    new = df[df['company_location'] == country]
    range = []
    for item in new["salary_usd"]:
        if 'salary_usd' not in new.columns:
            raise ValueError("'salary_usd' column is missing from the DataFrame")
        range.append(item)
    if not range:
        return "No range"
    return f"${min(range)} - ${max(range)}"
st.subheader("2. Salary in country")
# st.code("India " + get_salary_range_per_emp_type(df, "India"))
# st.code("China " + get_salary_range_per_emp_type(df, "China"))
# st.code("United States " + get_salary_range_per_emp_type(df, "United States"))
# st.code("France " + get_salary_range_per_emp_type(df, "France"))
# st.code("Denmark " + get_salary_range_per_emp_type(df, "Denmark"))
with st.expander("Salaries across all cointries", ):
    for c in countries:
        st.code(c + " " + get_salary_range_per_emp_type(df, c))

#Get Avg Exp Per Level - for each countriy avg number of uears experience per level as a dict
def get_exp_years(df, c):
    sub = df[df['company_location'] == c]
    etypes = sub['employment_type'].unique()
    dict_return = {}
    for t in etypes:
        sub2 = sub[sub['employment_type'] == t ]
        years = sub2['years_experience'].dropna().tolist()
        if years:
            dict_return[t] = round(mean(years),2)
        else:
            dict_return[t] = None
    return f"For {c}: {dict_return}"
        # dictoo = []
        # sub2 = sub[sub['employment_type'] == t]
        # for item in sub2:
        #     dictoo.append(item['years_experience'])
        # dict_return += {t: mean(dict)}

st.subheader("3. Experience Range per country per level")
# dicc = get_exp_years(df, "India")
# st.code(dicc)
with st.expander("Experience range"):
    for c in countries:
        st.code(get_exp_years(df, c))

#4. Get Industry
def get_industry(df):
    return_dict = {}
    for c in countries:
        dis = df[df['company_location'] == c]
        ind = dis['industry'].unique()
        return_dict[c] = ind.tolist()
    return return_dict
st.subheader("4. Industiers in each country")
with st.expander("Industries"):
    st.write(get_industry(df))

#5. Get Benefit score range
def get_benefit_score(df):
    return_dictionary = {}
    for c in countries:
        benef = []
        sm = df[df['company_location'] == c]
        for item in sm['benefits_score']:
            benef.append(item)
        return_dictionary[c] = benef
    rows = []
    for c, s in return_dictionary.items():
        if s:
            rows.append({
                "Country": c,
                "min benefit score": min(s),
                "meann benefit score": round(mean(s),2),
                "max benefit score": max(s)
            })
    df_scores = pd.DataFrame(rows)
    return df_scores
st.subheader("5. Get Benefit Score as a new dataframe")
with st.expander("Benefits"):
    st.write(get_benefit_score(df))