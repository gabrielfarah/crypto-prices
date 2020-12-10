
## How to run this crypto demo

##### Create local docker network for all the containers`

Please run in your terminal:

`
docker network create coins_network
`

##### Creating all the containers images comes next 

Please run in your terminal:

`
./scripts/setup.sh
`

Since this process creates all the resources it may take a while to finish.

NOTE: if you get stuck on the "Waiting for build" please press Ctrl-C to skip


## Running the web app

`
./scripts/run-local.sh
`

## Stopping the web app

`
./scripts/kill-local.sh
`



#### Next Steps

1. Use the email created in setup to enter the Django Admin
2. Login and create a new crypto coin
3. Go to main page and download the CSV Template
4. Fill out the template with the coin name we created and a json rule: https://jsonlogic.com/
5. Getting the coin prices and validating the rules will be implemented in the future.