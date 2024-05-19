# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(":cup_with_straw: Customise Your Smoothie :cup_with_straw:")
st.write(
    """ Choose the fruits you want in your custom smoothie!
    """
)

name_on_order = st.text_input("Name on Smoothie: ")
st.write("The name on your Smoothie will be: ", name_on_order)

# # Debugging - Print the contents of st.secrets
# st.write("Contents of st.secrets:")
# st.write(st.secrets)

# # Access Snowflake connection details from Streamlit secrets
# try:
#     snowflake_user = st.secrets["connections"]["snowflake"]["user"]
#     snowflake_password = st.secrets["connections"]["snowflake"]["password"]
#     snowflake_account = st.secrets["connections"]["snowflake"]["account"]
#     snowflake_warehouse = st.secrets["connections"]["snowflake"]["warehouse"]
#     snowflake_database = st.secrets["connections"]["snowflake"]["database"]
#     snowflake_schema = st.secrets["connections"]["snowflake"]["schema"]
#     st.write("Snowflake connection details loaded successfully.")
# except KeyError as e:
#     st.error(f"Missing key in secrets: {e}")
#     st.stop()






# session = get_active_session()
cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

# Multiselect
ingredients_list = st.multiselect(
    'Choose up to 5 ingregients:',
    my_dataframe, max_selections = 5)
if ingredients_list:
    ingredients_string = ''
    
    for Fruit_Chosen in ingredients_list:
        ingredients_string += Fruit_Chosen + ' '
        
    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string + """','"""+ name_on_order+"""')"""
    
    # st.write(my_insert_stmt)
    # st.stop()
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success('Your Smoothie is ordered!', icon="✅")

# New Section to display fruityvice nutrition information
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response.json())
fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
