# Gladiabot
A bot for the browser-based game Gladiatus

# Setup

Within a virtual python3 environment, install all the required packages in 'requirements.txt' with `pip install -r requirements.txt`

[Download, install and setup Geckodriver](https://github.com/mozilla/geckodriver/releases)

```
wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
tar -xvzf geckodriver*
chmod +x geckodriver
sudo mv geckodriver /usr/local/bin/
rm geckodriver*
```

Setup the required environment variables:

| Variable      | Description                       |
|---------------|-----------------------------------|
| user_email    | Email of the Gladiatus account    |
| user_password | Password of the Gladiatus account |

Next, feel free to modify the `login_data`, `work_data` and `food_data` dictionaries of `main.py` with your desired data, and the bot should be ready to run! 
