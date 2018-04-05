# mqtt-mpd-controller
This is  a python script that subscribes to MQTT and invokes commands (espically MPD) depending on what is published

# Installation

Assuming you're on a raspberry pi running the latest (as of this time) raspbian distribution (Debian 9.4):
```sh
sudo mkdir /etc/mqtt_mpc_controller # SIC
sudo cp config.ini /etc/mqtt_mpc_controller/
sudo vim /etc/mqtt_mpc_controller/config.ini # adjust to your needs
sudo cp mqtt-mpd-controller.py /usr/local/bin/mqtt_mpd_controller
sudo cp mqtt-mpd-controller.service /lib/systemd/system/
sudo systemctl enable mqtt-mpd-controller.service
sudo systemctl start mqtt-mpd-controller.service
```

# Installing Prerequisits

```sh
sudo apt install mpc
sudo pip3 install paho-mqtt
```

# Caveats

As of now, it is assumed that a local mpd instance is running and mpc is installed.
