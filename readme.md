# Who Is Home?

This Python script monitors your local network and notifies you of known hosts joining and leaving the network on everybody's favourite chat tool: Slack.

The network scan occurs every 60 seconds and the program is required to run as root to capture MAC-addresses of the network devices.

## Installation

```bash
// Install Python modules
pip install requests
pip install python-nmap

// Setuo the config file
cp example.cfg config.cfg
vim config.cfg
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

## Disclaimer

## License