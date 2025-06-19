import streamlit as st
import pandas as pd
from statistics import mean, median

# st.set_page_config(layout="wide")
st.title(":rainbow: Assignment 1")
st.sidebar.header("Outskill Hub")
st.sidebar.link_button("By Ratandeep Singh Bansal", "https://github.com/ratandeepbansal/")
st.sidebar.divider()
st.sidebar.link_button(":smile: Assignment Link Here", "https://drive.google.com/drive/folders/1v0l5-eiGXNgDr-keGL-K761U-71NZ_KG?usp=sharing")

############################################################
## 0. Read Data from CSV ###################################
############################################################
st.subheader("0. Get data from CSV")
def get_data(filename):
    return pd.read_csv(filename)
df = get_data("ai_job_dataset.csv")
with st.expander("DF from CSV"):
    st.write([df.columns])
    with st.expander("Full Data"):
        st.write(df)

############################################################
## 1. Get Company Location Country #########################
############################################################    
st.subheader("1. Company Location")
def get_countries(df):
    return df['company_location'].unique().tolist()
with st.expander("Get Company Locations"):
    st.write(get_countries(df))

############################################################
## 2. Get Salary Range for Exp Level #######################
############################################################      
st.subheader("2. Salary Range")
def salary_range(df, c):
    sub = df[df['company_location'] == c]
    etypes = sub['employment_type'].unique()
    return_dict = {}
    for t in etypes:
        # with st.expander("raw data"):
        #     st.write(t, " ", [sub[sub['employment_type'] == t]['salary_usd']])
        filtered = sub[sub['employment_type'] == t]
        salaries = filtered['salary_usd']
        return_dict[t] = [
                round(salaries.min()),
                round(salaries.mean()),
                round(salaries.median()),
                round(salaries.max())
            ]
    new_frame =  pd.DataFrame.from_dict(return_dict, orient='index', columns=[ "min", "mean", "median", "max"])
    new_frame.reset_index(inplace=True)
    new_frame.rename(columns={'index': 'employment_type'}, inplace=True)
    return new_frame
with st.expander("Get salary range per emp type (for country as input)"):
    selected_country = st.selectbox("Choose Country", get_countries(df), key="part2", placeholder="Select One Country")
    st.write(selected_country, salary_range(df, selected_country) )

############################################################
## 3. Get Avg Exp per Level ################################
############################################################     
st.subheader("3. Avg exp per level")
def avg_exp(df, c):
    # return "hello " + c
    sub = df[df['company_location'] == c]
    etypes = sub['employment_type'].unique()
    return_dict = {}
    for t in etypes:
        filtered = sub[sub['employment_type'] == t]
        experience = filtered['years_experience']
        return_dict[t] = round(experience.mean(),2)
        print("hello")
    return return_dict
    
with st.expander("Average experience per level (for country as input)"):
    selected_country_22 = st.selectbox("Choose Country", get_countries(df), key="part3",placeholder="Select One Country")
    st.write(avg_exp(df, selected_country_22))

############################################################
## 4. Get Industries for each country ######################
############################################################     
st.subheader("4. Industries")
def get_industries(df, c):
    # return "hello " + c
    number = df[df['company_location'] == c]['industry'].nunique()
    list = df[df['company_location'] == c]['industry'].unique().tolist()
    return f"There are {number} number of industries in {c}. And they are:\n- {'\n- '.join(list)}"
with st.expander("Number of Industries for selected country"):
    s_c = st.selectbox("Choose Country", get_countries(df), key="part4", placeholder="Select One Country")
    st.write(get_industries(df, s_c))
    
############################################################
## 5. Get Benefits  ########################################
############################################################ 
st.subheader("5. Benefits")
def get_benefits(df, c):
    # return "hello " + c
    sub = df[df['company_location'] == c]
    etypes = df['employment_type'].unique()
    return_dict = {}
    for t in etypes:
        filtered = sub[sub['employment_type'] == t]
        benefits = filtered['benefits_score']
        if benefits.empty:
            return "No Benefits"
        return_dict[t] = {
            'min': benefits.min(),
            'mean': round(benefits.mean(),2),
            'max': benefits.max()
        }
    new_frame2 = pd.DataFrame.from_dict(return_dict, orient="index")
    new_frame2.reset_index(inplace=True)
    new_frame2.rename(columns={'index': 'employment_type'}, inplace=True)
    return new_frame2
with st.expander("Benefit Score Range"):
    s_cc = st.selectbox("Choose Country", get_countries(df), key="part5", placeholder="Select One Country")
    st.write(s_cc, get_benefits(df, s_cc))