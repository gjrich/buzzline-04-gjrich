# buzzline-04-gjrich

We can analyze and visualize different types of streaming data as the information arrives.

The primary scripts are project_producer_gjrich.py and project_consumer_gjrich.py. 

project_producer_gjrich.py generates buzz messages of a medieval theme and writes them with authors to buzz_live.json. It then converts all letters to lower case and removes any non-letter characters, counts the number of time each letter appears in the message, and writes the letter distribution to buzz_letters.json.

project_consumer_gjrich.py then reads as messages are posted and generates a live histogram of the letter distribution in buzz_letters.json showing how many times each letter has shown up across all messages posted since the scripts began. This project uses matplotlib and its animation capabilities for visualization. 

Make sure to run the consumer before the producer for a clean session each time! This ensures the consumer does not miss any messages posted by the producer, and the consumer is designed to purge the contents of buzz_letters.json so your letter distribution reflects only those messages that have been posted since you started the consumer/producer.

If you have previously set up python 3.11 / kafka / zookeeper and set up and activated the virtual environment, you can simply run the script from two venv terminals
e.g. for windows


```shell
py -m consumers.project_consumer_gjrich
```

```shell
py -m producers.project_producer_gjrich
```



Otherwise, proceed with the full instructions.


## Step 0. Clone down repository & Install Python 3.11
Run this in the target repository (from powershell if windows). Git must be installed.

```shell
git clone https://github.com/gjrich/buzzline-04-gjrich/
```


Download Python 3.11 for your OS:

https://www.python.org/downloads/release/python-3119/


## Step 1. Manage Local Project Virtual Environment (Windows included

### Windows Instructions:
Create Virtual Environment (in project directory)

```shell
py -3.11 -m venv .venv
```

Activate / Install packages
```shell
.venv\Scripts\activate
py -m pip install --upgrade pip setuptools wheel
py -m pip install --upgrade -r requirements.txt
```

### Mac/Linux:
Create Virtual Environment (in project directory)
```zsh
python3 -3.11 -m venv .venv
```

Activate / Install packages
```zsh
source .venv/bin/activate
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install --upgrade -r requirements.txt
```

## Step 2. Start Zookeeper and Kafka (2 Terminals)

If Zookeeper and Kafka are not already running, you'll need to restart them.
See instructions at [SETUP-KAFKA.md] to:

1. Start Zookeeper Service ([link](https://github.com/denisecase/buzzline-02-case/blob/main/docs/SETUP-KAFKA.md#step-7-start-zookeeper-service-terminal-1))
2. Start Kafka ([link](https://github.com/denisecase/buzzline-02-case/blob/main/docs/SETUP-KAFKA.md#step-8-start-kafka-terminal-2))

---

## Step 3. Start the Streaming Application

This will take two additional terminals:

1. One to run the producer which writes to a file in the data folder. 
2. Another to run the consumer which reads from the dynamically updated file. 

For this example, we start with the consumer as it purges the JSON file and by starting it, we ensure we miss none of th emessages written by the producer.

### Consumer Terminal

First start the associated consumer that will process and visualize the messages. 

In VS Code, open a NEW terminal in your root project folder. 
Use the commands below to activate .venv, and start the consumer. 

Windows:
```shell
.venv\Scripts\activate
py -m consumers.project_consumer_gjrich
```

Mac/Linux:
```zsh
source .venv/bin/activate
python3 -m consumers.project_consumer_gjrich
```


### Producer Terminal

Start the producer to generate the messages. 

In VS Code, open a NEW terminal.
Use the commands below to activate .venv, and start the producer. 

Windows:

```shell
.venv\Scripts\activate
py -m producers.project_producer_gjrich
```

Mac/Linux:
```zsh
source .venv/bin/activate
python3 -m producers.project_producer_gjrich
```


## Troubleshooting
It's possible that your Environment will install Kafka/zookeeper differently than mine. 
If you run into errors with Kafka/zookeeper, you can check the IP your environment is set to run them on in ~/kafka/config/server.properties and ~/kafka/config/zookeeper.properties
Contrast the these with what is configured in this repository by searching the relevant files for 2181 and 9092, the ports which kafka and zookeeper run on.

## Save Space
To save disk space, you can delete the .venv folder when not actively working on this project.
You can always recreate it, activate it, and reinstall the necessary packages later. 
Managing Python virtual environments is a valuable skill. 

## License
This project is licensed under the MIT License as an example project. 
You are encouraged to fork, copy, explore, and modify the code as you like. 
See the [LICENSE](LICENSE.txt) file for more.
