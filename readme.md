# Who Is Home?

This Python script monitors your local network and notifies you of known hosts joining and leaving the network on everybody's favourite chat tool: Slack. Yet another good use case for a Raspberry Pi.

The network scan occurs every 60 seconds and the program is required to run as root to capture MAC-addresses of the network devices.

## Installation

```bash
// Install Python modules
pip install requests
pip install python-nmap

// Discover hosts on your local network
// and gather their MAC address for the config
arp -a
// or
sudo nmap -sn 192.168.178.0/24

// Setup the config file
cp example.json config.json
vim config.json
```

If you wish to run the script on system start you can use the prodvided init.d script (Linux only). Make sure you modify the init.d script to fit your needs (correct user and paths).
```bash
chmod +x initd.sh
sudo cp initd.sh /etc/init.d/whoishome
touch /var/log/whoishome.log && chown root /var/log/whoishome.log # CHANGE USER HERE
update-rc.d whoishome defaults
service \"whoishome\" start"
```

## Execution

Make sure to run the program as root in order to collect MAC addresses from the network interface.

```bash
sudo python whoIsHome.py
```

## Requirements

Make sure you have the following programms installed and running on your system:
- Python (only tested version 2.7)
- NMap

## Slack Integration

In order to get notified in Slack you have to setup a webhook. Follow the instructions on the Slack website: [https://YOUR-ORGANIZATION.slack.com/services/new/incoming-webhook](https://YOUR-ORGANIZATION.slack.com/services/new/incoming-webhook)
Enter the resulting webhhok URL in the config file.

## Disclaimer & License

Depending on your country of origin, scanning a network might be legal or not. Please research your local laws first. Get the permission of your network administrator and other users on the network before using this script.

---

The MIT License (MIT)

Copyright (c) 2014 Tom Herold

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
