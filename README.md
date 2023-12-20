# Automated Bots - Easy Apply Jobs Bot 🤖 - https://www.automated-bots.com/

![linkedineasyapplygif](https://user-images.githubusercontent.com/34207598/128695728-6efcb457-0f75-42e2-987a-f7a0c239a235.gif)
A python bot to apply all Linkedin Easy Apply jobs based on your preferences.

## Please be aware that there are forked/similar looking versions of this bot using scam, phishing donation links. While purchasing make sure you are on www.automated-bots.com page or just like below page have check our logo on each crypto payment site,

![Copyright image](https://github.com/wodsuz/EasyApplyJobsBot/assets/34207598/ea8ba3e2-1bed-4d80-ae20-9e96d1f5c09f)

## This is the free version of the bot, you can fork & modifty it by crediting us and without changing the donation links. To use the pro version you can visit our site www.automated-bots.com

# Demo

Easy Apply Jobs Bot Pro version running on Linux Firefox Browser

https://github.com/wodsuz/EasyApplyJobsBot/assets/34207598/0de30c7e-a8ab-4fc8-8609-f401e13accca

Easy Apply Jobs Bot Pro version running on Linux Chrome Browser

https://github.com/wodsuz/EasyApplyJobsBot/assets/34207598/6fa36b64-742f-4fb2-8228-c15d04560f4f

- Two options are avalible to use this bot, either with entering password or without fully secure no credentials are stored way.
- Export all results and offers as txt and csv (PRO FEATURE) file
- Export unanswered questions to txt file, enter answers there, next time bot will use these values
- PRO FEATURE: Answer unasnwered questions with AI! Let AI answer easy apply jobs' questions.
- Fully customizable job preferences (advanced filters, search filters)
- Can be used for many job search websites such as Linkedin, Glassdoor, AngelCo, Greenhouse, Monster, GLobalLogic and Djinni.

To modify, use, get documentation or for you business enquiries kindly contact us via: <br>
[**help@automated-bots.com**](mailto:help@automated-bots.com?subject=Contact%20Via%20[GitHub]%20EasyApplyJobsBot)

[**Or directly contact us from our website**](https://www.automated-bots.com/contact)<br>

## Donation and Support 🥳

With your support we build, update and work on this project. You can also purchase additional packages, tutorials and materials explaining how this bot is working. <br>

There are several features and simplifications we'd like to add to this project. For that we need your support to cover costs. Your support is keeping this project alive.

[**Donate & support!**](https://commerce.coinbase.com/checkout/923b8005-792f-4874-9a14-2992d0b30685)

## Purchase additional materials and guides 😍

You can currently, purchase full in depth detailed tutorial explaining how this bot is working, one hour booking session where i step by step build and run the bot on your machine or 5 videos
showing how this can be used. To buy, support this project and help me add more features. <br>

- [**Purchase online call tech support to install the bot for Windows**](https://commerce.coinbase.com/checkout/bfc45949-3719-4cac-8fc9-f9111b47a009)
- [**Purchase online call tech support to install the bot for Linux**](https://commerce.coinbase.com/checkout/c27538b8-ddee-4c68-a0eb-da43e6014043)
- [**Purchase online call tech support to install the bot for Mac OS**](https://commerce.coinbase.com/checkout/52472ffa-1653-4f56-b92b-60983e627e7c)
- [**Purchase documentation of this bot for Windows**](https://commerce.coinbase.com/checkout/03546cb2-8691-4837-91ec-a86cae1cb25d)
- [**Purchase documentation of this bot for Linux**](https://commerce.coinbase.com/checkout/b6ec4e61-cded-4845-a9b8-f87079482e7f)
- [**Purchase documentation of this bot for Mac OS**](https://commerce.coinbase.com/checkout/effe4a67-895f-4862-ad77-954217d752e6)

## Installation 🔌

- clone the repo `git clone https://github.com/wodsuz/EasyApplyJobsBot`
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

## Supported Platforms

| Browser | Mac | Windows | Linux-Ubuntu | Note                          |
| ------- | --- | ------- | ------------ | ----------------------------- |
| Chrome  | ✅  | ✅      | ✅           |
| Firefox | ✅  | ✅      | ✅           | Only avalible for Pro version |

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

## Free vs Pro version

| Category                                                           | Free Version | Pro Version        |
| ------------------------------------------------------------------ | ------------ | ------------------ |
| Supported Browsers                                                 | Chrome       | Firefox and Chrome |
| Headless(invisible) Browser                                        | ❌           | ✅                 |
| Login with Credentials                                             | ✅           | ✅                 |
| Auto login based on Firefox Profile                                | ❌           | ✅                 |
| Filter offers based on job location                                | ✅           | ✅                 |
| Filter offers based on keyword                                     | ✅           | ✅                 |
| Filter offers based on experience level                            | ✅           | ✅                 |
| Filter offers based on date posted                                 | ✅           | ✅                 |
| Filter offers based on salary                                      | ✅           | ✅                 |
| Filter offers based on recent or relevent                          | ✅           | ✅                 |
| Blacklist companies that you don't want to apply                   | ✅           | ✅                 |
| Blacklist offer titles that you don't want to apply                | ✅           | ✅                 |
| Follow or unfollow companies after application                     | ✅           | ✅                 |
| Output skipped questions in txt file for late application          | ❌           | ✅                 |
| Use AI to fill and answer skipped unanswered questions             | ❌           | ✅                 |
| Only Apply these companies feature                                 | ❌           | ✅                 |
| Only Apply titles having these keywords feature                    | ❌           | ✅                 |
| Don't apply the job posted by the Hiring member                    | ❌           | ✅                 |
| Only apply the job sposted by the Hiring member                    | ❌           | ✅                 |
| Only apply jobs having less than x amount applications             | ❌           | ✅                 |
| Only apply jobs having these keywords in the job description       | ❌           | ✅                 |
| Dont't apply the jobs having these keywords in the job description | ❌           | ✅                 |
| Apply companies having equal or more than employes                 | ❌           | ✅                 |
| Only apply the ones linkedin is saying "you may be a goodfit"      | ❌           | ✅                 |
| Only apply the ones you have skilled badge                         | ❌           | ✅                 |
| Save the jobs by pressing SAVE button before apply                 | ❌           | ✅                 |
| Sent a message to the hiring manager once you apply for the role   | ❌           | ✅                 |
| List and output non Easy Apply jobs links                          | ❌           | ✅                 |
| Check yes or no to all checkbox questions                          | ❌           | ✅                 |
| Output file in txt format                                          | ✅           | ✅                 |
| Output file in csv(excel) format                                   | ❌           | ✅                 |

## Documentation

[**Automated Bots - Easy Apply Jobs Config file Settings Document**](https://docs.google.com/document/d/1iqzsfily05ce1amr1ob01zemezzn3va2pbk3momn15g/edit?usp=sharing)

## Frequently Asked Questions

<details><summary> How to install and run the bot? </summary>
<br>
To install the bot simply clone the repo, install required packages (these are dependencies making the bot run properly), enter your credentials & edit the config file based on your preferences and run the bot with the command python3 [thePlatformName].py
<br><br>
To run the bot you need Python (general-purpose programming language), Pip (package manager for Python), Selenium (for browser automation) and some dependencies to be installed on your device. For more information and details, you can check the installation of each project on their specific site shown below.
</details>

<details><summary> Instalization is too complicated can you make it easier? </summary>
<br>
Yes, we are trying to improve the process of instalization meanwhile you can purchase and use the step by step instalization tutorials to install the bot properly on your device
</details>

<details><summary> What are the features of these bots? </summary>
<br>
Currently automated bots hold 3 different subgroups under one umbrella. One for applying for jobs automatically, one for listing businesses automatically and one for swiping & messaging automatically in dating apps. You can check the features of each bot on the homepage and their own GitHub repository that I share and update regularly. 
</details>

<details><summary> How much does it cost & how can I pay? </summary>
<br>
Each bot has a free and paid version. The free version comes with an open-source license that you can change & modify. For paid ones, you need to purchase coins and those coins will be deducted whenever the bot successfully acts (applying for jobs successfully, listing companies successfully or swiping & sending messages successfully). You can check our shop for the prices of each product. 
</details>

<details><summary> Would i get banned or my account be blocked? </summary>
<br>
No, since you run the bot on your own device and the traffic is coming from your own address, the risks of getting banned from any of the websites we support is very low. This is because you run the bot on your own device, your traffic will be similar with your own actions and the bot will act humanely meaning it will perform stopping waiting and skipping actions randomly.Meanwhile we dont recommend applying more than 200 jobs per day via job apply bot.
</details>

<details><summary>I have an error while running the bot, how can i fix? </summary>
<br>
When you have an error related to any of the bots. Please check the github project first. Someone else also might post a similar error. Then if its free version try Google the error, if that doesn't work kindly contact with us with our contact page.
</details>

<details><summary>What are the terms and rules of using these bots? </summary>
<br>
The free version comes with an open source license. You are free to modify and work in any way you want. Paid version comes with limited license meaning that you accept and approve that you will be using the bot for you only and you won't modify/sell/commercialize or steal in any way 
</details>

<details><summary>Linkedin pro bot will apply unanswered / additional questions? </summary>
<br>
Yes. Linkedin pro has several features for unanswered or additional questions. Firstly, it can answer a question based on Linkedin’s default value from previous applications of yours. Secondly, it can apply from a questions file - you need to add custom questions and answers in order for the bot to apply, thirdly AI can answer the questions for you. 
</details>

<details><summary>Do you have a bot for x website? </summary>
<br>
We currently support the sites we sell in our shop. Please check our shop in order to see if we support or not. We constantly add and update the bot, in the future we will have social media accounts to provide you better and faster updates. 
</details>

## Future Implementations

- Add full support to other major job seeking websites (Glassdoor, AngelCo https://angel.co/l/2xRADV, Greenhouse, https://cryptocurrencyjobs.co/, Monster, GLobalLogic, djinni)

## Special Thanks

Special thanks to all the contributors who are constantly helping and keeping this repository active. Your contributions, whether they're bug reports, feature suggestions, or code improvements, are greatly appreciated. We couldn't do this without you!

- Thanks a lot [@GabrielGircenko](https://github.com/GabrielGircenko) for putting his time and huge experince on this project. Please make sure to check his repo https://github.com/GabrielGircenko/EasyApplyJobsBot
