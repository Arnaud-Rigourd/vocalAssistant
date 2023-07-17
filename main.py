def get_user_instructions():
    instructions = input("Parlez : ")
    print(instructions)


def _send_instruction_to_GPT(instructions: str) -> bool:
    """Send the use prompt to GPT4 API and return a boolean to indicate if the API request worked"""
    pass


def _read_text(GPTanswer: str):
    pass


if __name__ == '__main__':
    get_user_instructions()
