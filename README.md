# Linkedin Easy Apply Bot 🤖 



![linkedineasyapplygif](https://user-images.githubusercontent.com/34207598/128695728-6efcb457-0f75-42e2-987a-f7a0c239a235.gif)
A python bot to apply all Linkedin Easy Apply jobs based on your preferences.

- Two options are avalible to use this bot, either with entering password or without fully secure no credentials are stored way.
- Export all results and offers as txt and csv (PRO FEATURE) file
- Export unanswered questions to txt file, enter answers there, next time bot will use these values
- PRO FEATURE: Answer unasnwered questions with AI! Let AI answer easy apply jobs' questions.
- Fully customizable job preferences (advanced filters, search filters)
- Can be used for many job search websites such as Linkedin, Glassdoor, AngelCo, Greenhouse, Monster, GLobalLogic and Djinni.

## Installation 🔌

Join our Discord community if you need help https://discord.gg/ab6XPEWN


### Run inside a Docker container (recommended)

- Clone the repo `git clone https://github.com/GabrielGircenko/EasyApplyJobsBot`
- Setup configs
   - Enter your linkedin credentials on line 8 and 9 of config.py file
- Install Docker
- Run `docker build -t easy-apply-bot .`


### Run without Docker

- clone the repo `git clone https://github.com/GabrielGircenko/EasyApplyJobsBot`
- Make sure Python and pip is installed
- Install dependencies with `pip3 install -r requirements.yaml`
- Enter your linkedin credentials on line 8 and 9 of config.py file
- Either create firefox Profile and put its path on line 8 of config.py or enter your linkedin credentials line 11 and 12 of config.py. - this feature is avalible currently only for Linkedin bot pro members)
- Modify config.py according to your demands.
- Run `python3 runner.py` or `python3 runAllConfigs.py` depending on your config setup
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

## Checkout the original repo

Without https://github.com/wodsuz/EasyApplyJobsBot , this repository might have never happened. Checkout his repo for a different Easy Apply experience :) 

