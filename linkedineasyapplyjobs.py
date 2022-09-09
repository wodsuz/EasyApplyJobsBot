import time,os,math
import jobPreferances.config as config,utils,constants
 
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

from dotenv import load_dotenv

class Linkedin:
    def __init__(self):
        load_dotenv()

        self.driver = webdriver.Firefox(options=self.browser_options())

        time.sleep(3)

    def browser_options(self):
        options = Options()
        firefoxAccountPath = os.getenv('firefoxAccountPath')
   
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-extensions")

        # Disable webdriver flags or you will be easily detectable
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        # add profile 
        options.add_argument("-profile")
        options.add_argument(firefoxAccountPath)

        return options

    def Link_job_apply(self):
        countApplied = 0
        countJobs = 0

        file = open('jobPreferances/urlData.txt', 'r')
        urlData = file.readlines()

        for url in urlData:        
            self.driver.get(url)

            totalJobs = self.driver.find_element(By.XPATH,'//small').text 
            totalPages = utils.jobsToPages(totalJobs)

            for page in range(totalPages):
                currentPageJobs = constants.jobsPerPage * page
                url = url +"&start="+ str(currentPageJobs)
                self.driver.get(url)
                time.sleep(5)

                offersPerPage = self.driver.find_elements(By.XPATH,'//li[@data-occludable-job-id]')

                offerIds = []
                for offer in offersPerPage:
                    offerId = offer.get_attribute("data-occludable-job-id")
                    offerIds.append(int(offerId.split(":")[-1]))

                for jobID in offerIds:
                    offerPage = 'https://www.linkedin.com/jobs/view/' + str(jobID)
                    self.driver.get(offerPage)
                    countJobs += 1
                    time.sleep(5)
                    
                    button = self.easyApplyButton()

                    if button is not False:
                        button.click()
                        time.sleep(2)
                        countApplied += 1
                        try:
                            self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']").click()
                            time.sleep(3)
                            print("* Just Applied to this job: " +str(offerPage))
                        except:
                            try:
                                self.driver.find_element(By.CSS_SELECTOR,"button[aria-label='Continue to next step']").click()
                                time.sleep(3)
                                comPercentage = self.driver.find_element(By.XPATH,'html/body/div[3]/div/div/div[2]/div/div/span').text
                                percenNumber = int(comPercentage[0:comPercentage.index("%")])

                                self.applyProcess(percenNumber,offerPage)
                            
                            except Exception as e: 
                                print("* Cannot apply to this job!")
                    else:
                        print("* Already applied!")
                    time.sleep(2)

            keyword, location = self.urlTokeywords(url)
            print("Category: " + keyword + "," +location+ " applied: " + str(countApplied) +
                  " jobs out of " + str(countJobs) + ".")

    def easyApplyButton(self):
        try:
            button = self.driver.find_element(By.XPATH,
                '//button[contains(@class, "jobs-apply-button")]')
            EasyApplyButton = button
        except: 
            EasyApplyButton = False

        return EasyApplyButton

    def applyProcess(self, percentage,offerPage):
        applyPages = math.floor(100 / percentage)   
        try:
            for pages in range(applyPages-2):
                self.driver.find_element(By.CSS_SELECTOR,"button[aria-label='Continue to next step']").click()
                time.sleep(3)
            self.driver.find_element(By.CSS_SELECTOR,"button[aria-label='Review your application']").click()
            time.sleep(3)
            self.driver.find_element(By.CSS_SELECTOR,"button[aria-label='Submit application']").click()
            time.sleep(3)
            print("* Just Applied to this job: " +str(offerPage))
        except:
            print("*" +str(applyPages)+ "Pages, couldn't apply to this job! Extra info needed. Link: " +str(offerPage))

        
        return applyPages
    
    def urlTokeywords(self,url):
        keyword = url[url.index("keywords=")+9:url.index("&location") ] 
        location = url[url.index("location=")+9:url.index("&f_E") ] 
        return (keyword,location)

start_time = time.time()
Linkedin().Link_job_apply()
end = time.time()
print("---Took: " + str(round((time.time() - start_time)/60)) + " minute(s).")
