import logging
import os

from dotenv import load_dotenv
from elevenlabs import generate, play

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    filename='app.log',
    filemode='w',
    format="%(asctime)s - %(levelname)s : %(message)s",
)


def ask_chatbot():
    instructions = input("Parlez : ")
    GPT_prompt = _setup_GPT_prompt(instructions)
    GPTanswer = _get_GPT_answer(GPT_prompt)
    audio = _generate_audio_from_text(GPTanswer)
    return play(audio)


def _get_user_instructions():
    instructions = input("Parlez : ")
    print(instructions)


def _setup_GPT_prompt():
    initial_prompt = "Tu es un chatbot dont le rôle est de m'assister dans mes problématiques quotidiennes. Tu es notamment spécialisé sur le langage Python depuis plus de 20 ans et tu as une connaissance parfaite de toutes les librairies, modules et packages permettant d'optimiser les fonctions que tu me proposes pour répondre à mes demandes. Tu agis en tant que consultant perfectionniste et a pour but de toujours apporter la réponse la plus précise. Pour atteindre cet objectif, tu n'hésites pas à me poser des questions si ma demande n'est pas assez claire pour que tu puisses y répondre parfaitement. Je vais t'envoyer des prompts en français, je veux que tu me répondes EN ANGLAIS à chaque fois. Ne réponds pas à ce message qui a pour but de t'indiquer ton role. Réponds à partir du prochain prompt qui te sera envoyé. Tes réponse ne doivent êtres concises et ne doivent ABSOLUMENT PAS dépasser les 10000 caractères."
    return


def _get_GPT_answer(GPT_prompt: str) -> bool:
    """Send the use prompt to GPT4 API and return a boolean to indicate if the API request worked"""
    pass


def _generate_audio_from_text(GPTanswer: str) -> bytes:
    audio = generate(
        text=GPTanswer,
        api_key=os.environ.get('ELEVEN_API_KEY', 'default_value'),
        voice="Elli",
        model="eleven_monolingual_v1"
    )
    try:
        logging.debug("_generate_audio_from_text: call to Eleven Labs API passed")
        return audio
    except:
        logging.error("Call to Eleven Labs API failed")


if __name__ == '__main__':
    audio = _generate_audio_from_text("hey")
    print(type(audio))
