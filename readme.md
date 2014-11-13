## Installation

```bash
pip install requests
pip install python-nmap

// if you would like to used status LEDs on the Raspberry Pi
pip install RPi.GPIO
```

## Execution

Make sure to run the program as Route in order to collect MAC addresses from the network interface.

```bash
sudo python whoIsHome.py
```

## Requirements

Make sure you have the following programms installed and running on your system
- Python
- NMap

## Slack Integration

In order to get notified in Slack you have to setup a webhook. Follow the instructions on the Slack website: [https://YOUR-ORGANIZATION.slack.com/services/new/incoming-webhook](https://YOUR-ORGANIZATION.slack.com/services/new/incoming-webhook)
Enter the resulting webhhok URL in the config file.

## FAQ

### 1. Nothing is working.
Make sure you run the programm as root user. Only root will capture the MAC address of everyone on the network.

## Disclaimer

## License