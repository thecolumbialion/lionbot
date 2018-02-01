# Contributing to LionBot

Thank you for your interest in developing for LionBot, a Facebook Messenger bot made by The Lion's Tech Team.

Before you begin reading through this guide, you should make sure to review Facebook's Messenger API for a better general understanding of how bots work. That link can be found [here](https://developers.facebook.com/docs/messenger-platform/send-messages) (Focus on the Messaging and Webhooks sections -- this should take about 10-15 minutes to read through).

For a quick guide to making bots with Python and Flask, see this intro to bots [tutorial](https://www.twilio.com/blog/2017/12/facebook-messenger-bot-python.html).

Once you have read the docs, continue on for our guide for adding to the bot.

## How to submit a new feature

The best part of LionBot is that it can always be improved with the addition of new features. Adding to the bot has 3 steps (each addressed in its own section):
1. Making a branch and adding your new code
2. Adding sample training sentences to Dialogflow (formerly API.AI)
3. Testing your bot locally along with The Lion Bot testing page.


## How can I add my new feature(s) to the bot? 

### Branching 
LionBot is developed by multiple people. To make this easier, we use individual branches for any new feature being implemented. This way, you can work on your code, make changes, all while leaving master as the defacto, working branch.

To add a new feature to the bot, first make a branch off of the latest version of master. 
Locally, you can run `git pull && git checkout [branch]` to switch to the new branch you will be working on.


### How the bot is structured/where to put your new code
The bot is built around what we call interfaces. What this means is that each new module/feature should have one master function, which we call "interface functions." The interface function must take in a the "result" (see the Dialogflow section for information on this) nested dictionary structure and your method must return a final message to send to the user. 

Interface functions should preferably be structured in this format: `<intent>_msg(result)` -- replacing `<intent>` with the name of the Dialogflow (formerly API.AI) intent name. Interface functions should left in the respective modules, not in app.py. When you make this new python file, be sure to go to the top of app.py and add `from [path][file] import [interface_function]` replacing [file] with the name of the python file you are adding and [interface_function] with the name of the interface method you wrote. Interface functions should be placed in a folder relevant to its purpose that can be found in the packages folder. If a folder does not match your code's purpose, make a new file and create an __init__.py file using `touch __init__.py`. This allows the files in that directory to be accessible to other files saved in other folders. [path] can then be set by using the names of the folders that must be traversed from the home directory to access the file.  Please import only the interface function (using the from keyword), and not the whole module, or any other modules.

Next, you need to add your bot to the dictionary entry we have for all the bot's intents. The key for the dictionary should be the string representing the name of the intent, and the value should be the corresponding interface function. Make sure to follow the conventions of other entries in the dictionary. Once you have completed this step, save your work and proceed to the section about Testing the bot with your new feature.

## DialogFlow 
### What is DialogFlow?
[DialogFlow](dialogflow.com) is a site that helps us make LionBot more personable. The site will take messages users send the bot and return which of the intents we currently have will best answer the user's question. 

### How do I get started with it?
Before you work on Dialogflow for LionBot, follow the getting started [guide](https://dialogflow.com/docs/getting-started/basics) with your own account (you should make an account using your LionMail Google Account). Once you feel comfortable with the site, request access to add intents to LionBot by asking one of The Lion's tech team leads or contacting operations@columbialion.com or labs@adicu.com. Once given access, be sure to review the current intents and entities before adding your own.

**Note:** Tech team leads looking to add people must sign in through the Lion Board's main email account (see Account Info in Board Drive) and add people by going to settings (gear icon) and then Share. New members should be added as "Reviewers" if not adding new features and as "Developer" for all other cases.

### Add your new feature's Dialogflow intent
When adding a new feature, it is important Dialogflow is trained to understand what to expect users might ask it. To handle this, you need to create a new intent (the name you use for this intent will also be used for your interface function in the adding a bot section). In the intent, give at least 5 sample sentences the bot can expect people to ask. Never make example sentences less than 3 words because this can make it hard for Dialogflow to find a pattern in the types of sentences it could receive about the intent. 

Along with the intent, be sure to label the relevant entities that Dialogflow should extract from sentences by highlighting them and labeling their respective entities (if one does not exist for your needs, feel free to make a new one). 

### Testing your intent
Be sure to test and verify that Dialogflow understands your intent well. Using the "Try it now" section of the website, ask it a few questions and make sure that it correctly maps to the correct intent and extracts the correct entities. If this fails, be sure to revisit your intent and update it with more examples.  

### Training the Bot
There's always room to make LionBot better at understanding user questions. When you have the time, be sure to review previously submitted questions to the bot via the Training tab and accept/reject queries based on whether they were correctly matched to their expected entities. 

### Backing up the DialogFlow settings
It always helps to backup the intents and entities used in DialogFlow. Tech team leads should regularly export the zip file containing this information and save it in The Lion Bot's Google Drive. The backup zip can be found in Settings (the gear icon) --> Export and Import 

### Now what?
If you understand DialogFlow and have now added your new intent, proceed to the Testing section where you will add your intent and code to the bot and test locally using Ngrok. 

## Testing

**Note: If you're working on a new feature, be sure that you are working on branch based on the most recent version of master.**
### Running code locally
To run the bot locally, you need to do the following:

### 1) Set up a Python3 Virtual Environment (taken from [here](https://gist.github.com/pandafulmanda/730a9355e088a9970b18275cb9eadef3)):

First type the following in Terminal: 
`python3 -m venv <filepath to your LionBot repo>`

Next, `cd` into the `bin` folder,
` cd bin `

Next, activate the virtual environment: 
`source activate`

To deactivate the environment, simply write: 
`deactivate `

### 2) Install Required Libraries
To install the required libraries, change directories to your LionBot repo and run the following:
`pip3 install -r requirements.txt` in order to install the libraries currently used in the bot. When adding a new feature to the bot that requires a new library, be sure to add library and the version number used following the formatting convention in the file.

### 3) Install Environment Variables
In order to run the bot locally, you need to add the environment variables. To keep these private keys safe, they are stored in the LionBot's Google Drive in a file called "lionbot_localtesting_variables.txt" 
If you do not have access to the file, contact a member of the team or email operations@columbialion.com or labs@adicu.com. Once you have the file, just copy and paste its contents into Terminal to have all the environment variables be added.

The file should look like the following if you are working on a non-Columbia version of the bot:
``` 
export ACCESS_TOKEN=FACEBOOK_ACCESS_TOKEN
export CLIENT_ACCESS_TOKEN=FACEBOOK_CLIENT_ACCESS_TOKEN
export DATABASE_URL=postgres://postgres:TABLEURLHERE
export DEVELOPER_ACCESS_TOKEN=DIAGLOG_FLOW_TOKEN
export SECRET_KEY=FLASK_SECURITY_KEY
export TZ=America/New_York
export VERIFY_TOKEN=FB_VERIFY_TOKEN
export YELP_API_KEY=YELP_API_KEY
export WEATHER_API_KEY=OPEN_WEATHER_MAP_KEY
```

### 4) Confirm your version is working locally
If you have everything setup correctly, make sure your terminal's current working directory is the bot's folder and run 

`python3 app.py`

You should get a message with a similar output to the following:

` * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)`

The bot by default will accept messages at the `/webhook` endpoint. Note, you will see a message that says "Failed validation. Make sure the validation tokens match." As per Facebook Messenger API rules, you need to use a verification code 

### 5) Install Ngrok
To help speed up the development process, we use Ngrok. This nifty tool allows you to launch our Flask app and make it publicly available via a free https:// generated website link. If you do not have Ngrok installed, visit this [gist](https://gist.github.com/wosephjeber/aa174fb851dfe87e644e) for installation instructions.

### 6) Get Bot code running on Ngrok
To get the bot running with it's own Ngrok website link, you need to have two terminal tabs/windows open. In the first tab or window, follow the steps listed in step 4. In the other tab or window, run the following command `ngrok http [port]` where [port] is replaced with the last four numbers in the link generated in the first tab where you ran the Flask app (In the example here, that would be 5000). 

If done correctly, you will see a screen like this in the second tab or window:
![Image of Ngrok in use](https://cdn.pbrd.co/images/GR3ufdA.png)

If the above does not work or you have Homebrew installed, just type `brew cask install ngrok`

Now, we're almost done getting our bot to be tested locally.

### 7) Getting Ready for testing the Bot 

Now we're at the good part -- actually getting to message the bot to see if it works. For our needs, we need two sections -- the Facebook for Developers [portal](https://developers.facebook.com/) and a Facebook [page](https://www.messenger.com/t/lionbottesting) to use for testing. Make sure that developers are added as **admins**. 


### 8) Updating the webhook
Login to Facebook Developers and go to the Test Bot page (in our example, a private page called 'The Lion Bot'). If you have not been added as a developer on the bot, this will fail -- make sure to be added as a developer to access it or make your own. 

To _accept_ the invitation to be a developer, click on the right upperhand corner, as shown below:

[![Screen_Shot_2018-01-26_at_4.47.35_PM.png](https://s18.postimg.org/el3whqed5/Screen_Shot_2018-01-26_at_4.47.35_PM.png)](https://postimg.org/image/62ugde7ud/)

Go to the webhooks section, and click 'Edit Subscriptions' In the box that loads, for the Callback URL enter the link created by Ngrok (make sure this is the link that starts with **https://** ) + "/webhook" (ex. "https://https://5fhan.ngrok.io/webhook), the endpoint at which our bot accepts messages. For the Verify Token field, enter the VERIFY_TOKEN key that you set as an environment variable from lionbot_localtesting_variables.txt If done correctly, the screen should close and accept the changes.

### 9) Test your bot
You can now message the testing [bot.](https:///m.me/lionbottesting) You should be able to get responses from the bot and view any error messages from your terminal tab or window where the Flask app is running.

### 10) Your code works (or doesn't). Now what?
If you have errors in your code, be sure to debug them and keep testing till they are fixed. Once you think your code is ready to be deployed, make a pull request and have your code reviewed. Once the pull request is accepted and merged onto master, it will be scheduled to be deployed to all users. 


## Pushing Code to Master/Deploying to Production
**Note: The only people pushing to master/deploying code to production should be one of the LionBot maintainers.**

LionBot is currently deployed using Dokku, a free Paas that is similar to Heroku, and hosted on Digital Ocean. Before working on pushing code to LionBot's Dokku instance, read through their guide [here.](http://dokku.viewdocs.io/dokku/deployment/application-deployment/).

### Helpful tips
While in the previous section, it was recommended to make one virtualenv for the bot, it would help to make two if you will also be pushing updates to the production version of the site. One could be named lionbot-dev and the other lionbot-prod. The steps in previous pages will be the same except use the different environment variable files found in the Bot's drive account. 

### Dokku Environment Variables
In order for Dokku to work successfully, you need to provide it with the same environment variables.
Using the production file, access the lionbot dokku and for every line in the production environment variables file on the Bot drive, replace the word 'export' with 'dokku config:set [app-name] KEY=VALUE' replacing [app-name] with lionbot or the name you've set for the Dokku instance.

**Note:** For accessing the Postgre Link, look for dokku's DOKKKU_POSTGRES_AQUA_URL and set that as the Database URL.

### Pushing
The bot is run with help from Dokku. To push an update to the bot, do the following:
Change directories into your local version of the bot and add a connection to dokku (only needs to be done once):

`git remote add dokku dokku@[ip-address or domain] [app-name]` (replacing [ip-address or domain] with the IP Address the bot is hosted on or the domain name (see LionBot Drive account) and [app-name] with the name of the Dokku container (in this case it should be lionbot).

After **verifying master is working**, push the changes to Dokku by entering

 `git push dokku master`

Once you type this, the code will be pushed to the Digital Ocean instance the bot is run on and all changes will go live to **all** users. 

## Now what?
Woo! You've gone through the process of adding a new feature to the bot. Continue working on new things to help make LionBot even better.

