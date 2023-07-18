from main import ask_chatbot, _get_initial_gpt_prompt


def test__ask_chatbot():
    assert type(ask_chatbot("Dis bonjour")) == str


def test__get_initial_gpt_prompt():
    assert type(_get_initial_gpt_prompt()) == str


def test_interact_with_gpt():
    assert False


def test__generate_audio_from_text():
    assert False


def test__get_remaining_characters():
    assert False
