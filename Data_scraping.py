import os
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import csv

#Funcion to create database
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bus_data.db')

def DataBase():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS bus_routes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        route_name TEXT,
                        route_link TEXT,
                        busname TEXT,
                        bustype TEXT,
                        departing_time TIME,
                        duration TEXT,
                        reaching_time TIME,
                        star_rating FLOAT,
                        price DECIMAL,
                        seats_available INT
                    )
                    ''')

    connection.commit()
    connection.close()

#Function to insert data in database

def insert_data(bus_route_name,route_link, bus_name, bus_type, departure_time, duration, arrival_time, rating, fare, seats_available):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO bus_routes (route_name,route_link, busname, bustype, departing_time, 
                 duration, reaching_time, star_rating, price, seats_available)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?,?, ?)''',
              (bus_route_name,route_link, bus_name, bus_type, departure_time, duration, arrival_time, rating, fare, seats_available))

    connection.commit()
    connection.close()

    print("Data inserted successfully in database.")

#Function to insert data in csv

def insert_data_into_csv(name, bus_name, bus_type, departure_time, duration, arrival_time, rating, fare, seats_available, file_path='buses.csv'):
    row = [name, bus_name, bus_type, departure_time, duration, arrival_time, rating, fare, seats_available]
    
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)

    print(f"Data successfully inserted into {file_path}")

#Funcion to get the bus data's
def bus(url):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(10)
    
    try:
        WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.ID, "result-section"))
        )
    except TimeoutException:
        print(f"Timeout or result not found: {url}")
        driver.quit()
        return

    try:
        result_section = driver.find_element(By.ID, "result-section")
        bus_items = result_section.find_elements(By.CLASS_NAME, "bus-item")
        processed_count = 0
        max_attempts = 10  
       
        while processed_count < 15 and max_attempts > 0:
            for bus in bus_items[processed_count:]:
                try:
                    driver.execute_script("arguments[0].scrollIntoView(true);", bus)

                    name = driver.find_element(By.XPATH, '//*[@id="mBWrapper"]/section/div[2]/h1').text
                    bus_name = bus.find_element(By.CLASS_NAME, "travels").text
                    bus_type = bus.find_element(By.CLASS_NAME, "bus-type").text
                    departure_time = bus.find_element(By.CLASS_NAME, "dp-time").text
                    duration = bus.find_element(By.CLASS_NAME, "dur").text
                    arrival_time = bus.find_element(By.CLASS_NAME, "bp-time").text

                    try:
                        rating = bus.find_element(By.CLASS_NAME, "rating").text
                    except NoSuchElementException:
                        rating = 'N/A'

                    fare = bus.find_element(By.CLASS_NAME, "fare").text.replace('INR', '').strip()
                    seats_available = bus.find_element(By.CLASS_NAME, "seat-left").text

                    if bus_name:
                        insert_data_into_csv(name, bus_name, bus_type, departure_time, duration, arrival_time, rating, fare, seats_available)
                        insert_data(name, url, bus_name, bus_type, departure_time, duration, arrival_time, rating, fare, seats_available)

                    processed_count += 1

                    if processed_count >= 15:
                        break

                except Exception as e:
                    print(f"Error extracting bus data: {e}")
                    continue

            if processed_count < 15:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)  
                bus_items = result_section.find_elements(By.CLASS_NAME, "bus-item")
                max_attempts -= 1

    except NoSuchElementException:
        print(f"No result section found on URL: {url}")
    finally:
        driver.quit()


# Main scraping 
def main():
    links = [
        "https://www.redbus.in/online-booking/west-bengal-transport-corporation",
        "https://www.redbus.in/online-booking/bihar-state-road-transport-corporation-bsrtc",
        "https://www.redbus.in/online-booking/north-bengal-state-transport-corporation",
        "https://www.redbus.in/online-booking/wbtc-ctc",
        "https://www.redbus.in/online-booking/bsrtc-operated-by-vip-travels",
        "https://www.redbus.in/online-booking/south-bengal-state-transport-corporation-sbstc",
        "https://www.redbus.in/online-booking/pepsu",
        "https://www.redbus.in/online-booking/pepsu-punjab",
        "https://www.redbus.in/online-booking/rsrtc",
        "https://www.redbus.in/online-booking/hrtc",
        "https://www.redbus.in/online-booking/uttar-pradesh-state-road-transport-corporation-upsrtc",
        "https://www.redbus.in/online-booking/chandigarh-transport-undertaking-ctu",
        "https://www.redbus.in/online-booking/ksrtc-kerala",
        "https://www.redbus.in/online-booking/ktcl",
        "https://www.redbus.in/online-booking/tsrtc",
        "https://www.redbus.in/online-booking/apsrtc",
        "https://www.redbus.in/online-booking/astc",
        "https://www.redbus.in/online-booking/kaac-transport",
        "https://www.redbus.in/online-booking/sikkim-nationalised-transport-snt",
        "https://www.redbus.in/online-booking/meghalaya-transport-corporation-mtc",
        "https://www.redbus.in/online-booking/gsrtc",
    ]

    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    DataBase()

    try:
        for link in links:
            print("first Link",link)
            driver.get(link)
            
            WebDriverWait(driver, 10).until( 
                EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[4]/div[2]/div[1]')) 
            )

            for i in range(2, 7):
                xpath_expression = f'//*[@id="root"]/div/div[4]/div[{i}]/div[1]'
                try:
                    parent_element = driver.find_element(By.XPATH, xpath_expression)
                    state_links = parent_element.find_elements(By.TAG_NAME, 'a')
                    for state_link in state_links:
                        href = state_link.get_attribute('href')
                        print(href)
                        bus(href)
                        
                except NoSuchElementException:
                    print(f"Element with XPath '{xpath_expression}' not found, skipping.")
                    continue
    except NoSuchElementException as e:
        print(f"Error finding main elements: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
