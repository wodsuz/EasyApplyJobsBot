import math,constants
from typing import List
import time

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

def writeResults(text: str):
    timeStr = time.strftime("%Y%m%d")
    fileName = "Applied Jobs DATA - " +timeStr + ".txt"
    try:
        with open("results/" +fileName) as file:
            lines = []
            for line in file:
                lines.append(line)
                
        with open("results/" +fileName, 'w') as f:
            for line in lines: 
                f.write(line)
            f.write(text+ "\n")
    except:
        with open("results/" +fileName, 'w') as f:
            f.write(text+ "\n")

