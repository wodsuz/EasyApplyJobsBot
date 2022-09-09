import math,constants
from typing import List

def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

def getUrlDataFile():
    urlData = ""
    try:
        file = open('jobPreferances/urlData.txt', 'r')
        urlData = file.readlines()
    except FileNotFoundError:
        text = "FileNotFound:urlData.txt file is not found. Please run ./jobPreferances/createUrl.py first and make sure you have urlData.txt generated."
        colored_text = colored(255, 0, 0, text) 
        print(colored_text)
    return urlData

def jobsToPages(numOfJobs: str) -> int:
  number_of_pages = 1

  if (' ' in numOfJobs):
    spaceIndex = numOfJobs.index(' ')
    totalJobs = (numOfJobs[0:spaceIndex])
    totalJobs_int = int(totalJobs.replace(',', ''))
    number_of_pages = math.ceil(totalJobs_int/constants.jobsPerPage)
    if (number_of_pages > 40 ): number_of_pages = 40

  else:
      number_of_pages = int(numOfJobs)

  return number_of_pages

def urlToKeywords(url: str) -> List[str]:
    keyword = url[url.index("keywords=")+9:url.index("&location") ] 
    location = url[url.index("location=")+9:url.index("&f_E") ] 
    return [keyword,location]

