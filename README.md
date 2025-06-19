# Description
* AI-powered Datagenie is an ultimate data virtual assistant for internal Zoom organizations enabling data-driven decision making. 
* The solution comprises of the chatbot app and the API server. 
* The chatbot app will leverage the Zoom Chatbot App based on Zoom Team Chat. Setting up the chatbot app is a fairly straight forward process which is documented here: https://developers.zoom.us/docs/team-chat-apps/create/
* This repository will only focus on the API server backend based on FastApi.

# Installation
1. Data Genie project requires Python 3.10. Install Python 3.10 if you do not have one. Instructions for MacOS - https://zoomvideo.atlassian.net/wiki/spaces/DSB/pages/2683316352/Install+and+Manage+Python+Environments+on+MacOS
2. Use poetry to set up the virtual environment and link the environment to your IDE's Python interpreter
4. Activate the virtual environment - https://python-poetry.org/docs/managing-environments/
    ```shell
    poetry shell
   ```
5. Install Data Genie
    ```shell
    poetry install
   ```

# Local testing
1. While the environment variables required for running Data Genie are pushed to the DEV and GO/PROD environments directly thru' AWS Secret Manager, the local testing requires you to have a '.env' file with the required environment variables. 
   Create a .env file under the project root with the following variables:
   * database_url='snowflake://data_genie_go:{password}(at)zoom-zoomus/{warehouse}'
   * chatbot_message_url='https://zoomdev.us/v2/im/chat/messages'
   * chatbot_token_url='https://zoomdev.us/oauth/token?grant_type=client_credentials'
   * chatbot_secret=base64encode({client_id}:{client_secret})
   * authorization='dummy'
2. Run Data Genie
    ```shell
    poetry run uvicorn zdt_datagenie.main:app --host 0.0.0.0 --port 8000 --reload
   ```
3. Use CuRL or Postman to interact with the Fast API server. The Data Genie Postman collection is available here: https://drive.google.com/file/d/1KHz_qBR8qh9Ru_ytP_G73Y2toZd8-wIM/view?usp=sharing

# Branching Strategy
1. Create a feature branch from `release-prego`. Recommended feature branch name: feature/{feature_name}
2. After the local testing, create an MR to merge feature branch into `release-prego`
3. After the testing on dev environment, create an MR to merge `release-prego` to `release-go`
4. For hotfixes, it is ok to merge feature branch to `release-go` after proper testing on `pre_go` environment

In short: `feature -> release-prego -> release-go` will be the normal flow

# Build (CI)
Jenkins link for the Data Genie build job - <>
Use the following steps to build the Data Genie app:
  * Click on Build with Parameters
  * VERSION: 0.0 for builds on the `release-prego` branch and 0.{1, 2, 3,.....} for builds on the `release-go` branch
  * BRANCH: `release-prego` or `release-go`

# Deployment (CD)
Jenkins link for the Data Genie deployment job - <>
* To deploy the Data Genie app on the `pre_go` environment, use the pre_go job. Typically all builds on the `release-prego` branch should use this job.
  * To deploy the Data Genie app on the `go` environment, use the go job. Typically all builds on the `release-go` branch should use this job.
  * **Note:** 
    * No build can be directly deployed to the `go` environment without the deployment on `pre_go`. Ensure that the build from `release-go` is deployed to `pre_go`, tested and then deployed to `go`
    * Data Genie uses `go` as the PROD deployment because the app itself being an internal one is not deployed to the Zoom marketplace.
    * The deployment pipeline uses the Data Genie infra repo to deploy the latest image onto the ECS cluster. More details about the infra is documented below. 

# Data Genie Infrastructure
* Data Genie infra is deployed using Terraform. The repo can be found here - <>
* API Endpoints: 
  * PRE_GO - https://datagenie.zoomdt.corp.zoom.com/datagenie/v0/bot
  * GO - https://datagenie.go.zoomdt.corp.zoom.com/datagenie/v0/bot

# Data Genie Executive Users
Data Genie bot can be opened up to executives without any Sales role authorization. The table `zoom_data.lab_ds.datagenie_executive_users` holds the list of executive users. 

Apart from the Zoom Executives, if any internal user needs access to the bot app for development or testing, he/she also needs to be added to this table.

**Steps:**

1. Find the user_jid of the user who needs to be added to the executive users table. 
```sql
select user_id from ZOOM_DATA.ELT.DW_PRODUCT_D_ZM_USER where email ilike '%firstname.lastname@zoom.us%';
```
2. Insert the name and user_jid into the executive users table.

```sql
insert into zoom_data.lab_ds.datagenie_executive_users(name, user_jid) values('<Firstname> <Lastname>', '<user_jid>@xmpp.zoom.us');
```

3. Refresh Cache of the API server 
   * To refresh the executive users cache on the PRE_GO (development) server, make a call to ```https://datagenie.zoomdt.corp.zoom.com/datagenie/v0/bot``` on the browser
   * To refresh the executive users cache on the GO server (production), make a call to ```https://datagenie-user-refresh.go.zoomdt.corp.zoom.com``` on the browser

**Note:** To perform the above steps:
1. You should be connected to the Zoom VPN
2. You should have Snowflake Admin privileges 

# Monitoring & Analytics
* API Server logs are available in Cloudwatch under the following Log Groups:
  * PRE_GO - /aws/ecs/prod-datagenie
  * GO - /aws/ecs/go-datagenie
* Data Genie Usage and Performance Analytics for DEV and GO can be found in `Cloudwatch -> Dashboards -> DataGenie-Analytics-prod / DataGenie-Analytics-go`
* AWS Account - data_team_prod

# Other Important Links
* Create a Team Chat App - https://developers.zoom.us/docs/team-chat-apps/create/
* Zoom Chatbot Events - https://developers.zoom.us/docs/api/rest/reference/chatbot/events/#overview
* Message with Markdown - https://developers.zoom.us/docs/team-chat-apps/customizing-messages/message-with-markdown 
* Bot builder toolkit - https://nodebots.zoom.us/botbuilderkit/page/createMessage
