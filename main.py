import pandas as pd
from time import sleep
from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver
from config.zipCodes import urls, base_url
from selenium.webdriver.chrome.options import Options



details = []

def get_data():
    options = Options()
    options.headless = True
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    for zip in urls:
        url = base_url + zip
        driver.get(url)
        sleep(randint(3,5))

        
        soup = BeautifulSoup(driver.page_source, 'lxml')
        mainsection = soup.find('div', class_='MuiTypography-root MuiTypography-body1')
        allAddress = mainsection.findAll('div', class_="MuiPaper-root jss326 MuiPaper-elevation1 MuiPaper-rounded")
        for section in allAddress:  
            try:    
                #Here is a findout address
                addresses = section.find('div', class_="MuiTypography-root jss329 MuiTypography-body2").text


                # This section findout the dates and time   
                dates = section.findAll('div', class_="MuiGrid-justify-content-xs-center")
                for data in dates:
                    date = data.findAll('div', class_="MuiTypography-root MuiTypography-body1")[0].text
                    time = data.findAll('div', class_="MuiTypography-root MuiTypography-body1")[1].text
                    
                    # Here is a try to decorate the data
                    
                    info = {
                        'date': date,
                        'time': time,
                        'address': addresses.split('|')[0]
                    }
                    details.append(info)
                    # print(info)
                    df_course = pd.DataFrame(details)
                    print(df_course)
                    #print csv file
                    df_course.to_csv('course_details.csv', index=False)
                    #print excel file
                    # df_course.to_excel('course_details.xlsx', index=False)
                    #print json file
                    # df_course.to_json('course_details.json', orient='records')                    
                    
            except:
                pass
    
    driver.quit()
get_data()                