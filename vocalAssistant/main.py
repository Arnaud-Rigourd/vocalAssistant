import json
import logging
import os
from functools import lru_cache
from pathlib import Path

import openai
import requests as requests
from dotenv import load_dotenv
from elevenlabs import generate, play
from tinydb import TinyDB

load_dotenv()

CUR_DIR = Path(__file__).resolve().parent

logging.basicConfig(
    level=logging.DEBUG,
    filename=f"{CUR_DIR}/app.log",
    filemode='a',
    format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    datefmt='%Y-%m-%d:%H:%M:%S',
)

db = TinyDB(f"{CUR_DIR}/history.json", indent=4)
chats = db.table("Chats")


def ask_chatbot(instructions) -> str:
    print("Thinking 🤔...")
    gpt_answer = interact_with_gpt(instructions)
    logging.debug("interact_with_GPT: success")
    print("Warming up the voice 🎤...")
    _generate_audio_from_text(gpt_answer[6:])
    logging.debug("_generate_audio_from_text: success")
    return _get_remaining_characters()


@lru_cache
def _get_initial_gpt_prompt() -> str:
    """Set up the intial GPT prompt"""
    initial_prompt = "Tu es un chatbot dont le rôle est de m'assister dans mes problématiques quotidiennes. Tu es notamment spécialisé sur le langage Python depuis plus de 20 ans et tu as une connaissance parfaite de toutes les librairies, modules et packages permettant d'optimiser les fonctions que tu me proposes pour répondre à mes demandes. Tu agis en tant que consultant perfectionniste et a pour but de toujours apporter la réponse la plus précise. Pour atteindre cet objectif, tu n'hésites pas à me poser des questions si ma demande n'est pas assez claire pour que tu puisses y répondre parfaitement. Je vais t'envoyer des prompts en français, je veux que tu me répondes EN ANGLAIS à chaque fois. Ne réponds pas à ce message qui a pour but de t'indiquer ton role. Réponds à partir du prochain prompt qui te sera envoyé. Tes réponse ne doivent êtres concises et ne doivent ABSOLUMENT PAS dépasser les 10000 caractères."

    return initial_prompt


def interact_with_gpt(instructions: str) -> str:
    """Send the use prompt to GPT3.5-turbo API and return the response"""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    initial_prompt = _get_initial_gpt_prompt()

    if chats:
        chats.insert({"role": "user", "content": instructions})
    else:
        chats.insert_multiple([
            {"role": "system", "content": initial_prompt},
            {"role": "user", "content": instructions},
        ])

    reply = _make_openai_api_request()

    return f"GPT : {reply}"


def _make_openai_api_request():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chats.all(),
            temperature=1
        )
        logging.debug("interact_with_gpt(): Success")
    except requests.exceptions.RequestException as e:
        logging.error(f"interact_with_gpt(): Failed -> {e}")
        raise e.response.status_code
    else:
        reply = response['choices'][0]['message']['content']
        chats.insert({"role": "assistant", "content": reply})

    return reply


def _generate_audio_from_text(gpt_answer: str) -> None:
    """Generates audio from text using Eleven Labs API"""
    try:
        audio = generate(
            text=gpt_answer,
            api_key=os.getenv('ELEVEN_API_KEY'),
            voice="Elli",
            model="eleven_monolingual_v1"
        )
        logging.debug("_generate_audio_from_text(): call to Eleven Labs API passed")
        print(gpt_answer)
        play(audio)
    except requests.exceptions.RequestException as e:
        logging.error("_generate_audio_from_text(): Call to Eleven Labs API failed")
        raise e.response.status_code
    else:
        return None


def _get_remaining_characters() -> str:
    headers = {
        "Accept": "application/json",
        "xi-api-key": os.getenv('ELEVEN_API_KEY')
    }

    response = _make_elevenlabs_api_request("https://api.elevenlabs.io/v1/user/subscription", **headers)
    # response_to_dict: dict = json.loads(response.text)
    remaining_characters: int = 10_000 - response["character_count"]

    return f"remaining characters: {remaining_characters}"


def _make_elevenlabs_api_request(url: str, **headers) -> json:
    try:
        response = requests.get(url, headers=headers)
        logging.debug("API request : Success")
    except requests.exceptions.RequestException as e:
        raise e.response.status_code
    else:
        return response.json()


if __name__ == '__main__':
    instructions = input("Parlez : ")
    while True:
        if "fin de la discussion" in instructions.lower():
            break
        response = ask_chatbot(instructions)
        print(response)
        instructions = input("Parlez : ")

    chats.truncate()
