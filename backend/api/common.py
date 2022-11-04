import requests, threading, time, multiprocessing
from api.models import Monitor


def validate_entry(entry, validators):
    if all(x in entry for x in validators):
        return True
    return False