# OpenAI-based Chatbot Assistant

This project contains a Python script that utilizes the OpenAI API to generate responses to user instructions. The
generated responses are then converted to audio using the Eleven Labs API, and the number of remaining characters for
the current month is displayed.

## Features

1. Interacting with the OpenAI API to obtain responses to user instructions.
2. Converting the text response from the OpenAI API to audio with the Eleven Labs API.
3. Handling interactions with a TinyDB database to log messages exchanged with the chatbot.
4. Displaying the number of remaining characters for the current month on the Eleven Labs API.

## Installation

Clone this repository in your local environment and ensure you have Python 3.7 or later installed. Install the necessary
dependencies with the following command:

```bash
pip install -r requirements.txt
```

## Configuration

This script requires some environment variables to function correctly:

- `OPENAI_API_KEY`: Your API key for the OpenAI API.
- `ELEVEN_API_KEY`: Your API key for the Eleven Labs API.

These environment variables can be set in a `.env` file.

## Usage

To use this script, you can run the following command in your terminal:

```bash
python3 main.py
```

## Tests

The unit tests for this script are not yet implemented, but feel free to contribute some!

## Contribution

Contributions to this project are welcome. Feel free to open an issue or submit a pull request.

