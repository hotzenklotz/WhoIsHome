#! /usr/bin/env python

import nmap
import time
import socket
import fcntl
import struct
import json
import sys
import requests
import ConfigParser

# Scan you local network for all hosts
def scan():

  hosts= str(get_lan_ip()) + "/24"
  nmap_args = "-sn" #simple host discovery without portscan

  scanner = nmap.PortScanner()
  scanner.scan(hosts=hosts, arguments=nmap_args)

  hostList = []

  for ip in scanner.all_hosts():

    host = {"ip" : ip}

    if "hostname" in scanner[ip]:
      host["hostname"] = scanner[ip]["hostname"]

    if "mac" in scanner[ip]["addresses"]:
      host["mac"] = scanner[ip]["addresses"]["mac"]

    hostList.append(host)

  return hostList


# Get your local network IP address. e.g. 192.168.178.X
def get_lan_ip():
  def get_interface_ip(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                            ifname[:15]))[20:24])

  ip = socket.gethostbyname(socket.gethostname())
  if ip.startswith("127.") and os.name != "nt":
    interfaces = [
        "eth0",
        "eth1",
        "eth2",
        "wlan0",
        "wlan1",
        "wifi0",
        "ath0",
        "ath1",
        "ppp0",
        ]
    for ifname in interfaces:
      try:
        ip = get_interface_ip(ifname)
        break
      except IOError:
        pass
  return ip


# Build the chat message being send to Slack
def notifySlack(newUsers, leftUsers, existingUsers):

  message = ""
  if len(newUsers) > 0:
    message += ", ".join(newUsers) + " just came into the office. "

  if len(leftUsers) > 0:
    message = ", ".join(leftUsers) + " just left the office. "

  if len(existingUsers) > 0:

    verb = "are" if len(existingUsers) > 1 else "is"
    message += ", ".join(existingUsers) + " " + verb + " still here."

  else:
    message += "No one else is here."

  sendSlackRequest(message)


# Send the HTTP Post Request to Slack
def sendSlackRequest(message):

  payload = json.dumps({
    "text" : message,
    "username" : "Secret Office Surveillance Bot",
    "channel" : "#general"
  })
  requests.post(SLACK_WEBHOOK, data=payload)


# Read the config file
def parseConfigFile():

  configParser = ConfigParser.ConfigParser()
  config = configParser.read("config.cfg")

  if len(config) < 1:
    print "Oops, couldn't read the config file. Consult the readme."
    sys.exit(0)

  try:
    slack_webhook = configParser.get("Slack", "webhook_url")
    know_hosts = dict([(mac, hostname) for hostname, mac in configParser.items("Hosts")])
  except ConfigParser.Error as e:
    print e
    print "Please correct your config file."
    sys.exit(0)

  if len(know_hosts) == 0:
    print "Oops, you did not specify any known hosts. Please correct your config file."
    sys.exit(0)

  return slack_webhook, know_hosts


# Entry point
if __name__ == "__main__":

  SLACK_WEBHOOK, KNOWN_HOSTS = parseConfigFile()

  # Initialize. Noone is here yet
  activeHosts = set()

  while True:

    scannedHosts = [host["mac"] for host in scan() if "mac" in host]
    recognizedHosts = set([KNOWN_HOSTS[host] for host in scannedHosts if host in KNOWN_HOSTS])
    print recognizedHosts

    # who joined the network?
    newHosts = recognizedHosts - activeHosts

    # who left the network?
    leftHosts = activeHosts - recognizedHosts

    # announce the new and leaving users in Slack
    if len(newHosts) > 0 or len(leftHosts) > 0:
      notifySlack(newHosts, leftHosts, activeHosts - leftHosts)

    # remember everyone for the next scan
    activeHosts = recognizedHosts

    # wait 60 seconds before trying again
    time.sleep(60)