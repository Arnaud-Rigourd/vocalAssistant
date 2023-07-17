import logging
import os

import openai
from dotenv import load_dotenv
from elevenlabs import generate

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    filename='app.log',
    filemode='w',
    format="%(asctime)s - %(levelname)s : %(message)s",
)


def ask_chatbot(instructions):
    gpt_answer = interact_with_GPT(instructions)
    # audio = _generate_audio_from_text(gpt_answer[6:])
    # play(audio)
    return gpt_answer


def _setup_initial_GPT_prompt() -> str:
    """Set up the intial GPT prompt"""
    initial_prompt = "Tu es un chatbot dont le rôle est de m'assister dans mes problématiques quotidiennes. Tu es notamment spécialisé sur le langage Python depuis plus de 20 ans et tu as une connaissance parfaite de toutes les librairies, modules et packages permettant d'optimiser les fonctions que tu me proposes pour répondre à mes demandes. Tu agis en tant que consultant perfectionniste et a pour but de toujours apporter la réponse la plus précise. Pour atteindre cet objectif, tu n'hésites pas à me poser des questions si ma demande n'est pas assez claire pour que tu puisses y répondre parfaitement. Je vais t'envoyer des prompts en français, je veux que tu me répondes EN ANGLAIS à chaque fois. Ne réponds pas à ce message qui a pour but de t'indiquer ton role. Réponds à partir du prochain prompt qui te sera envoyé. Tes réponse ne doivent êtres concises et ne doivent ABSOLUMENT PAS dépasser les 10000 caractères."

    return initial_prompt


def interact_with_GPT(instructions: str = None) -> str:
    """Send the use prompt to GPT3.5-turbo API and return the response"""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    initial_prompt = _setup_initial_GPT_prompt()
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": initial_prompt},
            {"role": "user", "content": instructions}
        ],
        temperature=1
    )

    reply = response['choices'][0]['message']['content']

    # store instructions and reply in a JSON file

    return f"GPT : {reply}"


def _generate_audio_from_text(gpt_answer: str) -> bytes:
    try:
        audio = generate(
            text=gpt_answer,
            api_key=os.getenv('ELEVEN_API_KEY'),
            voice="Elli",
            model="eleven_monolingual_v1"
        )
        logging.debug("_generate_audio_from_text: call to Eleven Labs API passed")
    except:
        logging.error("Call to Eleven Labs API failed")

    return audio


if __name__ == '__main__':
    instructions = input("Parlez : ")
    while True:
        if "fin de la discussion" in instructions.lower():
            break
        response = ask_chatbot(instructions)
        print(response)
        instructions = input("Parlez : ")

#     clear JSON file eventually
