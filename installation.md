## Installation

To install the necessary dependencies, follow these steps:

1. **Create a virtual environment**:
   Replace "your_venv_name" with your preferred name for the virtual environment (omit the quotation marks).

   ```sh
   python -m venv your_venv_name
2. **Activate the enviorment for macOS**:
    For macOS:

    ```sh
    source your_venv_name/bin/activate

2. **Activate if you are on Windows**:
    For Windows:

    ```sh
    your_venv_name\Scripts\activate

3. **Install the required packages**:
    For this we will need the discord.py, discord-py-slash-command , dotenv packages.
    Make sure your virtual environment is activated before executing this command.

    ```sh
    pip install discord.py
    pip install discord discord-py-slash-command
    pip install python-dotenv
    

4. **Verify the packages you installed**:
    Make sure that packages is installed in your virtual environment.

    ```sh
    pip list

## Creating the bot

1. **Go to the [Discord Developer Portal](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://discord.com/developers/applications&ved=2ahUKEwj6zv-Xs7OFAxXehIkEHQDXBwQQFnoECBcQAQ&usg=AOvVaw1wrZe_Tr9Sav0Zx4-42-Jf) and create your bot**:
From this you create the bot name amongst othe things feel free to look around

2. **Get bot token**
After you have created your bot you should go to the Bot section and click the reset bot token and then copy that and place it inside your .env file in your repository.

3. **Set the bot permission using the url generator with the bot permission for the desired functionality of the bot**
For this bot you need to select bot, read message history, use commands(slash or others you register), and send messages.
That url link will generate and you can add it to your server.

## Running the bot

1. **Copy main.py script**
After you have copied the script run it, and then move over to discord and see that the bot is online.
**IMPORTANT**
Make sure that the bot has the correct permissions inside the specific text channel in order for it to work properly.

**Now you are done**
now the bot should be working properly and you should be good to go.
If you have any questions please feel free to message me with any you have and ill do my best to help you.
Happy botting!

    
