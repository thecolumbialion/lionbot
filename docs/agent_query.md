# Making an agent query
We mostly just need to have a registered gcloud service account with the proper permissions, copy its key file to the current machine, and then have the proper environment variables. Since I'm assuming that we already have a valid service account that we can use to do this, I am not going through the whole authentication process for that. If you have access to the lionbot agent, then you should be able to look at its service accounts in the google cloud console, and find its key-file.

### 1. Installing gcloud
Refer to [Install gcloud](https://cloud.google.com/sdk/docs/downloads-apt-get) for more
detailed explanations of the following instructions.

1. `export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)"`

2. `echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list`

3. `curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -`

4. `sudo apt-get update && sudo apt-get install google-cloud-sdk`

### 2. Set gcloud config

Refer to [Gcloud config](https://cloud.google.com/sdk/gcloud/reference/config) and
[Gcloud auth](https://cloud.google.com/sdk/gcloud/reference/auth/) for more
detailed explanations of the following instructions.

1. Peek at the current configuration.
`gcloud config list`

The output should be:
```
[core]
disable_usage_reporting = True
Your active configuration is: [default]
```

2. Set the service account as the email address that you want to use.
`gcloud config set account [email-address]`

3. Set the lionbot project as the project that you want to use.
`gcloud config set project [lionbotProject-ID]`

### 3. Set credentials environment variable
Refer to [Enterprise Quickstart](https://cloud.google.com/dialogflow-enterprise/docs/quickstart).

`export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"`

Where PATH is the path to the service account key file (e.g. ~/lionbot/key.json)

Remember that this only applies to the current shell session. You will need to reinitialize this
variable each time unless you put a command in your bashrc.
