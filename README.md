# Discord Bot by JDR

Hey, there is the rpo of my discord bot 😀

- [Discord Bot by JDR](#discord-bot-by-jdr)
  - [Installation](#installation)


## Installation

To install the production version, proceed as follow:

```bash
$ cd directory/of/project/
$ python3 -m venv venv     # py instead of python3 on windows
$ ./venv/bin/activate      # .\venv\Scripts\activate on windows
(venv) $ python -m pip install --upgrade pip
(venv) $ pip install -r requirements.txt
```

Create a `.env` file and insert your environment variables as follow:
Be sure to create an app in the discord developer portal before.

```python
TOKEN=... #Token of your bot.
LOG_CHANNEL=... #ID of your log channel, so you can have error feedback 🤩
```
Then just launch `bot/main.py`, and your bot is ready.
You can also makes it run on Heroku, etc ...

  