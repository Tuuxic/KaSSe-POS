A simple Point-of-Service software to manage the payments for beverages.
It uses [Vue](https://vuejs.org/), [SocketIO](https://socket.io/), [Flask](https://flask.palletsprojects.com/) and stores data as [JSON](https://www.json.org/) files.

## Setup

### Requirements:

- [Python 3.7](https://www.python.org/) (possibly works on later versions as well)
- [Node.js](https://nodejs.org/en/)

#### Backend:
```
pip install -r requirements.txt
```

#### Frontend:
```
cd web

npm install
```

## Deploy
#### Backend:
```
python main.py
```

#### Frontend:
```
cd web

npm run serve
```
## Server

If you want to run this on a server u have to change the "host" variable in App.vue to the IP address of your server (with the corresponding port of the backend)