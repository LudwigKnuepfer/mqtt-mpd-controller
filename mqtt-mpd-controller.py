#!/usr/bin/env python3

import os
import sys
import time

import configparser

import paho.mqtt.client as mqtt

CONFIG = None

def LOG(msg):
    print(msg)

def handle_config_entry(entry):
    if 'system_command' in entry:
        os.system(entry['system_command'])
        LOG("ran %s" % entry['system_command'])
    if 'mpd_path' in entry:
        os.system("mpc clear ; mpc ls %s | mpc add ; mpc play" % entry['mpd_path'])
        LOG("playing %s" % entry['mpd_path'])

def mqtt_on_message(client, userdata, msg):
    global CONFIG

    topic = msg.topic
    payload = msg.payload.decode()
    LOG("mqtt got message: %s: %s" % (topic, payload))

    if payload in CONFIG:
        handle_config_entry(CONFIG[payload])
    else:
        LOG("no action associated with this payload")

def mqtt_on_connect(client, userdata, flags, rc):
    global CONFIG
    if rc == 0:
        LOG("mqtt connected")

        for topic in CONFIG['MQTT']['event_topics'].split():
            client.subscribe(topic, qos=0)

        client.publish(
                CONFIG['MQTT']['status_topic'], "mpd-controller up and running", qos=0, retain=True)
    else:
        LOG("mqtt connection failed")
        sys.exit(1)

def mqtt_init():
    global CONFIG
    protocol = mqtt.MQTTv311
    if 'protocol' in CONFIG['MQTT']:
        pass

    client_id = CONFIG['MQTT'].get('client_id', 'mpd-controller')

    client = mqtt.Client(
            client_id=client_id, clean_session=False, protocol=protocol)

    client.on_connect = mqtt_on_connect
    client.on_message = mqtt_on_message

    return client

def main():
    global CONFIG
    config = configparser.ConfigParser()
    config.read('/etc/mqtt_mpc_controller/config.ini')
    CONFIG = config

    client = mqtt_init()
    try:
        client.connect(
                CONFIG['MQTT']['host'],
                int(CONFIG['MQTT']['port']),
                60)
    except socket.error as err:
        LOG(err)
        sys.exit(1)

    client.loop_start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        LOG("KeyboardInterrupt")
    finally:
        client.publish(
                CONFIG['MQTT']['status_topic'], "mpd-controller dead", qos=0, retain=True)
        time.sleep(0.1)
        client.disconnect()

    sys.exit(0)

if __name__ == "__main__":
    main()
