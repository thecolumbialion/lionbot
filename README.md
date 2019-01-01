# LionBot 

## About LionBot
LionBot is a Facebook Messenger bot that was originally created by The Lion (a campus publication)’s technology team. It's now being maintained by [ADI](https://www.adicu.com) through its ADI Labs program. 

The bot allows people to ask questions and get answers 24/7. Its features range from checking what’s in the dining hall, getting mental health resources, to even checking if the laundry room in one’s dorm has open machines. It can currently be accessed at m.me/thecolumbialion. 
To add a feature, read our contributing [document](github.com/thecolumbialion/lionbot/CONTRIBUTING.MD).


## Structure

```bash
├── CONTRIBUTING.md   # Guide to adding to LionBot
├── README.md         # This file
├── requirements.txt  # Libraries used to build the bot
├── Procfile          # Used when deploying the bot to production
├── app.py            # The main bot code
└── packages/         # All supporting code used by app.py
    ├── academic/     # Features related to academic life
    ├── clubs/        # Features related to clubs
    ├── dining/       # Features related to Columbia/Barnard Dining
    ├── etc/          # Features that don't related to another folder 
    ├── housing/      # Features related to housing
    ├── internal/     # Features related to quick replies and postbacks
    ├── offcampus/    # Features related to off-campus activities
    ├── wellness/     # Features related to health/wellness
```

## Technology Stack
Below are the core libraries used in building the bot.

### PostgreSQL/Psycopg2
Bot data is saved and retrieving data using a database based on PostgreSQL. To interact with the database, the bot uses Psycopg2, a Python library that makes it easy for programmers to interact with Postgres tables.

### SQL
To insert and query for data, the bot relies on SQL.

### Python 3
LionBot is written in Python 3. 

### Flask
Flask is powerful micro web-framework that makes it easy to get a server-based Python app up and running quickly. 

### Dokku
Dokku is a platform as a service that makes it easy to deploy a website. This PaaS is used to deploy bot updates to all users.

### FMBQ/Facebook Messenger API
To handle sending messages, the bot relies on FBMQ, an open-source bot library. More information about the library can be found on its Github [page](github.com/conbus/fbmq).  

### Dialogflow
Dialogflow is a powerful API owned by Google that is core to the bot. This tool uses NLP and ML to process the messages users send the bot and helps provide an estimate of the specific tasks and keywords a user is interested in. 

## Contributors
Thanks to the following people for their initial work in developing LionBot

### Past & Current Product Managers

[Cesar Ramos](), [Shazmin Mahmud](), [Lesley Cordero](https://www.github.com/lesley2958)

### Current Core Developers

[Veronica Woldehanna](), [Shazmin Mahmud]()

### Past Core Developers

[Dagmawi Sraj](), [Monica Arbeit](), [Eleanor Murguia]() 

### Original Developers

Chang Liu, Christine Hsu, Will Essilfie, Eitan Kaplan, Eileen Gao, 
Salim M'Jahad, Carlo Salomon, Vivian Han, Jessy Han, and Malik Drabla

### Designers
Remi Free

### Campus Offices
Thank you to Barnard's Furman Counseling Center for providing resources for the Health/Wellness section of LionBot.

### The Lion
Initial support for the bot is thanks to The Columbia Lion. To learn more about The Lion, visit their [homepage](columbialion.com).


