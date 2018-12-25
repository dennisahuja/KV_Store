# KV Store

Basic Key Value Store in which Client and Server interact with the following functionalities :

1. Set a value to specified Key
2. Get the value of a specific Key
3. Get all Key Values in the KV Store
4. Listen to Server for any updates in the KV Store
5. Clear all values in the KV Store

## How to Set Up

Use pipenv to setup the environment :
```
pip install pipenv
pipenv install
```

# How to Use

Run Server with the following command :
```
pipenv run python server.py
```

Run client with the following command :
```
pipenv run python client.py --help
```
The help will guide you with the instructions on how to use the client.