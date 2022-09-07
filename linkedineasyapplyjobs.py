import time,os
import jobPreferances.config as config,utils,constants
 
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from dotenv import load_dotenv

class Linkedin:
    def __init__(self):
        load_dotenv()

        firefoxAccountPath = os.getenv('firefoxAccountPath')

        options = Options()
        options.add_argument("-profile")
        options.add_argument(firefoxAccountPath)
        self.driver = webdriver.Firefox(options=options)

        time.sleep(3)

    def Link_job_apply(self):
        countApplied = 0
        countJobs = 0

        location = config.location
        keywords = config.keywords

        file = open('jobPreferances/urlData.txt', 'r')
        lines = file.readlines()

        for url in lines:        
            self.driver.get(url)
            print(url)

            totalJobs = self.driver.find_element("xpath",'//small').text  # get number of results
            totalPages = utils.jobsToPages(totalJobs)

            print(totalPages)

            for page in range(totalPages):
                cons_page_mult = constants.jobsPerPage * page
                url = url + str(cons_page_mult)
                self.driver.get(url)
                time.sleep(10)
                links = self.driver.find_elements_by_xpath(
                    '//div[@data-job-id]')  # needs to be scrolled down
                IDs = []
                for link in links:
                    temp = link.get_attribute("data-job-id")
                    jobID = temp.split(":")[-1]
                    IDs.append(int(jobID))
                IDs = set(IDs)
                jobIDs = [x for x in IDs]
                for jobID in jobIDs:
                    job_page = 'https://www.linkedin.com/jobs/view/' + \
                        str(jobID)
                    self.driver.get(job_page)
                    countJobs += 1
                    time.sleep(5)
                    try:
                        button = self.driver.find_elements_by_xpath(
                            '//button[contains(@class, "jobs-apply")]/span[1]')
                        # if button[0].text in "Easy Apply" :
                        EasyApplyButton = button[0]
                    except:
                        EasyApplyButton = False
                    button = EasyApplyButton
                    if button is not False:
                        string_easy = "* has Easy Apply Button"
                        button.click()
                        time.sleep(2)
                        try:
                            self.driver.find_element_by_css_selector(
                                "button[aria-label='Submit application']").click()
                            time.sleep(3)
                            countApplied += 1
                            print("* Just Applied to this job!")
                        except:
                            try:
                                button = self.driver.find_element_by_css_selector(
                                    "button[aria-label='Continue to next step']").click()
                                time.sleep(3)
                                percen = self.driver.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/div/div/span").text
                                percen_numer = int(percen[0:percen.index("%")])
                                if int(percen_numer) < 25:
                                    print(
                                        "*More than 5 pages,wont apply to this job! Link: " +job_page)
                                elif int(percen_numer) < 30:
                                    try:
                                        self.driver.find_element_by_css_selector(
                                        "button[aria-label='Continue to next step']").click()
                                        time.sleep(3)
                                        self.driver.find_element_by_css_selector(
                                        "button[aria-label='Continue to next step']").click()
                                        time.sleep(3)
                                        self.driver.find_element_by_css_selector(
                                        "button[aria-label='Review your application']").click()
                                        time.sleep(3)
                                        self.driver.find_element_by_css_selector(
                                        "button[aria-label='Submit application']").click()
                                        countApplied += 1
                                        print("* Just Applied to this job!")
                                    except:
                                        print(
                                            "*4 Pages,wont apply to this job! Extra info needed. Link: " +job_page)
                                elif int(percen_numer) < 40:
                                    try: 
                                        self.driver.find_element_by_css_selector(
                                        "button[aria-label='Continue to next step']").click()
                                        time.sleep(3)
                                        self.driver.find_element_by_css_selector(
                                        "button[aria-label='Review your application']").click()
                                        time.sleep(3)
                                        self.driver.find_element_by_css_selector(
                                        "button[aria-label='Submit application']").click()
                                        countApplied += 1
                                        print("* Just Applied to this job!")
                                    except:
                                        print(
                                            "*3 Pages,wont apply to this job! Extra info needed. Link: " +job_page)
                                elif int(percen_numer) < 60:
                                    try:
                                        self.driver.find_element_by_css_selector(
                                        "button[aria-label='Review your application']").click()
                                        time.sleep(3)
                                        self.driver.find_element_by_css_selector(
                                        "button[aria-label='Submit application']").click()
                                        countApplied += 1
                                        print("* Just Applied to this job!")
                                    except:
                                        print(
                                            "* 2 Pages,wont apply to this job! Unknown.  Link: " +job_page)
                            except:
                                print("* Cannot apply to this job!!")
                    else:
                        print("* Already applied!")
                    time.sleep(2)
            print("Category: " + keywords + " ,applied: " + str(countApplied) +
                  " jobs out of " + str(countJobs) + ".")


start_time = time.time()
ed = Linkedin()
ed.Link_job_apply()
end = time.time()
print("---Took: " + str(round((time.time() - start_time)/60)) + " minute(s).")
