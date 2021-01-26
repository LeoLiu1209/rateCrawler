from selenium import webdriver                                  
from selenium.webdriver.chrome.options import Options                                                              
from selenium.webdriver.common.by import By                     
from selenium.webdriver.support.ui import WebDriverWait                                                            
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import random
import time
import yaml
import os
import datetime

retryCount = 0;
data_list = []
def autoFill(qDate):
    options = Options()
   
    try:
        chrome = webdriver.Chrome(options=options)
        getStr = "http://www.floatrates.com/historical-exchange-rates.html?currency_date="+qDate+"&base_currency_code=USD&format_type=html"
        chrome.get(getStr)

        oneUSD = chrome.find_elements_by_xpath("/html/body/div[1]/div[1]/div[3]/div/div[2]/table/tbody/tr[96]/td[3]")[0]
        oneUSDtext = oneUSD.get_attribute('innerText')

        data_list.append(qDate + "  " + "1USD : "+str(oneUSDtext)+ "\n")
        chrome.quit()

    except TimeoutException:
        chrome.quit()
        global retryCount
        retryCount+=1
        if(retryCount == 2):
            retryCount = 0
            pass
        else:
            autoFill(qDate)


if __name__ == "__main__":
    start = datetime.datetime.strptime("01-12-2020", "%d-%m-%Y")
    end = datetime.datetime.strptime("26-01-2021", "%d-%m-%Y")
    #(end-start).days+1) include today
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days+1)]

    for date in date_generated:
        qDate = date.strftime("%Y-%m-%d")
        autoFill(qDate);
    
    fp = open("rateData.txt", "a")
    fp.writelines(data_list)
    fp.close()