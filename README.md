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
python main.py noscan nocdp
```
(noscan & nocdp arguments disable scanner & customer display functionality)

#### Frontend:
```
cd web

npm run serve
```

# Screenshots

<p align="center">
<img src="screenshot_users.png" width="400"/> <img src="screenshot_pay.png" width="400"/> <img src="screenshot_buy.png" width="400"/> <img src="screenshot_transactions.png" width="400"/>
</p>

NOTE: Receipt printers are incredibly fun to mess around with.

[![forthebadge](https://forthebadge.com/images/badges/fuck-it-ship-it.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/contains-cat-gifs.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/compatibility-pc-load-letter.svg)](https://forthebadge.com)
