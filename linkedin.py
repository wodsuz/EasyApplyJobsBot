import math
import time

import config
import constants
import models
import repository_wrapper
import utils
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utils import prGreen, prRed, prYellow
from webdriver_manager.chrome import ChromeDriverManager


class Linkedin:
    def __init__(self):
        prYellow("🌐 The Bot is starting.")

        if config.chromeDriverPath != "":
            # Specify the path to Chromedriver provided by the Alpine package
            service = ChromeService(executable_path=config.chromeDriverPath)
        else:
            service = ChromeService(ChromeDriverManager().install())
        
        self.driver = webdriver.Chrome(service=service, options=utils.chromeBrowserOptions())        
        self.wait = WebDriverWait(self.driver, 15)

        # Navigate to the LinkedIn home page to check if we're already logged in
        self.goToUrl("https://www.linkedin.com")

        if not self.checkIfLoggedIn():
            self.goToUrl("https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin")

            prYellow("🔄 Trying to log in linkedin...")
            try:    
                self.driver.find_element("id","username").send_keys(config.email)
                utils.sleepInBetweenActions(1,2)
                self.driver.find_element("id","password").send_keys(config.password)
                utils.sleepInBetweenActions(1, 2)
                self.driver.find_element("xpath",'//button[@type="submit"]').click()
                utils.sleepInBetweenActions(3, 7)
                self.checkIfLoggedIn()
            except:
                prRed("❌ Couldn't log in Linkedin by using Chrome. Please check your Linkedin credentials on config files line 7 and 8. If error continue you can define Chrome profile or run the bot on Firefox")
        
        repository_wrapper.init()
    

    def checkIfLoggedIn(self):
        if self.exists(self.driver, By.CSS_SELECTOR, "img.global-nav__me-photo.evi-image.ember-view"):
            prGreen("✅ Logged in Linkedin.")
            return True
        else:
            return False


    def startApplying(self):
        try:
            jobCounter = models.JobCounter()

            urlData = utils.LinkedinUrlGenerate().generateUrlLinks()

            for url in urlData:        
                self.goToUrl(url)

                urlWords = utils.urlToKeywords(url)
                
                try:
                    totalJobs = self.wait.until(EC.presence_of_element_located((By.XPATH, '//small'))).text # TODO - fix finding total jobs
                    # totalJobs = self.driver.find_element(By.XPATH,'//small').text 

                    totalSearchResultPages = utils.jobsToPages(totalJobs)

                    lineToWrite = "\n Search keyword: " + urlWords[0] + ", Location: " + urlWords[1] + ", Found " + str(totalJobs)
                    self.displayWriteResults(lineToWrite)

                    for searchResultPage in range(totalSearchResultPages):
                        currentSearchResultPageJobs = constants.jobsPerPage * searchResultPage
                        url = url + "&start=" + str(currentSearchResultPageJobs)
                        self.goToUrl(url)

                        jobIds = self.getJobIdsFromSearchPage()

                        for jobID in jobIds:
                            jobCounter = self.processJob(jobID=jobID, jobCounter=jobCounter)
                                    
                except TimeoutException:
                    prRed("0 jobs found for: " + urlWords[0] + " in " + urlWords[1])

                prYellow("Category: " + urlWords[0] + " in " + urlWords[1]+ " applied: " + str(jobCounter.applied) +
                    " jobs out of " + str(jobCounter.total) + ".")

        except Exception as e:
            utils.displayWarning(config.displayWarnings, "Unhandled exception in startApplying", e, True)
            self.driver.save_screenshot("unhandled_exception.png")
            with open("page_source_at_unhandled_exception.html", "w") as file:
                file.write(self.driver.page_source)

    
    def goToUrl(self, url):
        self.driver.get(url)
        utils.sleepInBetweenActions()
        

    def goToJobPage(self, jobID):
        jobPage = 'https://www.linkedin.com/jobs/view/' + str(jobID)
        self.goToUrl(jobPage)
        return jobPage


    def processJob(self, jobID: str, jobCounter: models.JobCounter):
        jobPage = self.goToJobPage(jobID)
        jobCounter.total += 1
        utils.sleepInBetweenBatches(jobCounter.total)

        jobProperties = self.getJobProperties()
        if self.isJobBlacklisted(jobProperties): 
            jobCounter.skipped_blacklisted += 1
            lineToWrite = self.getLogTextForJobProperties(jobProperties, jobCounter) + " | " + "* 🤬 Blacklisted Job, skipped!: " + str(jobPage)
            self.displayWriteResults(lineToWrite)

        else:        
            jobCounter = self.handleJobPost(
                jobPage=jobPage, 
                jobProperties=jobProperties, 
                jobCounter=jobCounter)

        return jobCounter
    
    
    def getJobIdsFromSearchPage(self):
        jobsPerPage = self.driver.find_elements(By.XPATH,'//li[@data-occludable-job-id]')
        jobIds = []

        for jobPage in jobsPerPage:
            if self.exists(jobPage, By.XPATH, ".//*[contains(text(), 'Applied')]"):
                if config.displayWarnings:
                    prYellow("⚠️ Not adding a job id as I already applied to this job")
                continue
            
            jobId = jobPage.get_attribute("data-occludable-job-id")
            jobIds.append(int(jobId.split(":")[-1]))

        return jobIds
    

    def getLogTextForJobProperties(self, jobProperties: models.Job, jobCounter: models.JobCounter):
        textToWrite = str(jobCounter.total) + " | " + jobProperties.title +  " | " + jobProperties.company +  " | " + jobProperties.location + " | " + jobProperties.workplace_type + " | " + jobProperties.posted_date + " | " + jobProperties.applicants_at_time_of_applying
        if self.isJobBlacklisted(jobProperties):
            textToWrite = textToWrite + " | " + "blacklisted"

        return textToWrite
        

    def handleJobPost(self, jobPage, jobProperties: models.Job, jobCounter: models.JobCounter):
        if self.exists(self.driver, By.CSS_SELECTOR, "button[aria-label*='Easy Apply']"):
            # button = self.driver.find_element(By.XPATH,
            #     '//button[contains(@class, "jobs-apply-button")]')
            # button = self.driver.find_element(By.CSS_SELECTOR, "button:contains('Easy Apply')")
            button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label*='Easy Apply']")
            utils.interact(lambda : self.click_button(button))
            
            # Now, the easy apply popup should be open
            if self.exists(self.driver, By.CSS_SELECTOR, "button[aria-label='Submit application']"):
                jobCounter = self.handleSubmitPage(jobPage, jobProperties, jobCounter)
            elif self.exists(self.driver, By.CSS_SELECTOR, "button[aria-label='Continue to next step']"):
                jobCounter = self.handleMultiplePages(jobPage, jobProperties, jobCounter)

        else:
            jobCounter.skipped_already_applied += 1
            lineToWrite = self.getLogTextForJobProperties(jobProperties, jobCounter) + " | " + "* 🥳 Already applied! Job: " + str(jobPage)
            self.displayWriteResults(lineToWrite)

        return jobCounter
    

    def chooseResumeIfPossible(self):
        if self.isResumePage():
            utils.interact(lambda : self.clickIfExists(By.CSS_SELECTOR, "button[aria-label='Show more resumes']"))

            # Find all CV container elements
            cv_containers = self.driver.find_elements(By.CSS_SELECTOR, ".jobs-document-upload-redesign-card__container")

            # Loop through the elements to find the desired CV
            for container in cv_containers:
                cv_name_element = container.find_element(By.CLASS_NAME, "jobs-document-upload-redesign-card__file-name")
                
                if config.distinctCVKeyword[0] in cv_name_element.text:
                    # Check if CV is already selected
                    if 'jobs-document-upload-redesign-card__container--selected' not in container.get_attribute('class'):
                        utils.interact(lambda : self.click_button(cv_name_element))
                    # exit the loop once the desired CV is found and selected
                    break  


    def isResumePage(self):
        upload_button_present = self.exists(self.driver, By.CSS_SELECTOR, "label.jobs-document-upload__upload-button")
        resume_container_present = self.exists(self.driver, By.CSS_SELECTOR, "div.jobs-document-upload-redesign-card__container")
        return upload_button_present and resume_container_present


    def getJobProperties(self): 
        jobTitle = self.getJobTitle()
        jobCompany = ""
        jobLocation = self.getJobLocation()
        jobWorkPlaceType = self.getJobWorkPlaceType()
        jobPostedDate = ""
        jobApplications = ""
        jobDescription = self.getJobDescription()

        # First, find the container that holds all the elements.
        if self.exists(self.driver, By.XPATH, "//div[contains(@class, 'job-details-jobs')]//div"):
            primary_description_div = self.driver.find_element(By.XPATH, "//div[contains(@class, 'job-details-jobs')]//div")
            jobCompany = self.getJobCompany(primary_description_div)
            jobPostedDate = self.getJobPostedDate(primary_description_div)
            jobApplications = self.getJobApplications(primary_description_div)

        return models.Job(
            title=jobTitle,
            company=jobCompany,
            location=jobLocation,
            description=jobDescription,
            workplace_type=jobWorkPlaceType,
            posted_date=jobPostedDate,
            applicants_at_time_of_applying=jobApplications,
        )
    

    def getJobTitle(self):
        jobTitle = ""

        try:
            jobTitle = self.driver.find_element(By.XPATH, "//h1[contains(@class, 'job-title')]").get_attribute("innerHTML").strip()
        except Exception as e:
            utils.displayWarning(config.displayWarnings, "in getting jobTitle", e)

        return jobTitle
    

    def getJobCompany(self, primary_description_div):
        jobCompany = ""

        if self.exists(primary_description_div, By.CSS_SELECTOR, "a.app-aware-link"):
            # Inside this container, find the company name link.
            jobCompanyLink = primary_description_div.find_element(By.CSS_SELECTOR, "a.app-aware-link")
            jobCompany = jobCompanyLink.text.strip()
        else:
            utils.displayWarning(config.displayWarnings, "in getting jobCompany")

        return jobCompany
    
    
    def getJobLocation(self):
        jobLocation = ""

        try:
            jobLocation = self.driver.find_element(By.XPATH,"//span[contains(@class, 'bullet')]").get_attribute("innerHTML").strip()
        except Exception as e:
            utils.displayWarning(config.displayWarnings, "in getting jobLocation", e)

        return jobLocation
    

    def getJobWorkPlaceType(self):
        jobWorkPlaceType = ""

        try:
            jobWorkPlaceType = self.driver.find_element(By.XPATH,"//span[contains(@class, 'workplace-type')]").get_attribute("innerHTML").strip()
        except Exception as e:
            utils.displayWarning(config.displayWarnings, "in getting jobWorkPlaceType", e)
            
        return jobWorkPlaceType

    # TODO Use jobDetail later
    def getJobDescription(self):
        jobDescription = ""

        try:
            jobDescription = self.driver.find_element(By.XPATH, "//div[contains(@class, 'job-details-jobs')]//div").text.replace("·", "|")
        except Exception as e:
            if (config.displayWarnings):
                utils.displayWarning("in getting jobDescription: ", e)

        return jobDescription        


    def getJobApplications(self, primary_description_div):
        if self.exists(primary_description_div, By.CSS_SELECTOR, "span.tvm__text--neutral"):
            neutral_text_spans = primary_description_div.find_elements(By.CSS_SELECTOR, "span.tvm__text--neutral")
            for span in neutral_text_spans:
                if "applicant" in span.text.lower():  # Catches 'applicant' and 'applicants'
                    return span.text.strip()
        else:
            utils.displayWarning(config.displayWarnings, "in getting jobApplications")
        return ""


    def getJobPostedDate(self, primary_description_div):
        if self.exists(primary_description_div, By.CSS_SELECTOR, "span.tvm__text--neutral"):
            neutral_text_spans = primary_description_div.find_elements(By.CSS_SELECTOR, "span.tvm__text--neutral")
            for span in neutral_text_spans:
                if self.exists(span, By.TAG_NAME, 'span'):
                    date_span = span.find_element(By.TAG_NAME, 'span')
                    if date_span:
                        return date_span.text.strip()
        else:
            utils.displayWarning(config.displayWarnings, "in getting jobPostedDate")
        return ""
    

    def isJobBlacklisted(self, job: models.Job):
        is_blacklisted = any(blacklistedCompany.strip().lower() == job.company.lower() for blacklistedCompany in config.blacklistCompanies)
        if is_blacklisted:
            return True

        is_blacklisted = any(blacklistedTitle.strip().lower() in job.title.lower() for blacklistedTitle in config.blackListTitles)
        if is_blacklisted:
            return True

        return False

    
    def handleMultiplePages(self, jobPage, jobProperties: models.Job, jobCounter: models.JobCounter):
        utils.interact(lambda : self.clickIfExists(By.CSS_SELECTOR, "button[aria-label='Continue to next step']"))

        comPercentage = self.driver.find_element(By.XPATH,'html/body/div[3]/div/div/div[2]/div/div/span').text
        percentage = int(comPercentage[0:comPercentage.index("%")])
        applyPages = math.ceil(100 / percentage) - 2
        try:
            for _ in range(applyPages):
                self.handleApplicationStep()
                utils.interact(lambda : self.clickIfExists(By.CSS_SELECTOR,"button[aria-label='Continue to next step']"))

            self.handleApplicationStep()
            utils.interact(lambda : self.clickIfExists(By.CSS_SELECTOR,"button[aria-label='Review your application']"))

            jobCounter = self.handleSubmitPage(jobPage, jobProperties, jobCounter)
        except:
            jobCounter.skipped_unanswered_questions += 1
            # TODO Instead of except, output which questions need to be answered
            lineToWrite = self.getLogTextForJobProperties(jobProperties, jobCounter) + " | " + "* 🥵 " + str(applyPages) + " Pages, couldn't apply to this job! Extra info needed. Link: " + str(jobPage)
            self.displayWriteResults(lineToWrite)

        return jobCounter
        
    def handleSubmitPage(self, jobPage, jobProperties: models.Job, jobCounter: models.JobCounter):
        followCompany = self.driver.find_element(By.CSS_SELECTOR,"label[for='follow-company-checkbox']")
        # Use JavaScript to check the state of the checkbox
        is_followCompany_checked = self.driver.execute_script("""
            var label = arguments[0];
            var checkbox = document.getElementById('follow-company-checkbox');
            var style = window.getComputedStyle(label, '::after');
            var content = style.getPropertyValue('content');
            // Check if content is not 'none' or empty which may indicate the presence of the ::after pseudo-element
            return checkbox.checked || (content && content !== 'none' && content !== '');
        """, followCompany)
        if config.followCompanies != is_followCompany_checked:
            utils.interact(lambda : self.click_button(followCompany))

        utils.interact(lambda : self.clickIfExists(By.CSS_SELECTOR,"button[aria-label='Submit application']"))
        lineToWrite = self.getLogTextForJobProperties(jobProperties, jobCounter.total) + " | " + "* 🥳 Just Applied to this job: " + str(jobPage)
        self.displayWriteResults(lineToWrite)

        jobCounter.applied += 1
        return jobCounter

    def displayWriteResults(self, lineToWrite: str):
        try:
            prYellow(lineToWrite)
            utils.writeResults(lineToWrite)
        except Exception as e:
            prRed("❌ Error in DisplayWriteResults: " + str(e))

    def handleApplicationStep(self):
        self.chooseResumeIfPossible()
        # TODO self.handleQuestions()

    def handleQuestions(self):
        if self.exists(self.driver, By.CSS_SELECTOR, "div.pb4"):
            # Locate the div that contains all the questions
            questionsContainer = self.driver.find_element(By.CSS_SELECTOR, "div.pb4")

            if self.exists(questionsContainer, By.CSS_SELECTOR, "div.jobs-easy-apply-form-section__grouping"):
                # Find all question groups within that div
                questionGroups = questionsContainer.find_elements(By.CSS_SELECTOR, "div.jobs-easy-apply-form-section__grouping")

                # Iterate through each question group
                for group in questionGroups:
                    # TODO Next commented code is to handle city selection and other dropdowns
                    """  
                    # Find the element (assuming you have a way to locate this div, here I'm using a common class name they might share)
                    div_element = self.driver.find_element(By.CLASS_NAME, "common-class-name")

                    # Check for the specific data-test attribute
                    if div_element.get_attribute("data-test-single-typeahead-entity-form-component") is not None:
                        # Handle the first type of div
                        print("This is the first type of div with data-test-single-typeahead-entity-form-component")

                    elif div_element.get_attribute("data-test-single-line-text-form-component") is not None:
                        # Handle the second type of div
                        print("This is the second type of div with data-test-single-line-text-form-component")

                    else:
                        # Handle the case where the div doesn't match either type
                        print("The div doesn't match either specified type")
                    """

                    if self.exists(group, By.CSS_SELECTOR, "label.artdeco-text-input--label"):
                        # Find the label for the question within the group
                        questionLabel = group.find_element(By.CSS_SELECTOR, "label.artdeco-text-input--label").text
                        
                        # Determine the type of question and call the appropriate handler
                        if self.exists(group, By.CSS_SELECTOR, "input.artdeco-text-input--input"):
                            self.handleTextInput(group, questionLabel, By.CSS_SELECTOR, "input.artdeco-text-input--input")
                        elif self.exists(group, By.CSS_SELECTOR, "textarea"):
                            self.handleTextInput(group, questionLabel, By.CSS_SELECTOR, "textarea")
                        elif self.exists(group, By.CSS_SELECTOR, "input[type='radio']"):
                            self.handleRadioInput(group, questionLabel, By.CSS_SELECTOR, "input[type='radio']")
                        else:
                            self.logUnhandledQuestion(questionLabel)

    def exists(self, parent, by, value):
        # Check if an element exists on the page
        return len(parent.find_elements(by, value)) > 0
        
    def handleTextInput(self, group, questionLabel, by, value):
        # Locate the input element  
        inputElement = group.find_element(by, value)

        # Retrieve the value of the input element
        inputValue = inputElement.get_attribute('value')

        # Check if the input element is empty
        if inputValue == '':
            # TODO Check the backend for answers

            # TODO If there is an answer for this question, fill it in
            # If you want to fill the input
            # question_input.send_keys("Your answer here") then sleep
            # If no answers are found, move to the next step (backend should handle saving unanswered questions)
            if config.displayWarnings:
                prYellow(f"The input for '{questionLabel}' is empty.")
        else:
            # TODO Save answers to the backend if they are not already saved
            if config.displayWarnings:
                prYellow(f"The input for '{questionLabel}' has the following value: {inputValue}")


    def handleRadioInput(self, group, questionLabel, by, value):
        # Check if it's a radio selector question
        radioInputs = group.find_elements(by, value)
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


    def clickIfExists(self, by, selector):
        if self.exists(self.driver, by, selector):
            clickableElement = self.driver.find_element(by, selector)
            self.click_button(clickableElement)


    def click_button(self, button):
        try:
            button.click()
        except Exception as e:
            # If click fails, use JavaScript to click on the button
            self.driver.execute_script("arguments[0].click();", button)
