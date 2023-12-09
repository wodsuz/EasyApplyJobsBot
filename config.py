# Enter your Linkedin password and username below. Do not commit this file after entering these credentials.
# Linkedin credentials
email = "YourLinkedin@UserEmail.com"
password = "YourLinkedinPassword"

# Optional! run browser in headless mode, no browser screen will be shown it will work in background.
headless = False
# If you left above credentials fields empty. For Chrome enter profile dir to run the bot to prevent logging in your account each time
# get Chrome profile path by typing following url: chrome://version/
chromeProfilePath = r""

# location you want to search the jobs - ex : ["Poland", "Singapore", "New York City Metropolitan Area", "Monroe County"]
# continent locations:["Europe", "Asia", "Australia", "NorthAmerica", "SouthAmerica", "Africa", "Australia"]
location = ["NorthAmerica"]
# keywords related with your job search
keywords = ["frontend", "react", "typescript","javascript", "vue", "python", "programming", "blockchain"]
#job experience Level - ex:  ["Internship", "Entry level" , "Associate" , "Mid-Senior level" , "Director" , "Executive"]
experienceLevels = [ "Entry level" ]
#job posted date - ex: ["Any Time", "Past Month" , "Past Week" , "Past 24 hours"] - select only one
datePosted = ["Past Week"]
#job type - ex:  ["Full-time", "Part-time" , "Contract" , "Temporary", "Volunteer", "Intership", "Other"]
jobType = ["Full-time", "Part-time" , "Contract"]
#remote  - ex: ["On-site" , "Remote" , "Hybrid"]
remote = ["On-site" , "Remote" , "Hybrid"]
#salary - ex:["$40,000+", "$60,000+", "$80,000+", "$100,000+", "$120,000+", "$140,000+", "$160,000+", "$180,000+", "$200,000+" ] - select only one
salary = [ "$80,000+"]
#sort - ex:["Recent"] or ["Relevent"] - select only one
sort = ["Recent"]
#Blacklist companies you dont want to apply - ex: ["Apple","Google"]
blacklistCompanies = []
#Blaclist keywords in title - ex:["manager", ".Net"]
blackListTitles = []
#Follow companies after sucessfull application True - yes, False - no
followCompanies = False
# One keyword which is unique to one of your CV's. This is used to select the correct CV. ex: ["Android"]
distinctCVKeyword = ["Web"]

 # Testing & Debugging features
displayWarnings = False
