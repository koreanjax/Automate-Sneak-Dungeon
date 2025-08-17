# Automate-Sneak-Dungeon
PAD Client receives some packets from the PAD Server.

The goal is to automate the fetching of the information from the packets rather than hand decrypting one by one.

First and foremost, you need decryption.py. This is not provided.

The provided card_data.json file is up-to-date as of August, 16th, 2025. I don't know if I will update this frequently for it to be reliable. Please update the card_data.json file on your own if you know how to.

There are couple things you need to setup before running proxy.py script.

1. Install necessary libraries using whatever installer you use.
2. Create a Root Certificate with tools like openssl and install the profile on your device.
3. After installing the certificate, setup a proxy on your P&D device that connects to the device you run proxy.py on.
4. Go to mitm.it domain and install the mitm certificate on your P&D device.
5. Enable full trust for both certificates.
6. Test connection by creating DumpMaster class with terminal logging.
7. Once you see packets being sniffed, rerun the script without logging to only see necessary information.