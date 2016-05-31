import selenium, re, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup


def consoleit(arr):
	pass

try:
	
    display = Display(visible=0, size=(800, 600))
    display.start()
    driver = webdriver.Firefox()
    driver.get('http://my-gurukul.com/login.aspx?SID=1022')
    username_element = driver.find_element_by_name("txtUserName")
    username_element.send_keys("USERNAME")
    password_element = driver.find_element_by_name("txtPassword")
    password_element.send_keys("PASSWORD")
    password_element.send_keys(Keys.RETURN)
    time.sleep(5)
    
    #Begin the extraction 
    failcount=0
    start=102211000 #Starting Scan range
    everything = dict()
    high=0
    highdata=[]
    while(failcount<600): #Number of times to fail
            #URL below is the iframe of the result page
            driver.get('http://my-gurukul.com/frmStudentExamResultViewListFrame1.aspx?M_ISPOSTBACK=Y&M_EXAMNAME=MAY / JUNE 2016&M_SECTION=A&M_USERID='+str(start))
            start+=1
            page = driver.page_source
            
            soup = BeautifulSoup(page,"html.parser")
            data = []
            rows = soup.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele]) # Get rid of empty values

            try:
                subs = [row[3] for i,row in enumerate(data) if i<=8 and i>0]
                marks = [row[5] for i,row in enumerate(data) if i<=8 and i>0]
                m=float(data[-2][-1])
                if high<m and 'Software Engineering' in subs: #Check for a particular branch or field
                    high=m
                    highdata=data
                print("highest marks so far = ",high)
                #Make a dictionary
                i=0
                for sub in subs:
                    if sub in everything.keys():
                        everything[sub].append(marks[i])
                    else:
                        everything[sub]=list(marks[i])
                    i+=1

            except:
                print('Error Count = '+str(failcount)+',for id = '+str(start))
                failcount+=1
                continue


    #Prepare the CSV
    csv = open('op.csv','w')


    for sub,mark in everything.items():
        csv.write(sub+',')
        for m in mark:
            csv.write(m+',')
        csv.write('\n')
    csv.close()

    print("Highest Marks:")
    print(high)
    print(highdata)

except KeyboardInterrupt:
    driver.quit()
    display.stop()
