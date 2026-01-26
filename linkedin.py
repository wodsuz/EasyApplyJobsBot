import time,math,random,os
import sys
import utils,constants,config
import pickle, hashlib

sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

try:
    from selenium_stealth import stealth
    STEALTH_AVAILABLE = True
except ImportError:
    STEALTH_AVAILABLE = False

class Linkedin:
    def __init__(self):
            utils.prYellow("🤖 Thanks for using Easy Apply Jobs bot, for more information you can visit our site - www.automated-bots.com")
            utils.prYellow("🌐 Bot will run in Chrome browser and log in Linkedin for you.")
            
            # Fix for WinError 193: Explicitly construct chromedriver path
            try:
                chrome_install = ChromeDriverManager().install()
                folder = os.path.dirname(chrome_install)
                chromedriver_path = os.path.join(folder, "chromedriver.exe")
                service = ChromeService(chromedriver_path)
                self.driver = webdriver.Chrome(service=service, options=utils.chromeBrowserOptions())
            except Exception as e:
                # Fallback to original method if explicit path fails
                if config.displayWarnings:
                    utils.prYellow(f"⚠️ Warning: Could not use explicit chromedriver path, using default: {str(e)[0:50]}")
                self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=utils.chromeBrowserOptions())
            
            # Apply stealth mode if available
            if STEALTH_AVAILABLE:
                try:
                    stealth(self.driver,
                            languages=["en-US", "en"],
                            vendor="Google Inc.",
                            platform="Win32",
                            webgl_vendor="Intel Inc.",
                            renderer="Intel Iris OpenGL Engine",
                            fix_hairline=True)
                except Exception as e:
                    utils.prYellow(f"⚠️ Warning: Could not apply stealth mode: {str(e)}")
            
            self.cookies_path = f"{os.path.join(os.getcwd(),'cookies')}/{self.getHash(config.email)}.pkl"
            self.driver.get('https://www.linkedin.com')
            self.loadCookies()

            if not self.isLoggedIn():
                self.driver.get("https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin")
                utils.prYellow("🔄 Trying to log in Linkedin...")
                try:    
                    self.driver.find_element("id","username").send_keys(config.email)
                    time.sleep(2)
                    self.driver.find_element("id","password").send_keys(config.password)
                    time.sleep(2)
                    self.driver.find_element("xpath",'//button[@type="submit"]').click()
                    time.sleep(30)
                except:
                    utils.prRed("❌ Couldn't log in Linkedin by using Chrome. Please check your Linkedin credentials on config files line 7 and 8.")

                self.saveCookies()
            # start application
            self.linkJobApply()

    def getHash(self, string):
        return hashlib.md5(string.encode('utf-8')).hexdigest()

    def loadCookies(self):
        if os.path.exists(self.cookies_path):
            cookies =  pickle.load(open(self.cookies_path, "rb"))
            self.driver.delete_all_cookies()
            for cookie in cookies:
                self.driver.add_cookie(cookie)

    def saveCookies(self):
        if not os.path.exists(os.path.dirname(self.cookies_path)):
            os.makedirs(os.path.dirname(self.cookies_path))
        pickle.dump(self.driver.get_cookies() , open(self.cookies_path,"wb"))
    
    def isLoggedIn(self):
        self.driver.get('https://www.linkedin.com/feed')
        try:
            self.driver.find_element(By.XPATH,'//*[@id="ember14"]')
            return True
        except:
            pass
        return False 
    
    def generateUrls(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        try: 
            with open('data/urlData.txt', 'w',encoding="utf-8" ) as file:
                linkedinJobLinks = utils.LinkedinUrlGenerate().generateUrlLinks()
                for url in linkedinJobLinks:
                    file.write(url+ "\n")
            utils.prGreen("✅ Apply urls are created successfully, now the bot will visit those urls.")
        except:
            utils.prRed("❌ Couldn't generate urls, make sure you have editted config file line 25-39")

    def linkJobApply(self):
        self.generateUrls()
        countApplied = 0
        countJobs = 0

        urlData = utils.getUrlDataFile()

        for url in urlData:        
            self.driver.get(url)
            time.sleep(random.uniform(1, constants.botSpeed))

            # Handle case where no jobs are found (//small element doesn't exist)
            try:
                totalJobs = self.driver.find_element(By.XPATH,'//small').text 
            except Exception as e:
                urlWords = utils.urlToKeywords(url)
                lineToWrite = "\n Category: " + urlWords[0] + ", Location: " + urlWords[1] + ", No jobs found for this search criteria. Skipping..."
                self.displayWriteResults(lineToWrite)
                if config.displayWarnings:
                    utils.prYellow(f"⚠️ Warning: No jobs found for {urlWords[0]} in {urlWords[1]}. The //small element was not found.")
                continue  # Skip to next URL

            totalPages = utils.jobsToPages(totalJobs)

            urlWords =  utils.urlToKeywords(url)
            lineToWrite = "\n Category: " + urlWords[0] + ", Location: " +urlWords[1] + ", Applying " +str(totalJobs)+ " jobs."
            self.displayWriteResults(lineToWrite)

            for page in range(totalPages):
                currentPageJobs = constants.jobsPerPage * page
                url = url +"&start="+ str(currentPageJobs)
                self.driver.get(url)
                time.sleep(random.uniform(1, constants.botSpeed))

                offersPerPage = self.driver.find_elements(By.XPATH, '//li[@data-occludable-job-id]')
                offerIds = []
                
                # Extract all offer IDs immediately to avoid stale element references
                for offer in offersPerPage:
                    try:
                        offerId = offer.get_attribute("data-occludable-job-id")
                        if offerId:
                            offerIds.append(int(offerId.split(":")[-1]))
                    except Exception as e:
                        if config.displayWarnings:
                            utils.prYellow(f"⚠️ Warning: Could not get offer ID: {str(e)[0:50]}")
                        continue
                
                time.sleep(random.uniform(1, constants.botSpeed))
                
                # Check for "Applied" status by re-finding elements to avoid stale references
                try:
                    offersPerPage = self.driver.find_elements(By.XPATH, '//li[@data-occludable-job-id]')
                    appliedOfferIds = []
                    for offer in offersPerPage:
                        try:
                            if self.element_exists(offer, By.XPATH, ".//*[contains(text(), 'Applied')]"):
                                offerId = offer.get_attribute("data-occludable-job-id")
                                if offerId:
                                    appliedOfferIds.append(int(offerId.split(":")[-1]))
                        except Exception:
                            continue
                    # Remove already applied jobs from the list
                    offerIds = [jobId for jobId in offerIds if jobId not in appliedOfferIds]
                except Exception as e:
                    if config.displayWarnings:
                        utils.prYellow(f"⚠️ Warning: Could not check applied status: {str(e)[0:50]}")

                for jobID in offerIds:
                    offerPage = 'https://www.linkedin.com/jobs/view/' + str(jobID)
                    self.driver.get(offerPage)
                    time.sleep(random.uniform(1, constants.botSpeed))

                    countJobs += 1

                    jobProperties = self.getJobProperties(countJobs)
                    if "blacklisted" in jobProperties: 
                        lineToWrite = jobProperties + " | " + "* 🤬 Blacklisted Job, skipped!: " +str(offerPage)
                        self.displayWriteResults(lineToWrite)
                    
                    else :                    
                        easyApplybutton = self.easyApplyButton()

                        if easyApplybutton is not False:
                            easyApplybutton.click()
                            time.sleep(random.uniform(1, constants.botSpeed))
                            
                            try:
                                self.chooseResume()
                                # Fill phone number before submitting
                                self.fillPhoneNumber()
                                self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']").click()
                                time.sleep(random.uniform(1, constants.botSpeed))

                                lineToWrite = jobProperties + " | " + "* 🥳 Just Applied to this job: "  +str(offerPage)
                                self.displayWriteResults(lineToWrite)
                                countApplied += 1

                            except:
                                try:
                                    # Fill phone number before continuing
                                    self.fillPhoneNumber()
                                    self.driver.find_element(By.CSS_SELECTOR,"button[aria-label='Continue to next step']").click()
                                    time.sleep(random.uniform(1, constants.botSpeed))
                                    self.chooseResume()
                                    comPercentage = self.driver.find_element(By.XPATH,'html/body/div[3]/div/div/div[2]/div/div/span').text
                                    percenNumber = int(comPercentage[0:comPercentage.index("%")])
                                    result = self.applyProcess(percenNumber,offerPage)
                                    lineToWrite = jobProperties + " | " + result
                                    self.displayWriteResults(lineToWrite)
                                
                                except Exception: 
                                    self.chooseResume()
                                    lineToWrite = jobProperties + " | " + "* 🥵 Cannot apply to this Job! " +str(offerPage)
                                    self.displayWriteResults(lineToWrite)
                        else:
                            lineToWrite = jobProperties + " | " + "* 🥳 Already applied! Job: " +str(offerPage)
                            self.displayWriteResults(lineToWrite)


            utils.prYellow("Category: " + urlWords[0] + "," +urlWords[1]+ " applied: " + str(countApplied) +
                  " jobs out of " + str(countJobs) + ".")
        
        utils.donate(self)

    def chooseResume(self):
        try:
            self.driver.find_element(
                By.CLASS_NAME, "jobs-document-upload__title--is-required")
            resumes = self.driver.find_elements(
                By.XPATH, "//div[contains(@class, 'ui-attachment--pdf')]")
            if (len(resumes) == 1 and resumes[0].get_attribute("aria-label") == "Select this resume"):
                resumes[0].click()
            elif (len(resumes) > 1 and resumes[config.preferredCv-1].get_attribute("aria-label") == "Select this resume"):
                resumes[config.preferredCv-1].click()
            elif (type(len(resumes)) != int):
                utils.prRed(
                    "❌ No resume has been selected please add at least one resume to your Linkedin account.")
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
                utils.prYellow("⚠️ Warning in getting jobTitle: " + str(e)[0:50])
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
                utils.prYellow("⚠️ Warning in getting jobDetail: " + str(e)[0:100])
            jobDetail = ""

        try:
            jobWorkStatusSpans = self.driver.find_elements(By.XPATH, "//span[contains(@class,'ui-label ui-label--accent-3 text-body-small')]//span[contains(@aria-hidden,'true')]")
            for span in jobWorkStatusSpans:
                jobLocation = jobLocation + " | " + span.text

        except Exception as e:
            if (config.displayWarnings):
                print(e)
                utils.prYellow("⚠️ Warning in getting jobLocation: " + str(e)[0:100])
            jobLocation = ""

        textToWrite = str(count) + " | " + jobTitle +" | " + jobDetail + jobLocation
        return textToWrite

    def easyApplyButton(self):
        try:
            time.sleep(random.uniform(1, constants.botSpeed))
            button = self.driver.find_element(By.XPATH, "//div[contains(@class,'jobs-apply-button--top-card')]//button[contains(@class, 'jobs-apply-button')]")
            EasyApplyButton = button
        except: 
            EasyApplyButton = False

        return EasyApplyButton

    def fillPhoneNumber(self):
        """Fill phone number fields if they exist and are empty"""
        try:
            # Get phone number from config or additionalQuestions.yaml
            phone_number = ""
            
            # Try to get from config.Phone first
            if hasattr(config, 'Phone') and config.Phone and config.Phone.strip():
                phone_number = config.Phone.strip()
            else:
                # Try to read from additionalQuestions.yaml if available
                try:
                    import yaml
                    if os.path.exists('additionalQuestions.yaml'):
                        with open('additionalQuestions.yaml', 'r', encoding='utf-8') as f:
                            questions = yaml.safe_load(f)
                            if questions and 'inputField' in questions:
                                phone_number = questions['inputField'].get('Phone Number', '').strip()
                except Exception:
                    pass
            
            if not phone_number:
                return  # No phone number configured, skip filling
            
            # Try multiple selectors to find phone number input fields
            phone_selectors = [
                "input[type='tel']",
                "input[name*='phone']",
                "input[id*='phone']",
                "input[aria-label*='phone']",
                "input[placeholder*='phone']",
                "input[data-test-single-line-text-input]",
                "input[class*='phone']"
            ]
            
            phone_filled = False
            
            # Also try XPath selectors for case-insensitive matching
            xpath_selectors = [
                "//input[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'phone')]",
                "//input[contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'phone')]",
                "//input[contains(translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'phone')]",
                "//input[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'phone')]"
            ]
            
            # Try CSS selectors first
            for selector in phone_selectors:
                try:
                    phone_inputs = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for phone_input in phone_inputs:
                        try:
                            # Check if field is visible and empty
                            if phone_input.is_displayed():
                                current_value = phone_input.get_attribute("value") or ""
                                if current_value == "":
                                    phone_input.clear()
                                    phone_input.send_keys(phone_number)
                                    time.sleep(0.5)
                                    phone_filled = True
                                    if config.displayWarnings:
                                        utils.prYellow(f"✅ Filled phone number: {phone_number}")
                                    break
                        except Exception:
                            continue
                    if phone_filled:
                        break
                except Exception:
                    continue
            
            # Try XPath selectors if CSS didn't work
            if not phone_filled:
                for xpath in xpath_selectors:
                    try:
                        phone_inputs = self.driver.find_elements(By.XPATH, xpath)
                        for phone_input in phone_inputs:
                            try:
                                if phone_input.is_displayed():
                                    current_value = phone_input.get_attribute("value") or ""
                                    if current_value == "":
                                        phone_input.clear()
                                        phone_input.send_keys(phone_number)
                                        time.sleep(0.5)
                                        phone_filled = True
                                        if config.displayWarnings:
                                            utils.prYellow(f"✅ Filled phone number: {phone_number}")
                                        break
                            except Exception:
                                continue
                        if phone_filled:
                            break
                    except Exception:
                        continue
                
        except Exception as e:
            if config.displayWarnings:
                utils.prYellow(f"⚠️ Warning: Error in fillPhoneNumber: {str(e)[0:50]}")

    def applyProcess(self, percentage, offerPage):
        applyPages = math.floor(100 / percentage) - 2 
        result = ""
        for pages in range(applyPages):
            # Fill phone number before continuing to next step
            self.fillPhoneNumber()
            self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Continue to next step']").click()
            time.sleep(random.uniform(1, constants.botSpeed))

        # Fill phone number before review
        self.fillPhoneNumber()
        self.driver.find_element( By.CSS_SELECTOR, "button[aria-label='Review your application']").click()
        time.sleep(random.uniform(1, constants.botSpeed))

        if config.followCompanies is False:
            try:
                self.driver.find_element(By.CSS_SELECTOR, "label[for='follow-company-checkbox']").click()
            except:
                pass

        self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']").click()
        time.sleep(random.uniform(1, constants.botSpeed))

        result = "* 🥳 Just Applied to this job: " + str(offerPage)

        return result

    def displayWriteResults(self,lineToWrite: str):
        try:
            print(lineToWrite)
            utils.writeResults(lineToWrite)
        except Exception as e:
            utils.prRed("❌ Error in DisplayWriteResults: " +str(e))

    def element_exists(self, parent, by, selector):
        return len(parent.find_elements(by, selector)) > 0

start = time.time()
Linkedin().linkJobApply()
end = time.time()
utils.prYellow("---Took: " + str(round((time.time() - start)/60)) + " minute(s).")
