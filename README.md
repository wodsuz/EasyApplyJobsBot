# Easy Apply Jobs Bot 🤖

![linkedineasyapplygif](https://user-images.githubusercontent.com/34207598/128695728-6efcb457-0f75-42e2-987a-f7a0c239a235.gif)
A python bot to apply all Linkedin Easy Apply jobs based on your preferences.

- Two options are avalible to use this bot, either with entering password or without fully secure no credentials are stored way.
- Export all results and offers as txt file
- Export unanswered questions to txt file, enter answers there next time bot will use these values
- Answer unasnwered question with AI! Let AI answer easy apply jobs' questions.
- Fully customizable job preferences (advanced filters, search filters)
- Can be used for many job search websites such as Linkedin, Glassdoor, AngelCo, Greenhouse, Monster, GLobalLogic and Djinni.

## Installation 🔌

- clone the repo `git clone https://github.com/petrenko0806/EasyApplyJobsBot`
- Make sure Python and pip is installed
- Install dependencies with `pip3 install -r requirements.yaml`
- Enter your linkedin credentials on line 8 and 9 of config.py file
- Either create firefox Profile and put its path on line 8 of config.py or enter your linkedin credentials line 11 and 12 of config.py. - this feature is avalible currently only for Linkedin bot pro members)
- Modify config.py according to your demands.
- Run `python3 linkedin.py`
- Check Applied Jobs DATA .txt file is generate under /data folder

## Features 💡

- Ability to filter jobs, by easy apply, by location (Worldwide, Europe, Poland, etc.), by keyword (python, react, node), by experience, position, job type and date posted.
- Apply based on your salary preferance (works best for job offers from States)
- Automatically apply single page jobs in which you need to send your up-to-date CV and contact.
- Automatically apply more than one page long offers with the requirements saved in LinkedIn like experience, legal rights, resume etc.
- Output the results in a data txt file where you can later work on.
- Print the links for the jobs that the bot couldn’t apply for because of extra requirements. (User can manually apply them to optimize the bot)
- Put time breaks in between functions to prevent threshold.
- Automatically apply for jobs.
- Automatically run in the background.
- Compatible with Firefox and Chrome.
- Runs based on your preferences.
- Optional follow or not follow company upon successful application.
- Much more!

## Tests 🔦

There is a specific test folder for you to test the dependencies, the bot and if everything is set up correctly. To do that I recommend,
running below codes,

1. Go to the tests folder run `python3 setupTests.py` this will output if Python,pip,selenium,dotenv and Firefox are installed correctly on your system.
2. Run `python3 seleniumTest.py` this will output if the Selenium and gecko driver is able to retrieve data from a website. If it returns an error make sure you have correctly installed selenium and gecko driver
3. Run `python3 linkedinTest.py` this will try to log in automatically to your Linkedin account based on the path you defined in the .env file. If its giving an error make sure the path exists and you created firefox profile, logged in manually to your Linkedin account once.
   Here is the result you should get after running test files,
   ![test1](https://user-images.githubusercontent.com/34207598/189535308-c2c546de-caec-4460-823d-dd5ca208c480.png)

## How to Set up (long old way) 🛠

This tutorial briefly explains how to set up LinkedIn Easy Apply jobs bot. With few modifications you can make your own bot or try my other bots for other platforms.

1. Install Firefox or Chrome. I was using Firefox for this so I will continue the usage of it on Firefox browser. Process would be similar on Chrome too.
2. Install Python.
3. Download Geckodriver put it in Python’s installation folder.
4. Install pip, python get-pip.py
5. Install selenium pip install selenium
6. Clone the code
7. Create a profile on Firefox, about:profiles
8. Launch new profile, go Linkedin.com and log in your account
9. Copy the root folder of your new profile, to do that type about:profiles on your Firefox search bar, copy the root folder C:\---\your-profile-name.
10. Paste the root folder on .env file
11. Modify/adapt the code and run
12. After each run check the jobs that the bot didn’t apply automatically, apply them manually by saving your preferences
13. Next time the bot will apply for more jobs based on your saved preferences on Linkedin.
14. Feel free to contact me for any update/request or question.

## Demo 🖥

![banner](https://user-images.githubusercontent.com/34207598/189535377-98ca5bfc-8f4e-4f68-9b3c-59e259d4fe5f.png)
![1](https://user-images.githubusercontent.com/34207598/128695723-2af373a6-3fbb-4dcc-9bba-24af57f17ee9.png)
![2](https://user-images.githubusercontent.com/34207598/128695725-5250cc6d-72e7-4a79-b060-8decfb9be54a.png)
![2022-09-11_18-08](https://user-images.githubusercontent.com/34207598/189535397-2673d603-9489-4104-a066-dd66aca624fd.png)
![2022-09-11_18-09](https://user-images.githubusercontent.com/34207598/189535410-2131a9d0-fd63-419f-a5ea-c663103877d2.png)

## Future Implementations

- Headless browser experience (run the bot without launching the browser)
- Blacklist offers in Linkedin
- Output not completed fields in Linkedin
- Add support to other major job seeking websites (Glassdoor, AngelCo, Greenhouse, Monster, GLobalLogic, djinni)
- AngelCo - https://angel.co/l/2xRADV
- https://cryptocurrencyjobs.co/
