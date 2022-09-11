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
        firefoxProfilePath = os.getenv('firefoxProfilePath')
   
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-extensions")

        # Disable webdriver flags or you will be easily detectable
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        # add profile 
        options.add_argument("-profile")
        options.add_argument(firefoxProfilePath)

        return options

    def Link_job_apply(self):
        countApplied = 0
        countJobs = 0

        urlData = utils.getUrlDataFile()

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
                    time.sleep(5)

                    countJobs += 1

                    jobProperties = self.getJobProperties(countJobs) 
                    time.sleep(5)
                    
                    button = self.easyApplyButton()

                    if button is not False:
                        button.click()
                        time.sleep(2)
                        countApplied += 1
                        try:
                            self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']").click()
                            time.sleep(3)
                            
                            lineToWrite = jobProperties + " | " + "* Just Applied to this job: "  +str(offerPage)
                            self.displayWriteResults(lineToWrite)

                        except:
                            try:
                                self.driver.find_element(By.CSS_SELECTOR,"button[aria-label='Continue to next step']").click()
                                time.sleep(3)

                                comPercentage = self.driver.find_element(By.XPATH,'html/body/div[3]/div/div/div[2]/div/div/span').text
                                percenNumber = int(comPercentage[0:comPercentage.index("%")])
                                self.applyProcess(percenNumber,offerPage)
                            
                            except Exception as e: 
                                lineToWrite = jobProperties + " | " + "* Cannot apply to this Job! " +str(offerPage)
                                self.displayWriteResults(lineToWrite)
                    else:
                        lineToWrite = jobProperties + " | " + "* Already applied! Job: " +str(offerPage)
                        self.displayWriteResults(lineToWrite)

                    time.sleep(2)

            urlWords =  utils.urlToKeywords(url)
            print("Category: " + urlWords[0] + "," +urlWords[1]+ " applied: " + str(countApplied) +
                  " jobs out of " + str(countJobs) + ".")
        
        self.donate()

    def getJobProperties(self, count):
        textToWrite = ""
        try: 
            jobTitle = self.driver.find_element(By.XPATH,"//h1[contains(@class, 'job-title')]").get_attribute("innerHTML").strip()
            jobCompany = self.driver.find_element(By.XPATH,"//a[contains(@class, 'ember-view t-black t-normal')]").get_attribute("innerHTML").strip()
            jobLocation = self.driver.find_element(By.XPATH,"//span[contains(@class, 'bullet')]").get_attribute("innerHTML").strip()
            jobWOrkPlace = self.driver.find_element(By.XPATH,"//span[contains(@class, 'workplace-type')]").get_attribute("innerHTML").strip()
            jobPostedDate = self.driver.find_element(By.XPATH,"//span[contains(@class, 'posted-date')]").get_attribute("innerHTML").strip()
            jobApplications= self.driver.find_element(By.XPATH,"//span[contains(@class, 'applicant-count')]").get_attribute("innerHTML").strip()
            textToWrite = str(count)+ " | " +jobTitle+  " | " +jobCompany+  " | "  +jobLocation+ " | "  +jobWOrkPlace+ " | " +jobPostedDate+ " | " +jobApplications
        except:
            textToWrite = " |  |  |  |  | " 
        return textToWrite

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
            print("* " +str(applyPages)+ " Pages, couldn't apply to this job! Extra info needed. Link: " +str(offerPage))
        return applyPages
    
    def donate(self):
        print('If you like the project, please support me so that i can make more such projects, thanks!')
        try:
            self.driver.get('https://commerce.coinbase.com/checkout/923b8005-792f-4874-9a14-2992d0b30685')
        except Exception as e:
            print(e)

    def displayWriteResults(self,lineToWrite: str):
        try:
            print(lineToWrite)
            utils.writeResults(lineToWrite)
        except Exception as e:
            print("Error in DisplayWriteResults: " +e)


start = time.time()
Linkedin().Link_job_apply()
end = time.time()
print("---Took: " + str(round((time.time() - start)/60)) + " minute(s).")
