# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd


# Headings
st.title(":cup_with_straw: Customize your smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Name on your order
title = st.text_input('Name on smoothie:')
st.write("The name on your smoothie will be:", title)

# Making connection
cnx = st.connection("snowflake")
session = cnx.session()

# Drop list of ingredients
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients;', my_dataframe, max_selections=5
    
)

if ingredients_list:
    ingredients_string = ''
    for fruit in ingredients_list:
        ingredients_string += fruit + ' '
        st.subheader(fruit + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width = True)
    #st.write(ingredient_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + title + """')"""

#st.write(my_insert_stmt) 
#st.stop()

time_to_insert = st.button("Submit Order")
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success(f'Your Smoothie is ordered! {title}')






