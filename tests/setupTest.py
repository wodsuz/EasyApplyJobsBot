import sys

def checkPython():
    try:
        if(sys.version):
            print("✅ Python is succesfully installed!")
        else:
            print("❌ Python is not installed please install Python first: https://www.python.org/downloads/")
    except Exception as e:
        print(e)

def checkPip():
    try:
        import pip
        print("✅ Pip is succesfully installed!")
    except ImportError:
        print("❌ Pip not present. Install pip: https://pip.pypa.io/en/stable/installation/")

def checkSelenium():
    try:
        import selenium
        print("✅ Selenium is succesfully installed!")
    except ImportError:
        print("❌ Selenium not present. Install Selenium: https://pypi.org/project/selenium/")

def checkDotenv():
    try:
        import dotenv
        print("✅ Dotenv is succesfully installed!")
    except ImportError:
        print("❌ Dotenv not present. Install Dotenv: https://pypi.org/project/python-dotenv/")

def checkFirefox():
    try:
        import subprocess
        output = subprocess.check_output(['firefox', '--version'])
        if(output):
            print("✅ Firefox is succesfully installed!")
        else:
            print("❌ Firefox not present. Install firefox: https://www.mozilla.org/en-US/firefox/")

    except ImportError as e:
        print(e)

checkPython()
checkFirefox()
checkPip()
checkSelenium()
checkDotenv()