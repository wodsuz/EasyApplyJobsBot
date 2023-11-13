import time,math,os
import utils,constants,config
from utils import prRed,prYellow,prGreen

from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Linkedin:
    def __init__(self):
            prYellow("🌐 Bot will run in Chrome browser and log in Linkedin for you.")

            if config.chromeDriverPath != "":
                # Specify the path to Chromedriver provided by the Alpine package
                service = ChromeService(executable_path=config.chromeDriverPath)
            else:
                service = ChromeService(ChromeDriverManager().install())
            
            self.driver = webdriver.Chrome(service=service, options=utils.chromeBrowserOptions())
            self.driver.get("https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin")
            self.wait = WebDriverWait(self.driver, 15)

            prYellow("🔄 Trying to log in Linkedin...")
            try:    
                self.driver.find_element("id","username").send_keys(config.email)
                utils.sleepInBetweenActions(1,2)
                self.driver.find_element("id","password").send_keys(config.password)
                utils.sleepInBetweenActions(1, 2)
                self.driver.find_element("xpath",'//button[@type="submit"]').click()
                utils.sleepInBetweenActions(3, 7)
                self.linkJobApply()
            except:
                prRed("❌ Couldn't log in Linkedin by using Chrome. Please check your Linkedin credentials on config files line 7 and 8.")
    
    def generateUrls(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        try: 
            with open('data/urlData.txt', 'w',encoding="utf-8" ) as file:
                linkedinJobLinks = utils.LinkedinUrlGenerate().generateUrlLinks()
                for url in linkedinJobLinks:
                    file.write(url+ "\n")
            prGreen("✅ Apply urls are created successfully, now the bot will visit those urls.")
        except:
            prRed("❌ Couldn't generate urls, make sure you have editted config file line 25-39")

    def linkJobApply(self):
        try:
            self.generateUrls()
            countApplied = 0
            countJobs = 0

            urlData = utils.getUrlDataFile()

            for url in urlData:        
                self.driver.get(url)
                utils.sleepInBetweenActions()

                try:
                    totalJobs = self.wait.until(EC.presence_of_element_located((By.XPATH, '//small'))).text # TODO - fix finding total jobs
                    # totalJobs = self.driver.find_element(By.XPATH,'//small').text 

                    totalPages = utils.jobsToPages(totalJobs)

                    urlWords =  utils.urlToKeywords(url)
                    lineToWrite = "\n Search keyword: " + urlWords[0] + ", Location: " +urlWords[1] + ", Applying " +str(totalJobs)+ " jobs."
                    self.displayWriteResults(lineToWrite)

                    for page in range(totalPages):
                        currentPageJobs = constants.jobsPerPage * page
                        url = url +"&start="+ str(currentPageJobs)
                        self.driver.get(url)
                        utils.sleepInBetweenActions()

                        offersPerPage = self.driver.find_elements(By.XPATH,'//li[@data-occludable-job-id]')
                        offerIds = []

                        utils.sleepInBetweenActions()

                        for offer in offersPerPage:
                            if self.exists(offer, By.XPATH, ".//*[contains(text(), 'Applied')]"):
                                if config.displayWarnings:
                                    prYellow("⚠️ Not adding a job id as I already applied to this job")
                            else:
                                offerId = offer.get_attribute("data-occludable-job-id")
                                offerIds.append(int(offerId.split(":")[-1]))

                        for jobID in offerIds:
                            offerPage = 'https://www.linkedin.com/jobs/view/' + str(jobID)
                            self.driver.get(offerPage)
                            utils.sleepInBetweenActions()

                            countJobs += 1

                            jobProperties = self.getJobProperties(countJobs)
                            if "blacklisted" in jobProperties: 
                                lineToWrite = jobProperties + " | " + "* 🤬 Blacklisted Job, skipped!: " +str(offerPage)
                                self.displayWriteResults(lineToWrite)
                            
                            else:                    
                                easyApplyButton = self.easyApplyButton()

                                if easyApplyButton is not False:
                                    try:
                                        easyApplyButton.click()
                                    except:
                                        self.driver.execute_script("arguments[0].click();", easyApplyButton)
                                    
                                    utils.sleepInBetweenActions()
                                    
                                    try:
                                        self.handleResumeSelectionAndQuestions()
                                        self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']").click()
                                        utils.sleepInBetweenActions()

                                        lineToWrite = jobProperties + " | " + "* 🥳 Just Applied to this job: " + str(offerPage)
                                        self.displayWriteResults(lineToWrite)
                                        countApplied += 1

                                    except:
                                        try:
                                            self.handleResumeSelectionAndQuestions()
                                            self.driver.find_element(By.CSS_SELECTOR,"button[aria-label='Continue to next step']").click()
                                            utils.sleepInBetweenActions()

                                            comPercentage = self.driver.find_element(By.XPATH,'html/body/div[3]/div/div/div[2]/div/div/span').text
                                            percentNumber = int(comPercentage[0:comPercentage.index("%")])
                                            result = self.applyProcess(percentNumber, offerPage)
                                            lineToWrite = jobProperties + " | " + result
                                            self.displayWriteResults(lineToWrite)
                                        
                                        except Exception as e: 
                                            if(config.displayWarnings):
                                                prRed("⚠️ Warning in applying to job: " +str(e)[0:50])
                                            lineToWrite = jobProperties + " | " + "* 🥵 Cannot apply to this Job! " + str(offerPage)
                                            self.displayWriteResults(lineToWrite)
                                else:
                                    lineToWrite = jobProperties + " | " + "* 🥳 Already applied! Job: " + str(offerPage)
                                    self.displayWriteResults(lineToWrite)
                                    
                except TimeoutException:
                    prRed("Element not found within the time limit")
                    # TODO Handle the situation, like retrying, logging, or graceful shutdown

                prYellow("Category: " + urlWords[0] + "," +urlWords[1]+ " applied: " + str(countApplied) +
                    " jobs out of " + str(countJobs) + ".")
            
            utils.donate(self)

        except Exception as e:
            if config.displayWarnings:
                prYellow("⚠️ Exception caught: " +str(e)[0:50])

    def chooseResumeIfOffered(self):
        try: 
            beSureIncludeResumeTxt = self.driver.find_element(By.CLASS_NAME, "jobs-document-upload__title--is-required")
            if beSureIncludeResumeTxt.text == "Be sure to include an updated resume":
                more_resumes = self.driver.find_element(By.CSS_SELECTOR,"button[aria-label='Show more resumes']")
                if(more_resumes.is_displayed()):
                    more_resumes.click()
                    utils.sleepInBetweenActions()

                # Find all CV container elements
                cv_containers = self.driver.find_elements(By.CSS_SELECTOR, ".jobs-document-upload-redesign-card__container")

                # Loop through the elements to find the desired CV
                for container in cv_containers:
                    cv_name_element = container.find_element(By.CLASS_NAME, "jobs-document-upload-redesign-card__file-name")
                    
                    if config.distinctCVKeyword[0] in cv_name_element.text:
                        # Check if CV is already selected
                        if 'jobs-document-upload-redesign-card__container--selected' not in container.get_attribute('class'):
                            cv_name_element.click()  # Clicking on the CV name, adjust if needed
                            utils.sleepInBetweenActions()
                        # exit the loop once the desired CV is found and selected
                        break  
        except:
            pass

    def getJobProperties(self, count):
        textToWrite = ""
        jobTitle = ""
        jobLocation = ""

        try:
            jobTitle = self.driver.find_element(By.XPATH, "//h1[contains(@class, 'job-title')]").get_attribute("innerHTML").strip()
            res = [blItem for blItem in config.blackListTitles if (blItem.lower() in jobTitle.lower())]
            if (len(res) > 0):
                jobTitle += "(blacklisted title: " + ' '.join(res) + ")"
        except Exception as e:
            if (config.displayWarnings):
                prYellow("⚠️ Warning in getting jobTitle: " + str(e)[0:50])
            jobTitle = ""

        try:
            time.sleep(5)
            jobDetail = self.driver.find_element(By.XPATH, "//div[contains(@class, 'job-details-jobs')]//div").text.replace("·", "|")
            res = [blItem for blItem in config.blacklistCompanies if (blItem.lower() in jobTitle.lower())]
            if (len(res) > 0):
                jobDetail += "(blacklisted company: " + ' '.join(res) + ")"
        except Exception as e:
            if (config.displayWarnings):
                print(e)
                prYellow("⚠️ Warning in getting jobDetail: " + str(e)[0:100])
            jobDetail = ""

        try:
            jobWorkStatusSpans = self.driver.find_elements(By.XPATH, "//span[contains(@class,'ui-label ui-label--accent-3 text-body-small')]//span[contains(@aria-hidden,'true')]")
            for span in jobWorkStatusSpans:
                jobLocation = jobLocation + " | " + span.text

        except Exception as e:
            if (config.displayWarnings):
                print(e)
                prYellow("⚠️ Warning in getting jobLocation: " + str(e)[0:100])
            jobLocation = ""

        textToWrite = str(count) + " | " + jobTitle +" | " + jobDetail + jobLocation
        return textToWrite

    def easyApplyButton(self):
        try:
            utils.sleepInBetweenActions()
            button = self.driver.find_element(By.XPATH, "//div[contains(@class,'jobs-apply-button--top-card')]//button[contains(@class, 'jobs-apply-button')]")
            # button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label*='Easy Apply']")
            return button
        except: 
            return False

    def applyProcess(self, percentage, offerPage):
        applyPages = math.floor(100 / percentage) - 2
        result = ""  
        try:
            for pages in range(applyPages):
                self.handleResumeSelectionAndQuestions()
                self.driver.find_element(By.CSS_SELECTOR,"button[aria-label='Continue to next step']").click()
                utils.sleepInBetweenActions()

            self.handleResumeSelectionAndQuestions()
            self.driver.find_element(By.CSS_SELECTOR,"button[aria-label='Review your application']").click() 
            utils.sleepInBetweenActions()

            followCompany = self.driver.find_element(By.CSS_SELECTOR,"label[for='follow-company-checkbox']")
            # Use JavaScript to check the state of the checkbox
            is_followCompany_checked = self.driver.execute_script(
                "return document.getElementById('follow-company-checkbox').checked;"
            )
            if config.followCompanies != is_followCompany_checked:
                followCompany.click() 
                utils.sleepInBetweenActions()

            self.driver.find_element(By.CSS_SELECTOR,"button[aria-label='Submit application']").click()
            utils.sleepInBetweenActions()

            result = "* 🥳 Just Applied to this job: " + str(offerPage)
        except:
            result = "* 🥵 " + str(applyPages) + " Pages, couldn't apply to this job! Extra info needed. Link: " + str(offerPage)

        return result

    def displayWriteResults(self, lineToWrite: str):
        try:
            prYellow(lineToWrite)
            utils.writeResults(lineToWrite)
        except Exception as e:
            prRed("❌ Error in DisplayWriteResults: " +str(e))

    def handleResumeSelectionAndQuestions(self):
        self.chooseResumeIfOffered()
        self.handleQuestions()

    def handleQuestions(self):
        if self.exists(self.driver, By.CSS_SELECTOR, "div.pb4"):
            # Locate the div that contains all the questions
            questionsContainer = self.driver.find_element(By.CSS_SELECTOR, "div.pb4")

            if self.exists(questionsContainer, By.CSS_SELECTOR, "div.jobs-easy-apply-form-section__grouping"):
                # Find all question groups within that div
                questionGroups = questionsContainer.find_elements(By.CSS_SELECTOR, "div.jobs-easy-apply-form-section__grouping")

                # Iterate through each question group
                for group in questionGroups:
                    if self.exists(group, By.CSS_SELECTOR, "label.artdeco-text-input--label"):
                        # Find the label for the question within the group
                        questionLabel = group.find_element(By.CSS_SELECTOR, "label.artdeco-text-input--label").text
                        
                        # Determine the type of question and call the appropriate handler
                        if self.exists(group, By.CSS_SELECTOR, "input[type='text']"):
                            self.handleTextInput(group, questionLabel, "input[type='text']")
                        elif self.exists(group, By.CSS_SELECTOR, "input[type='radio']"):
                            self.handleRadioInput(group, questionLabel, "input[type='radio']")
                        # elif self.exists(group, By.CSS_SELECTOR, "select"):
                        #     self.handle_select_input(group, question_label)
                        else:
                            self.logUnhandledQuestion(questionLabel)

    def exists(self, parent, by, selector):
        # Check if an element exists on the page
        return len(parent.find_elements(by, selector)) > 0
        
    def handleTextInput(self, group, questionLabel, element):
        # Locate the input element  
        inputElement = group.find_element(By.CSS_SELECTOR, element)

        # Retrieve the value of the input element
        inputValue = inputElement.get_attribute('value')

        # Check if the input element is empty
        if inputValue == '':
            # TODO Check the backend for answers


            # TODO If there is an answer for this question, fill it in
            # If you want to fill the input
            # question_input.send_keys("Your answer here") then sleep
            # If no answers are found, move to the next step (backend should handle saving unanswered questions)
            prYellow("The input element is empty.")
        else:
            # TODO Save answers to the backend if they are not already saved
            prYellow(f"The input element has the following value: {inputValue}")

    def handleRadioInput(self, group, questionLabel, element):
        # Check if it's a radio selector question
        radioInputs = group.find_elements(By.CSS_SELECTOR, element)
        for radioInput in radioInputs:
            # Retrieve the associated label
            label = radioInput.find_element(By.XPATH, "./following-sibling::label").text
            # TODO Check the backend for answers. If there is an answer for this question, fill it in
            # Check or uncheck based on some condition
            # if "desired option" in label:
            #     prYellow(f"Selecting option: {label}")
            #     radio_input.click()  # Select the radio button if it's the desired option then sleep

    def logUnhandledQuestion(self, questionLabel):
        # Log or print the unhandled question
        prRed(f"Unhandled question: {questionLabel}")


start = time.time()
Linkedin().linkJobApply()
end = time.time()
prYellow("---Took: " + str(round((time.time() - start)/60)) + " minute(s).")
