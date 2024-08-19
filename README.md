# Linkedin Easy Apply Bot 🤖 

A python bot to apply all Linkedin Easy Apply jobs based on your preferences.

![linkedineasyapplygif](https://user-images.githubusercontent.com/34207598/128695728-6efcb457-0f75-42e2-987a-f7a0c239a235.gif)

## Installation 🔌

NOTE: If you need help setting up or running the bot locally [join our Discord community](https://discord.gg/y9fC2snanK)


### Run inside a Docker container (recommended)

- Clone the repo `git clone https://github.com/GabrielGircenko/EasyApplyJobsBot`
- Setup configs
   - In the project directory, create 'configs' directory
   - Add your configuration
      - Copy the configs.py template into the 'configs' directory
      - Enter your linkedin credentials on the beginning of your_config.py file
      - Add your search preferences. Checkout examples: [CTO in Croatia](https://gist.github.com/GabrielGircenko/fa5cd2200c291096e5fb138677892352) & [Data Scientist in Europe and North America](https://gist.github.com/GabrielGircenko/ec85ae125812b5052da2ed6ea6cdec85)
      - Repeat for various searches
- Install Docker
- Run `docker-compose up --build -d`


### Run without Docker

- clone the repo `git clone https://github.com/GabrielGircenko/EasyApplyJobsBot`
- Make sure Python and pip is installed
- Install dependencies with `pip3 install -r requirements.yaml`
- You have 2 choices
   - SIMPLE: One config.py 
      - Enter your linkedin credentials on the beginning of config.py file
      - Modify config.py according to your preferences. Checkout examples: [CTO in Croatia](https://gist.github.com/GabrielGircenko/fa5cd2200c291096e5fb138677892352) & [Data Scientist in Europe and North America](https://gist.github.com/GabrielGircenko/ec85ae125812b5052da2ed6ea6cdec85)
      - Run `python3 runner.py`
   - MULTIPLE SEARCHES: Multiple configurations
      - Follow the steps described in 'Add your configuration' step of the 'Docker Setup' explained above
      - Run `python3 runAllConfigs.py`
- Check Applied Jobs DATA .txt file is generate under /data folder


### Debug locally in VSCode

- add launch.json to .vscode with the following content:
```
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
      {
         "name": "Debug EasyApply With 1 Config",
         "type": "python",
         "request": "launch",
         "program": "${workspaceFolder}/EasyApplyJobsBot/runner.py",
         "env": {"PYTHONUNBUFFERED": "1"},
         "console": "integratedTerminal"
      }
   ]
}
```
- in config.py
  - leave chromeDriverPath empty or add your local path to it
  - add your chromeProfilePath (instructions to find it are in the config.py)

Then you might have issues with chromedriver not having the right permissions. Here is the solution for MacOS. 
- after starting the debugging at least once, you should have the chromedriver installed
- add path to that chromedriver in config.py
- run something like this (adjust the path to your local environment)
```chmod +x /Users/your_user/.wdm/drivers/chromedriver/mac_version_/version_number/chromedriver-mac-mac_version/chromedriver```
- extra step is to verify the permissions with something like:
```ls -l /Users/your_user/.wdm/drivers/chromedriver/mac_version/version_number/chromedriver-mac-mac_version/chromedriver```


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
- Runs based on your preferences.
- Optional follow or not follow company upon successful application.
- Much more!

### In Detail Feature Table

| Category                                                           |  Available   | In the works
| ------------------------------------------------------------------ | ------------ | ------------
| Supported Browsers                                                 | Chrome       |
| Headless(invisible) Browser                                        | ✅           |
| Login with Credentials                                             | ✅           |
| Filter offers based on job location                                | ✅           |
| Filter offers based on keyword                                     | ✅           |
| Filter offers based on experience level                            | ✅           |
| Filter offers based on date posted                                 | ✅           |
| Filter offers based on salary                                      | ✅           |
| Filter offers based on recent or relevent                          | ✅           |
| Blacklist companies that you don't want to apply                   | ✅           |
| Blacklist offer titles that you don't want to apply                | ✅           |
| Follow or unfollow companies after application                     | ✅           |
| Answer skipped unanswered questions                                | ❌           | https://github.com/GabrielGircenko/EasyApplyJobsBot/issues/9
| Use AI to fill and answer skipped unanswered questions             | ❌           | https://github.com/GabrielGircenko/EasyApplyJobsBot/issues/12
| Don't apply to jobs posted by a Hiring member                      | ❌           | https://github.com/GabrielGircenko/EasyApplyJobsBot/issues/11
| Output file in txt format                                          | ✅           | 
| Output file in csv(excel) format                                   | ❌           | https://github.com/GabrielGircenko/EasyApplyJobsBot/issues/10

If you would like to see a specific feature developed, please open an issue or suggest it in our [Discord community](https://discord.gg/y9fC2snanK)

### Demo 🖥

![banner](https://user-images.githubusercontent.com/34207598/189535377-98ca5bfc-8f4e-4f68-9b3c-59e259d4fe5f.png)
![1](https://user-images.githubusercontent.com/34207598/128695723-2af373a6-3fbb-4dcc-9bba-24af57f17ee9.png)
![2](https://user-images.githubusercontent.com/34207598/128695725-5250cc6d-72e7-4a79-b060-8decfb9be54a.png)
![2022-09-11_18-08](https://user-images.githubusercontent.com/34207598/189535397-2673d603-9489-4104-a066-dd66aca624fd.png)
![2022-09-11_18-09](https://user-images.githubusercontent.com/34207598/189535410-2131a9d0-fd63-419f-a5ea-c663103877d2.png)

## Motivation for this fork

It started out as few fixes to the out-dated functionality (due to LinkedIn's HTML changes). 

Now, the main motivation is to make it very easy to use for tech savvy individuals with basic knowledge of python and Docker. The secondary motivation is to add answering to questions as part of the free functionality compared to the original repo.

Additionally, @GabeGiro is developing a user friendly, closed-source solution. If you want to be one of the first ones to try it out, [join the Discord community](https://discord.gg/y9fC2snanK).

## Contribution

- Fork the repository
- Pick (or create) an issue you want to work on. Assign yourself to the issue (or ask to be assigned to)
- Create a branch
- Link the branch to the issue
- When you are done, open a PR (pull request) - add @GabeGiro as a reviewer
- We might go back and fourth few times and after your PR is approved, you will use "Squash and merge"

## Frequently Asked Questions

<details><summary> How to install and run the bot? </summary>
<br>
To install the bot simply clone the repo, install required packages (these are dependencies making the bot run properly), enter your credentials & edit the config file based on your preferences and run the bot with the command python3 [thePlatformName].py
<br><br>
To run the bot you need Python (general-purpose programming language), Pip (package manager for Python), Selenium (for browser automation) and some dependencies to be installed on your device. For more information and details, you can check the installation steps explained in this README file.
</details>

<details><summary> Instalization is too complicated can you make it easier? </summary>
<br>
Yes, we are trying to improve the process of instalization meanwhile you can purchase and use the step by step instalization tutorials to install the bot properly on your device
</details>

<details><summary> How much does it cost & how can I pay? </summary>
<br>
The free version comes with an open-source license that you can change & modify. For paid versions you can visit original developer's project for more info.
</details>

<details><summary> Would I get banned or my account be blocked? </summary>
<br>
No, since you run the bot on your own device and the traffic is coming from your own address, the risks of getting banned from any of the websites we support is very low. This is because you run the bot on your own device, your traffic will be similar with your own actions and the bot will act humanely meaning it will perform stopping waiting and skipping actions randomly. Meanwhile we dont recommend applying more than 200 jobs per day via job apply bot.
</details>

<details><summary>I have an error while running the bot, how can I fix? </summary>
<br>
When you have an error related to the bot, please check the github project first. Someone else also might post a similar error. If that doesn't work kindly submit your issue.
</details>

<details><summary>What are the terms and rules of using these bots? </summary>
<br>
The free version comes with an open source license. You are free to modify and work in any way you want.
</details>

<details><summary>Linkedin pro bot will apply unanswered / additional questions? </summary>
<br>
Yes and no. It can answer a question based on Linkedin’s default value from previous applications of yours. 
The unanswared questions will stay unanswared but we are working on the solution for that. If you want to be one of the first ones to use this feature, join our [Discord community](https://discord.gg/ab6XPEWN)
</details>

<details><summary>Do you have a bot for x website? </summary>
<br>
No, we only have the [Discord community](https://discord.gg/ab6XPEWN)
</details>

## Checkout the original repo

Without https://github.com/wodsuz/EasyApplyJobsBot , this repository might have never happened. Checkout his repo for a different Easy Apply experience :) 

