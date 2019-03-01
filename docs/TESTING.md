# Testing LionBot

  1. Make sure that you have done all of the setup requirements and have gotten everything working properly. Check out the [Contributing](https://github.com/thecolumbialion/lionbot/blob/master/CONTRIBUTING.md) page if you haven't yet. The most important part is that you have downloaded all of the python dependencies (Flask, Dialogflow...) and ngrok.

  2. Next, just because we want everyone to be able to test changes that they have made to the bot without messing with others' work, you'll want your own personal test Dialogflow agent. There are a few things we have to do for this.

  #### Get a copy of our LionBot Agent
  Go to the [Dialogflow](dialogflow.com) website. Log in. You should be added to LionBot at this point. Go to the LionBot agent.
  Your browser should look something like the following:
  ![Image of LionBot console](./imgs/LionBotConsole.png?raw=true)
  Now, click on go to the settings page by clicking on the wheel next to the bot:
  ![Lionbot Settings](./imgs/LionBotConsoleSettingsWheel.jpg?raw=true)
  Now, you should be in the settings page and there should an **Export and Import** field, click on it:
  ![Lionbot Export Import](./imgs/ExportImportTag.jpg?raw=true)
  Then, click on **Export as Zip**. This should download a zip file of the current LionBot containing the Intents and Entities of the agent.
  ![LionBot Export Button](./imgs/ExportButton.jpg?raw=true)

  #### Create a new Dialogflow agent/project
  Click on the create new agent button on the drop-down menu for your Dialogflow projects.
  ![Create New Agent](./imgs/CreateNewAgent.jpg?raw=true)
  You can use the default settings, make sure that you name your agent. The creation should take a few seconds.
  ![Create New Agent Settings](./imgs/AgentCreationSettings.png?raw=true)

  #### Import the LionBot agent.
  You want to have your new Dialogflow agent become a copy of Lionbot. So, you'll want to use the **Restore From Zip** option make your newly created agent a copy of LionBot.
  ![Restore LionBot](./imgs/RestoreLionbot.jpg?raw=true)

  3. We need to update some of the environment variables that we set before running the test app. We need to replace the existing `CLIENT_ACCESS_TOKEN`and `DEVELOPER_ACCESS_TOKEN` with the ones that you find in your settings page. You also probably want to set the version to v1.
  ![Change Tokens](./imgs/ChangeTokens.jpg?raw=true)

  4. Now we want to connect our webhook to the agent so that we can test any changes we make to the webhook. Remember from the [Contributing](https://github.com/thecolumbialion/lionbot/blob/master/CONTRIBUTING.md) page how we deploy the webhook locally.
  In one bash instance, _with our virtual environment activated_, run `$ python testapp.py`, then in another bash instance run `$ ngrok http 5000`. In the ngrok window, the localhost instance will be forwarded to an actual url (e.g. `http://das87968.ngrok.io`) that you can copy and paste.

  Now, you should use this, to deploy a webhook for your test agent. Go to the fulfillment's page, enable webhook, and copy the url you got from ngrok with `/webhook` appended to the end. And remember to scroll down and click **SAVE**.
  ![Enable Webook](./imgs/EnableWebhook.png?raw=true)

  Now, you should be good to go, you can enter your test queries in the test window.
  ![Test the Bot](./imgs/TestNOW.jpg?raw=true)
