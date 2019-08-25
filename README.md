# Gladiabot
A bot for the browser-based game Gladiatus.

# Setup

Within a virtual python3 environment, install all the required packages in 'requirements.txt' with `pip install -r requirements.txt`.

[Download, install and setup Geckodriver](https://github.com/mozilla/geckodriver/releases)

Setup the required environment variables:

| Variable      | Description                       |
|---------------|-----------------------------------|
| user_email    | Email of the Gladiatus account    |
| user_password | Password of the Gladiatus account |

Make sure that the strings in `translation.py` are in the same language of your server.

Next, feel free to modify the `settings.py` with your desired data, and the bot should be ready to run!

To run the bot within your virtual environment simply doing `python main.py` should be enough.
