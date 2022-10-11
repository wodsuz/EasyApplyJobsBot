import config

linkJobUrl = "https://www.linkedin.com/jobs/search/"

def generateUrlLinks():
    path = []
    for location in config.location:
        for keyword in config.keywords:
                url = linkJobUrl + "?f_AL=true&keywords=" +keyword+jobType()+remote()+checkJobLocation(location)+jobExp()+datePosted() 
                path.append(url)
    return path

def checkJobLocation(job):
    jobLoc = "&location=" +job
    match job.casefold():
        case "asia":
            jobLoc += "&geoId=102393603"
        case "europe":
            jobLoc += "&geoId=100506914"
        case "northamerica":
            jobLoc += "&geoId=102221843&"
        case "southamerica":
            jobLoc +=  "&geoId=104514572"
        case "australia":
            jobLoc +=  "&geoId=101452733"
        case "africa":
            jobLoc += "&geoId=103537801"

    return jobLoc

def jobExp():
    jobtExpArray = config.experienceLevels
    firstJobExp = jobtExpArray[0]
    jobExp = ""
    match firstJobExp:
        case "Internship":
            jobExp = "&f_E=1"
        case "Entry level":
            jobExp = "&f_E=2"
        case "Associate":
            jobExp = "&f_E=3"
        case "Mid-Senior level":
            jobExp = "&f_E=4"
        case "Director":
            jobExp = "&f_E=5"
        case "Executive":
            jobExp = "&f_E=6"
    for index in range (1,len(jobtExpArray)):
        match jobtExpArray[index]:
            case "Internship":
                jobExp += "%2C1"
            case "Entry level":
                jobExp +="%2C2"
            case "Associate":
                jobExp +="%2C3"
            case "Mid-Senior level":
                jobExp += "%2C4"
            case "Director":
                jobExp += "%2C5"
            case "Executive":
                jobExp  +="%2C6"

    return jobExp

def datePosted():
    datePosted = ""
    match config.datePosted[0]:
        case "Any Time":
            datePosted = ""
        case "Past Month":
            datePosted = "&f_TPR=r2592000&"
        case "Past Week":
            datePosted = "&f_TPR=r604800&"
        case "Past 24 hours":
            datePosted = "&f_TPR=r86400&"
    return datePosted

def jobType():
    jobTypeArray = config.jobType
    firstjobType = jobTypeArray[0]
    jobType = ""
    match firstjobType:
        case "Full-time":
            jobType = "&f_JT=F"
        case "Part-time":
            jobType = "&f_JT=P"
        case "Contract":
            jobType = "&f_JT=C"
        case "Temporary":
            jobType = "&f_JT=T"
        case "Volunteer":
            jobType = "&f_JT=V"
        case "Intership":
            jobType = "&f_JT=I"
        case "Other":
            jobType = "&f_JT=O"
    for index in range (1,len(jobTypeArray)):
        match jobTypeArray[index]:
            case "Full-time":
                jobType += "%2CF"
            case "Part-time":
                jobType +="%2CP"
            case "Contract":
                jobType +="%2CC"
            case "Temporary":
                jobType += "%2CT"
            case "Volunteer":
                jobType += "%2CV"
            case "Intership":
                jobType  +="%2CI"
            case "Other":
                jobType  +="%2CO"
    jobType += "&"
    return jobType

def remote():
    remoteArray = config.remote
    firstJobRemote = remoteArray[0]
    jobRemote = ""
    match firstJobRemote:
        case "On-site":
            jobRemote = "f_WT=1"
        case "Remote":
            jobRemote = "f_WT=2"
        case "Hybrid":
            jobRemote = "f_WT=3"
    for index in range (1,len(remoteArray)):
        match remoteArray[index]:
            case "On-site":
                jobRemote += "%2C1"
            case "Remote":
                jobRemote += "%2C2"
            case "Hybrid":
                jobRemote += "%2C3"

    return jobRemote

with open('urlData.txt', 'w') as f:
    linkedinJobLinks = generateUrlLinks()
    for url in linkedinJobLinks:
        f.write(url+ "\n")

