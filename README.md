# Telegram Registration Bot

This is a Telegram bot that registers new users and saves their information to a MySQL database.

## Features

- Step-by-step user registration process.
- Collects the following user data:
    - First Name
    - Last Name
    - Patronymic
    - Customer Phone
    - Contact Phone
    - Organization Name
    - Social Media (Instagram, VK, or Telegram)
- Saves the collected data to a MySQL database.

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the environment variables:**
   You need to set your Telegram Bot Token as an environment variable. Create a `.env` file in the root of the project and add the following line:
   ```
   TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
   ```
   The bot uses `python-dotenv` to load this variable, so make sure to install it (`pip install python-dotenv`).

   Alternatively, you can set the environment variable directly in your shell:
   ```bash
   export TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
   ```

5. **Database Configuration:**
   The database connection details are loaded from environment variables. Add the following to your `.env` file:
   ```
   DB_HOST="6a6153f2448029a1ea2d3be2.twc1.net"
   DB_USER="gen_user"
   DB_PASSWORD=">N+mW1$%LUarf}"
   DB_NAME="default_db"
   DB_PORT=3306
   ```

## Running the Bot

1. **Run the bot:**
   ```bash
   python bot.py
   ```

2. **Start a conversation with your bot on Telegram:**
   - Find your bot on Telegram.
   - Send the `/start` command to begin the registration process.

## How to Use

- Send the `/start` command to the bot to start the registration.
- Follow the prompts to enter your information.
- Use the `/cancel` command at any time to stop the registration process.