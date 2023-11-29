websiteUrl = "www.automated-bots.com"
contactUrl = "https://www.automated-bots.com/contact"

linkJobUrl = "https://www.linkedin.com/jobs/search/"
angelCoUrl = "https://angel.co/login"
globalLogicUrl = "https://www.globallogic.com/career-search-page/"

jobsPerPage = 25

fast = 2
medium = 3
slow = 5 

botSpeed = slow

# Webdriver Elements 
jobsPageUrl = "https://www.linkedin.com/jobs"
jobsPageCareerClass = "//div[contains(@class, 'careers')]"
testJobUrl = "https://www.linkedin.com/jobs/search/?currentJobId=3577461385&distance=25&f_AL=true&f_E=2&f_JT=F%2CP%2CC&f_SB2=3&f_WT=1%2C2%2C3&geoId=102221843&keywords=frontend"
totalJobs = "//small"
testPageUrl = testJobUrl +"&start="+ str(2)
offersPerPage = "//li[@data-occludable-job-id]"
easyApplyButton = '//button[contains(@class, "jobs-apply-button")]'
