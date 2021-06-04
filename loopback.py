# LOOPBACK INTERFACE
# Simulates RockBLOCK web service for sending to mobile. The endpoint then echoes back
# a simulated reply from mobile, sent to the receive interface

import os
import binascii
import requests
from flask import Blueprint, request, url_for, current_app
#from flask_login import current_user
from datetime import datetime, timezone
from worker import q

endpoint = "/loopback"
momsn_file = "momsn.txt"
momsn_init = 99
rock7_date_format = "%y-%m-%d %H:%M:%S"


loopback_bp = Blueprint('loopback', __name__)

def read_momsn():
    momsn_str = ""
    
    # Create file if it doesn't exist
    if not os.path.exists(momsn_file):
        with open(momsn_file, "w") as f:
            f.write("{:d}\n".format(momsn_init)) # initial momsn
            f.close()
        
    try:
        with open(momsn_file, "r") as f:
            momsn_str = f.read()
            f.close()
            # parse value
            momsn = int(momsn_str)
    except OSError as e:
        print("-- loopback: momsn: {}: {}".format(momsn_file, e))
    except ValueError:
        momsn = momsn_init
    
    return momsn


def save_momsn(momsn):
    try:
        with open(momsn_file, "w") as f:
            f.write("{:d}\n".format(momsn))
            f.close()
    except OSError as e:
        print("FAILED,{}: error opening for write. {}".format(momsn_file, e))


def do_send(url, message):
    """
    do_send
    post message to receive endpoint, emulates Rock7 MT web call to user app
    """
    r = requests.post(url=url, data=message)
    print("-- loopback: do_send: url={} message={} status={}"
          .format(url, message, r.status_code))
    return


@loopback_bp.route(endpoint, methods=['post'])
def loopback_post():
    """
    loopback_post
    For testing sat-chat app. Emulates Rock7 MO web service
    """
    global momsn_file

    # Receive
    imei = request.form.get('imei')
    username = request.form.get('username')
    password = request.form.get('password')

    app = current_app

    # TODO: Simulate authentication with IMEI, USERNAME, PASSWORD

    # convert hex message back to text and add some text
    try:
        hex = request.form.get('data')
        text = binascii.a2b_hex(hex).decode("utf-8") + " reply"
        hex = binascii.b2a_hex(text.encode('utf-8'))
    except Exception as e:
        print("-- loopback: conversion error: {}".format(e))

    # Read static momsn message serial number from file
    momsn = read_momsn()

    # the loopback simulates an MO message, incrementing the momsn again
    mobile_momsn = momsn + 1

    message = {
        'imei': imei,
        'momsn': mobile_momsn + 1,
        'transmit_time': datetime.strftime(datetime.utcnow(), rock7_date_format),
        'iridium_latitude': "39.5807",
        'iridium_longitude': "-104.8772",
        'iridium_cep': 8.7,
        'data': hex
    }

    # use redis queue to enqueue call to do_send, delayed by 5 seconds
    job = q.enqueue_call(
        func=do_send, args=(
            os.environ['RECEIVE_ENDPOINT'], message,), result_ttl=5000
    )
    print("-- loopback: job id: {}".format(job.get_id()))

    # Update static momsn message serial number
    save_momsn(mobile_momsn+1)

    return "OK,{}".format(mobile_momsn)
