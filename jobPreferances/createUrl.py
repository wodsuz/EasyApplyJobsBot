import config

linkedinPath = "https://www.linkedin.com/jobs/search/"

def keywordLocationJoin():
    path = []
    for location in config.location:
        for keyword in config.keywords:
            for expLevel in config.experienceLevels:
                url = linkedinPath + "?f_AL=true&keywords=" +keyword+ "&location=" +location
                expUrl = ""
                match expLevel:
                    case "Internship":
                        expUrl = "&f_E=1"
                    case "Entry level":
                        expUrl = "&f_E=2"
                    case "Associate":
                        expUrl = "&f_E=3"
                    case "Mid-Senior level":
                        expUrl = "&f_E=4"
                    case "Director":
                        expUrl = "&f_E=4"
                    case "Executive":
                        expUrl = "&f_E=4" 
                date = datePosted()
                url = url + expUrl + date
                path.append(url)
    return path

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

with open('urlData.txt', 'w') as f:
    linkedinJobLinks = keywordLocationJoin()
    for url in linkedinJobLinks:
        f.write(url+ "\n")

