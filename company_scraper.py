from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import csv



#-----------------------------Scraper function-----------------------------------------#
class SCRAPER:
    def __init__(self):
        self.options = Options()
        self.options.add_argument('--headless')
        self.main()
        
    # scraper function will take url as input
    def COMPANIES_LINKS(self, url):
        lst = []
        
        pause = 5
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)
        driver.get(url)
        print('[INFO] downloading companies URLS...')
        try:
            last_height = driver.execute_script("return document.body.scrollHeight")
            
            while True:
                # Scroll down to bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
                # Wait to load page
                time.sleep(pause)
            
                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            time.sleep(pause)
            COMPANIES_TABLE = driver.find_element_by_css_selector('div.styles-module__section___2yul1.styles-module__results___2lP37')
            COMPANIES = COMPANIES_TABLE.find_elements_by_css_selector('a.styles-module__company___1UVnl.no-hovercard')    
            for COMPANY in COMPANIES:
                lst.append(COMPANY.get_attribute('href'))
        except:
            last_height = driver.execute_script("return document.body.scrollHeight")
            
            while True:
                # Scroll down to bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
                # Wait to load page
                time.sleep(pause)
            
                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            time.sleep(pause)
            COMPANIES_TABLE = driver.find_element_by_css_selector('div.styles-module__section___2yul1.styles-module__results___2lP37')
            COMPANIES = COMPANIES_TABLE.find_elements_by_css_selector('a.styles-module__company___1UVnl.no-hovercard')    
            for COMPANY in COMPANIES:
                lst.append(COMPANY.get_attribute('href'))
        # Get scroll height
        
        print('URLS found: ', len(lst))
        driver.quit()
        return lst        
    
    def COMPANIES_DATA(self, url):
        LIST = []
        # initialize and declare an empty list
        # use header to send request with different agents to avoid blocking
        hdr = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
        # send request to url
        req = Request(url,headers=hdr)
        # visiting html page
        page = urlopen(req)
        # check while page status code not equal to 200
        while page.getcode() != 200:
            page = urlopen(req)
        # put page content to beautiful soup parser to convert it to html contents
        soup = BeautifulSoup(page, "html.parser")
        # check if url is home page url
        
        # locate all the table in single container using div tag and css CLASS selector
        try:
            LOGO = soup.find('img', class_='w-32 h-32')
            LOGO_IMG = LOGO['src']
        except:
            LOGO_IMG = ''
        LIST.append(LOGO_IMG)
        try:
            COM_NAME_INdUSTYPE = soup.find('div', class_='space-y-3')
            COM_NAME           = COM_NAME_INdUSTYPE.find('div', class_='prose max-w-full').text
        except:
            COM_NAME = ''
        LIST.append(COM_NAME)
        try:
            TAGS_BOX = COM_NAME_INdUSTYPE.find('div', class_='flex flex-row align-center flex-wrap gap-y-2 gap-x-2')
            TAGS = TAGS_BOX.find_all('span')
            TAGS = [i.text for i in TAGS]
            TAGS = ','.join(TAGS)
        except:
            TAGS = ''
        LIST.append(TAGS)
        try:
            COM_INDUSTYPE      = COM_NAME_INdUSTYPE.find('div', class_='hidden md:block prose max-w-full').text
        except:
            COM_INDUSTYPE = ''
        LIST.append(COM_INDUSTYPE)
        try:
            COM_LINK_BOX1 = soup.find('div', class_='my-8 mb-4 hidden md:block')
            COM_LINK_BOX2 = COM_LINK_BOX1.find('div', class_='flex justify-between')
            COM_LINK_BOX3 = COM_LINK_BOX2.find('div', class_='flex flex-row items-center leading-none px-3')
            COM_LINK      = COM_LINK_BOX3.find('a')['href']
        except:
            COM_LINK = ''
        LIST.append(COM_LINK)
        try:
            FOUND_TEAM_LOCAT_LINKEDIN_BOX = soup.find('div', class_='ycdc-card space-y-1.5 sm:w-[300px]')
            FOUND_TEAM_LOCAT_CONT         = FOUND_TEAM_LOCAT_LINKEDIN_BOX.find('div', class_='space-y-0.5')
            FOUNDED_YEAR_                 = FOUND_TEAM_LOCAT_CONT.find_all('div', class_='flex flex-row justify-between')[0]
            FOUNDED_YEAR                  = FOUNDED_YEAR_.find_all('span')[1].text
        except:
            FOUNDED_YEAR = ''
        LIST.append(FOUNDED_YEAR)
        try:
            TEAM_SIZE_ = FOUND_TEAM_LOCAT_CONT.find_all('div', class_='flex flex-row justify-between')[1]
            TEAM_SIZE  = TEAM_SIZE_.find_all('span')[1].text
        except:
            TEAM_SIZE = ''
        LIST.append(TEAM_SIZE)
        try:
            LOCATION_ = FOUND_TEAM_LOCAT_CONT.find_all('div', class_='flex flex-row justify-between')[2]
            LOCATION = LOCATION_.find_all('span')[1].text
        except:
            LOCATION = ''
        LIST.append(LOCATION)
        COM_LINKEDIN = ''
        try:
            LINKEDIN_BOX = FOUND_TEAM_LOCAT_LINKEDIN_BOX.find('div', class_='space-x-2')
            COM_LINKEDIN    = LINKEDIN_BOX.find_all('a')[0]['href']
            if 'www.linkedin.com' in COM_LINKEDIN:
                COM_LINKEDIN = COM_LINKEDIN
            else:
                COM_LINKEDIN = ''
        except:
            COM_LINKEDIN = ''
        LIST.append(COM_LINKEDIN)
        
        FOUNDERS_LST = []
        FOUNDERS_LIST          = soup.find_all('div', class_='ycdc-card shrink-0 space-y-1.5 sm:w-[300px]')
        for FOUNDERS in FOUNDERS_LIST:
            
            FOUNDER_NAME           = FOUNDERS.find('div', class_='font-bold').text 
            FOUNDERS_LST.append(FOUNDER_NAME)
            FOUNDER_SOCIAL         = FOUNDERS.find('div', class_='mt-1 space-x-2') 
            FOUNDER_SOCIAL_        = FOUNDER_SOCIAL.find_all('a')
            FOUNDER_LINKEDIN = ''
            for FOUNDER_SOCIAL_LINKS in FOUNDER_SOCIAL_:
                FOUNDER_LINKEDIN = FOUNDER_SOCIAL_LINKS['href']
                if 'www.linkedin.com' in FOUNDER_LINKEDIN:
                    FOUNDER_LINKEDIN = FOUNDER_LINKEDIN
                else:
                    FOUNDER_LINKEDIN = ''
            
            FOUNDERS_LST.append(FOUNDER_LINKEDIN)
        LIST.append(FOUNDERS_LST)
            
        return LIST
    
    def main(self):
        header = ["COMPANY-NAME", "INDUSTRY-TYPE", "COMPANY-LOGO", "COMPANY TAGS", "COMPANY-LOCATION",
                  "COMPANY-WBESITE", "COMPANY-TEAM-SIZE", "COMPANY-FOUNDED-YEAR",
                  "COMPANY-LINKEDIN", 'COMPANY-FOUNDERS-DATA']
        lst = self.COMPANIES_LINKS('https://www.ycombinator.com/companies/')
        with open('Output.csv', 'w', newline = '') as output_csv:
            csv_writer = csv.writer(output_csv)
            csv_writer.writerow(header)
            for url in lst:
                print(url)
                data = self.COMPANIES_DATA(url)
                Data_lst = [data[1], data[3], data[0], data[2], data[7], data[4], data[6], data[5], data[8], ', '.join(data[9])]
                csv_writer.writerow(Data_lst)
        return
                
                
SCRAPER()