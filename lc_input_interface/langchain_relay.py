# lc_input_interface/langchain_relay.py
from lc_core import process_input

_last_output = None

def process_input_relay(input_text):
    global _last_output
    _last_output = process_input(input_text)
    return _last_output

def get_output():
    return _last_output
