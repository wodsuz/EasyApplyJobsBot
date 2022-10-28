# General bot settings

# browser you want the bot to run ex: ["Firefox"], ["Chrome"] choose one only
browser = ["Firefox"]
# Optional! run browser in headless mode, no browser screen will be shown it will work in background.
headless = False
# Optional! for Firefox enter profile dir to run the bot without logging in your account each time
firefoxProfileRootDir = r""
# If you left above field empty enter your Linkedin password and username below
# Linkedin credits
email = ""
password = ""

# These settings are for running Linkedin job apply bot
LinkedinBotProPasswrod = ""
# location you want to search the jobs - ex : ["Poland", "Singapore", "New York City Metropolitan Area", "Monroe County"]
# continent locations:["Europe", "Asia", "Australia", "NorthAmerica", "SouthAmerica", "Africa", "Australia"]
location = ["Poland"]
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

# These settings are for running AngelCO job apply bot
AngelCoBotPassword = ""
# AngelCO credits
AngelCoEmail = ""
AngelCoPassword = ""
# jobTitle ex: ["Frontend Engineer", "Marketing"]
angelCoJobTitle = ["Frontend Engineer"]
# location ex: ["Poland"]
angelCoLocation = ["Poland"]

# These settings are for running GlobalLogic job apply bot
GlobalLogicBotPassword = ""
# AngelCO credits
GlobalLogicEmail = ""
GlobalLogicPassword = ""
# Functions ex: ["Administration", "Business Development", "Business Solutions", "Content Engineering", 	
# Delivery Enablement", Engineering, Finance, IT Infrastructure, Legal, Marketing, People Development,
# Process Management, Product Support, Quality Assurance,Sales, Sales Enablement,Technology, Usability and Design]
GlobalLogicFunctions = ["Engineering"]
# Global logic experience: ["0-1 years", "1-3 years", "3-5 years", "5-10 years", "10-15 years","15+ years"]
GlobalLogicExperience = ["0-1 years", "1-3 years"]
# Global logic location filter: ["Argentina", "Chile", "Crotia", "Germany", "India","Japan", "Poland"
# Romania, Sweden, Switzerland,Ukraine, United States]
GlobalLogicLocation = ["poland"]
# Freelance yes or no
GlobalLogicFreelance = ["no"]
# Remote work yes or no
GlobalLogicRemoteWork = ["yes"]
# Optional! Keyword:["javascript", "react", "angular", ""]
GlobalLogicKeyword = ["react"]
# Global Logic Job apply settinngs
FirstName = "O"
LastName = "D"
Email = "asdsa@gmail.com"
LinkedInProfileURL = "www.google.com"
Phone = "" #OPTIONAL
Location = "" #OPTIONAL
HowDidYouHeard = "" #OPTIONAL
ConsiderMeForFutureOffers = True #true = yes, false = no