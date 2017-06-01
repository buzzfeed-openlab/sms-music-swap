# sms-music-swap
A simple sms bot for mediating music recs between strangers

## About
This is a flask app that handles text message exchanges with strangers. It uses [Twilio](https://www.twilio.com/) to send/receive SMS.

In a nutshell, the app:
-  texts a prompt (currently the topic is music recs, but this can be adapted to fit other topics)
- stores responses
- texts randomly selected responses from strangers
- texts notifications when responses have been seen
- allows admins to moderate responses

#### Try it out by texting 1-415-851-7927

## Setup

**1. Make sure you have OS level dependencies**
- Python 3
- MySQL

**2. Clone this repo**
```bash
git clone https://github.com/buzzfeed-openlab/sms-music-swap.git
cd sms-music-swap
```

**3. Install required python libraries**

Optional but recommended: make a virtual environment using [virtualenv](https://virtualenv.readthedocs.io/en/latest/) and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html).

*Notes:*
- *Instructions for setting up virtualenv [here](http://docs.python-guide.org/en/latest/dev/virtualenvs/).*
- *`mkvirtualenv sms` will automatically activate the `sms` environment; to activate it in the future, just use `workon sms`*
- *if the virtualenv you make isn't python 3 (check w/ `python --version`), use `mkvirtualenv sms -p /path/to/your/python3` (find your python3 path with `which python3`)*


```bash
mkvirtualenv sms
```

Install requirements:
```bash
pip install -r requirements.txt
```

**4. create a MySQL database**

```bash
mysql -u root
```
& then
```bash
create database sms;
```

*If you're working locally, you're good to go. But if you're going to host this on a shared server you probably want to create a new user for this database instead of using `root`.*

**5. Configure the app**

There are two ways to do this: (a) making a config file or (b) setting environment variables.

You will need a twilio account & number to configure the app. (INSTRUCTIONS TO COME)

**Option A**  
Copy the example secret config file
```bash
cp sms_swap/app_config_secret.py.example sms_swap/app_config_secret.py
```

Then, edit `sms_swap/app_config_secret.py`.

**Option B**  
see `sms_swap/app_config.py` for the names of environment variables to set

**6. Run the app locally**
```bash
python application.py
```

**7. Initialize the database**

  Visit the `/initialize` route (e.g. `localhost:5000/intialize`) & enter admin credentials (`ADMIN_USER` & `ADMIN_PASS`). This will create the table for storing responses.
