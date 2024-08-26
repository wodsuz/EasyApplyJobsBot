import math
from typing import List

from typing import List

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


# This class is responsible for handling the LinkedIn job application process
# It uses the Selenium WebDriver to interact with the LinkedIn website
# It also uses the repository_wrapper to interact with the backend
#
# The class is responsible for:
# - Logging in to LinkedIn (done in the constructor)
# - Searching for jobs
# - Applying to jobs
# - Handling job posts
# - Handling questions
# - Handling multiple pages of the application process
# - Handling the resume selection
# - Handling the submission of the application
# - Handling the follow company checkbox
# - Handling the application of the job
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

            urlData = utils.LinkedinUrlGenerator().generateSearchUrls()

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

                        jobsForVerification = self.getJobsFromSearchPage()
                        verifiedJobs = repository_wrapper.verify_jobs(jobsForVerification)

                        for job in verifiedJobs:
                            jobCounter = self.processJob(jobID=job.linkedin_job_id, jobCounter=jobCounter)
                                    
                except TimeoutException:
                    prRed("0 jobs found for: " + urlWords[0] + " in " + urlWords[1])

                prYellow("Category: " + urlWords[0] + " in " + urlWords[1]+ " applied: " + str(jobCounter.applied) +
                    " jobs out of " + str(jobCounter.total) + ".")

        except Exception as e:
            utils.logDebugMessage("Unhandled exception in startApplying", utils.MessageTypes.ERROR, e, True)
            self.driver.save_screenshot("unhandled_exception.png")
            with open("page_source_at_unhandled_exception.html", "w") as file:
                file.write(self.driver.page_source)


    def goToJobsSearchPage(self):
        searchUrl = utils.LinkedinUrlGenerator.getGeneralSearchUrl()
        self.goToUrl(searchUrl)
        utils.sleepInBetweenActions()

    
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

        jobProperties = self.getJobProperties(jobID)
        repository_wrapper.update_job(jobProperties)
        if self.isJobBlacklisted(company=jobProperties.company, title=jobProperties.title): 
            jobCounter.skipped_blacklisted += 1
            lineToWrite = self.getLogTextForJobProperties(jobProperties, jobCounter) + " | " + "* 🤬 Blacklisted Job, skipped!: " + str(jobPage)
            self.displayWriteResults(lineToWrite)

        else:        
            jobCounter = self.handleJobPost(
                jobPage=jobPage, 
                jobProperties=jobProperties, 
                jobCounter=jobCounter)

        return jobCounter
    
    
    def getJobsFromSearchPage(self) -> List[models.JobForVerification]:
        jobsListItems = self.driver.find_elements(By.XPATH,'//li[@data-occludable-job-id]')
        jobsForVerification = []
        companyName = None
        jobTitle = None
        workPlaceType = None

        for jobItem in jobsListItems:
            if self.exists(jobItem, By.XPATH, ".//*[contains(text(), 'Applied')]"):
                if config.displayWarnings:
                    prYellow("⚠️  Not adding a job as I already applied to this job")
                continue

            companyNameSpan = jobItem.find_elements(By.XPATH, ".//span[contains(@class, 'job-card-container__primary-description')]")
            if companyNameSpan:
                full_description = companyNameSpan[0].text.strip()
                # Split the description to extract the company name before the '·' character
                companyName = full_description.split('·')[0].strip() if '·' in full_description else full_description

                if self.isCompanyBlacklisted(companyName):
                    if config.displayWarnings:
                        prYellow(f"⚠️  Not adding a job as the company '{companyName}' is blacklisted")
                    continue

            if companyName is None:
                utils.logDebugMessage("Couldn't find companyName", utils.MessageTypes.WARNING)
                continue

            jobTitleAnchor = jobItem.find_elements(By.XPATH, ".//a[contains(@class, 'job-card-container__link job-card-list__title')]")
            if len(jobTitleAnchor) > 0:
                allTexts = jobTitleAnchor[0].text.split("\n")
                uniqueTexts = list(dict.fromkeys(allTexts))
                jobTitle = uniqueTexts[0].strip()

                if self.isTitleBlacklisted(jobTitle):
                    if config.displayWarnings:
                        prYellow(f"⚠️  Not adding a job as the title '{jobTitle}' is blacklisted")
                    continue
            
            if jobTitle is None:
                utils.logDebugMessage("Couldn't find jobTitle", utils.MessageTypes.WARNING)
                continue

            workPlaceTypeSpan = jobItem.find_elements(By.XPATH, ".//li[contains(@class, 'job-card-container__metadata-item')]")
            if len(workPlaceTypeSpan) > 0:
                firstSpanText = workPlaceTypeSpan[0].text.strip()
                textWithinParentheses = utils.extractTextWithinParentheses(firstSpanText)
                workPlaceType = self.verifyWorkPlaceType(textWithinParentheses)
            
            if jobTitle is None:
                utils.logDebugMessage("Couldn't find jobTitle", utils.MessageTypes.WARNING)
                continue

            workPlaceTypeSpan = jobItem.find_elements(By.XPATH, ".//li[contains(@class, 'job-card-container__metadata-item')]")
            if len(workPlaceTypeSpan) > 0:
                firstSpanText = workPlaceTypeSpan[0].text.strip()
                textWithinParentheses = utils.extractTextWithinParentheses(firstSpanText)
                workPlaceType = self.verifyWorkPlaceType(textWithinParentheses)
            
            jobId = jobItem.get_attribute("data-occludable-job-id")

            if jobId is None:
                utils.logDebugMessage("Couldn't find jobID", utils.MessageTypes.WARNING)
                continue

            jobsForVerification.append(models.JobForVerification(
                linkedinJobId=jobId.split(":")[-1],
                title=jobTitle,
                company=companyName,
                workplaceType=workPlaceType))

        return jobsForVerification
    

    # TODO Move to logger.py (after splitting utils.py)
    def getLogTextForJobProperties(self, jobProperties: models.Job, jobCounter: models.JobCounter):
        textToWrite = str(jobCounter.total) + " | " + jobProperties.title +  " | " + jobProperties.company +  " | " + jobProperties.location + " | " + jobProperties.workplace_type + " | " + jobProperties.posted_date + " | " + jobProperties.applicants_at_time_of_applying
        if self.isJobBlacklisted(company=jobProperties.company, title=jobProperties.title):
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
    

    def chooseResumeIfPossible(self, jobProperties: models.Job):
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

                    # Update the backend to save the selected CV
                    repository_wrapper.attached_resume_to_job(jobProperties, cv_name_element.text)
                    # exit the loop once the desired CV is found and selected
                    break  


    def isResumePage(self):
        upload_button_present = self.exists(self.driver, By.CSS_SELECTOR, "label.jobs-document-upload__upload-button")
        resume_container_present = self.exists(self.driver, By.CSS_SELECTOR, "div.jobs-document-upload-redesign-card__container")
        return upload_button_present and resume_container_present


    def getJobProperties(self, jobID: str) -> models.Job: 
        jobTitle = self.getJobTitle()
        jobCompany = self.getJobCompany()
        jobLocation = ""
        jobPostedDate = ""
        numberOfApplicants = ""
        jobWorkPlaceType = self.getJobWorkPlaceType()
        jobDescription = self.getJobDescription()

        # First, find the container that holds all the elements.
        if self.exists(self.driver, By.XPATH, "//div[contains(@class, 'job-details-jobs-unified-top-card__primary-description-container')]//div"):
            primary_description_div = self.driver.find_element(By.XPATH, "//div[contains(@class, 'job-details-jobs-unified-top-card__primary-description-container')]//div")
            jobLocation = self.getJobLocation(primary_description_div)
            jobPostedDate = self.getJobPostedDate(primary_description_div)
            numberOfApplicants = self.getNumberOfApplicants(primary_description_div)
        else:
            utils.logDebugMessage("in getting primary_description_div", utils.MessageTypes.WARNING)

        return models.Job(
            title=jobTitle,
            company=jobCompany,
            location=jobLocation,
            description=jobDescription,
            workplace_type=jobWorkPlaceType,
            posted_date=jobPostedDate,
            applicants_at_time_of_applying=numberOfApplicants,
            linkedin_job_id=jobID
        )
    

    def getJobTitle(self):
        jobTitle = ""

        try:
            jobTitleElement = self.driver.find_element(By.CSS_SELECTOR, "h1.t-24.t-bold.inline")
            jobTitle = jobTitleElement.text.strip()
            jobTitleElement = self.driver.find_element(By.CSS_SELECTOR, "h1.t-24.t-bold.inline")
            jobTitle = jobTitleElement.text.strip()
        except Exception as e:
            utils.logDebugMessage("in getting jobTitle", utils.MessageTypes.WARNING, e)

        return jobTitle
    

    def getJobCompany(self):
        jobCompany = ""

        if self.exists(self.driver, By.XPATH, "//div[contains(@class, 'job-details-jobs-unified-top-card__company-name')]//a"):
            # Inside this container, find the company name link.
            jobCompanyElement = self.driver.find_element(By.XPATH, "//div[contains(@class, 'job-details-jobs-unified-top-card__company-name')]//a")
            jobCompany = jobCompanyElement.text.strip()
            
        else:
            utils.logDebugMessage("in getting jobCompany card", utils.MessageTypes.WARNING)

        return jobCompany        
    
    
    def getJobLocation(self, primary_description_div):
        jobLocation = ""

        try:
            jobLocationSpan = primary_description_div.find_element(By.XPATH, ".//span[contains(@class, 'tvm__text--low-emphasis')][1]")
            jobLocation = jobLocationSpan.text.strip()
        except Exception as e:
            utils.logDebugMessage("in getting jobLocation", utils.MessageTypes.WARNING, e)

        return jobLocation


    def getJobPostedDate(self, primary_description_div):
        jobPostedDate = ""

        try:
            postedDateSpan = primary_description_div.find_element(By.XPATH, ".//span[contains(@class, 'tvm__text--low-emphasis')][3]")
            jobPostedDate = postedDateSpan.text.strip()
        except Exception as e:
            utils.logDebugMessage("Error in getting jobPostedDate", utils.MessageTypes.WARNING, e)

        return jobPostedDate


    def getNumberOfApplicants(self, primary_description_div):
        jobApplications = ""

        try:
            applicationsSpan = primary_description_div.find_element(By.XPATH, ".//span[contains(@class, 'tvm__text--low-emphasis')][5]")
            jobApplications = applicationsSpan.text.strip()
        except Exception as e:
            utils.logDebugMessage("Error in getting jobApplications", utils.MessageTypes.WARNING, e)

        return jobApplications


    def getJobWorkPlaceType(self):
        jobWorkPlaceType = ""

        try:
            jobWorkPlaceTypeElement = self.driver.find_element(By.XPATH, "//li[contains(@class, 'job-details-jobs-unified-top-card__job-insight')]/span/span")
            firstSpanText = jobWorkPlaceTypeElement.text.strip()
            jobWorkPlaceType = self.verifyWorkPlaceType(firstSpanText)
            jobWorkPlaceTypeElement = self.driver.find_element(By.XPATH, "//li[contains(@class, 'job-details-jobs-unified-top-card__job-insight')]/span/span")
            firstSpanText = jobWorkPlaceTypeElement.text.strip()
            jobWorkPlaceType = self.verifyWorkPlaceType(firstSpanText)
        except Exception as e:
            utils.logDebugMessage("in getting jobWorkPlaceType", utils.MessageTypes.WARNING, e)
            
        return jobWorkPlaceType
    

    def verifyWorkPlaceType(self, text: str):
        if "Remote" or "On-site" or "Hybrid" in text:
            return text
        else:
            return None
    

    def verifyWorkPlaceType(self, text: str):
        if "Remote" or "On-site" or "Hybrid" in text:
            return text
        else:
            return None


    # TODO Use jobDetail later
    def getJobDescription(self):
        jobDescription = ""

        try:
            jobDescription = self.driver.find_element(By.XPATH, "//div[contains(@class, 'job-details-jobs')]//div").text.replace("·", "|")
        except Exception as e:
            utils.logDebugMessage("in getting jobDescription: ", utils.MessageTypes.WARNING, e)

        return jobDescription   
    

    def isJobBlacklisted(self, company: str, title: str):
        is_blacklisted = self.isCompanyBlacklisted(company)
        if is_blacklisted:
            return True

        is_blacklisted = self.isTitleBlacklisted(title)
        if is_blacklisted:
            return True

        return False
    

    def isCompanyBlacklisted(self, company: str):
        return any(blacklistedCompany.strip().lower() == company.lower() for blacklistedCompany in config.blacklistCompanies)
    

    def isTitleBlacklisted(self, title: str):
        return any(blacklistedTitle.strip().lower() in title.lower() for blacklistedTitle in config.blackListTitles)

    
    def handleMultiplePages(self, jobPage, jobProperties: models.Job, jobCounter: models.JobCounter):
        utils.interact(lambda : self.clickIfExists(By.CSS_SELECTOR, "button[aria-label='Continue to next step']"))

        comPercentage = self.driver.find_element(By.XPATH,'html/body/div[3]/div/div/div[2]/div/div/span').text
        percentage = int(comPercentage[0:comPercentage.index("%")])
        applyPages = math.ceil(100 / percentage) - 2
        try:
            for _ in range(applyPages):
                self.handleApplicationStep(jobProperties)
                utils.interact(lambda : self.clickIfExists(By.CSS_SELECTOR,"button[aria-label='Continue to next step']"))

            self.handleApplicationStep(jobProperties)
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
        repository_wrapper.applied_to_job(jobProperties)
        lineToWrite = self.getLogTextForJobProperties(jobProperties, jobCounter) + " | " + "* 🥳 Just Applied to this job: " + str(jobPage)
        self.displayWriteResults(lineToWrite)

        jobCounter.applied += 1
        return jobCounter


    # TODO Move to logger.py (after splitting utils.py)
    # TODO Move to logger.py (after splitting utils.py)
    def displayWriteResults(self, lineToWrite: str):
        try:
            prYellow(lineToWrite)
            utils.writeResults(lineToWrite)
        except Exception as e:
            prRed("❌ Error in DisplayWriteResults: " + str(e))


    def handleApplicationStep(self, jobProperties: models.Job):
        self.chooseResumeIfPossible(jobProperties)
        # self.handleQuestions(jobProperties)


    def handleQuestions(self, jobProperties: models.Job):
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
            pass

