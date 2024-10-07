import sqlite3
import streamlit as st
import os 

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bus_data.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT DISTINCT route_name FROM bus_routes")
route_names = cursor.fetchall()
route_names = [name[0] for name in route_names]  

st.title("Bus Route Details")

selected_route = st.selectbox("Select a Route", route_names)


cursor.execute("""
    SELECT route_name, route_link, busname, bustype, departing_time, duration, reaching_time, star_rating, price, seats_available
    FROM bus_routes
    WHERE route_name = ?
""", (selected_route,))
route_details = cursor.fetchall()
print(route_details)

for detail in route_details:
        st.write("**Route Name:**", detail[0])
        st.write("**Route Link:**", detail[1])
        st.write("**Bus Name:**", detail[2])
        st.write("**Bus Type:**", detail[3])
        st.write("**Departing Time:**", detail[4])
        st.write("**Duration:**", detail[5])
        st.write("**Reaching Time:**", detail[6])
        st.write("**Star Rating:**", detail[7])
        st.write("**Price:**", detail[8])
        st.write("**Seats Available:**", detail[9])
        st.write("---") 

conn.close()
