import os
import json
import csv

import asyncio
from mitmproxy import http, options
from mitmproxy.tools.dump import DumpMaster

# not included for privacy reasons
from decryption import decrypt

from parser import waves_parser
from card_handler import Card
import json_to_csv

class ActionFilter:

    # Maybe it can be expanded for more information?
    ACTION_KEYWORDS = ['sneak_dungeon']

    # I don't think I need to pass cards through the async func. But for now it will stay.
    def __init__(self, cards: dict[int, Card]):
        self.cards = cards

    # Filter packets until we find our keyword for the action
    def request(self, flow: http.HTTPFlow):
        query_params = flow.request.query
        for key, value in query_params.items():
            for action in self.ACTION_KEYWORDS:
                if action == key.lower() or action == value.lower():
                    flow.metadata["matched_query"] = True
    
    # Once the packet is found, play around with the information
    def response(self, flow: http.HTTPFlow):
        if flow.metadata.get("matched_query"):
            text = flow.response.get_text(strict=False)
            try:
                data = json.loads(text)
                encrypted = data.get("e", None)
            except Exception as ex:
                encrypted = f"[Error parsing JSON: {ex}]"
                return

            print(f"{waves_parser(self.cards, decrypt(encrypted))}\n\n")

async def start(cards: dict[int, Card]):
    opts = options.Options(listen_port=8080)
    m = DumpMaster(opts, with_termlog=False, with_dumper=False)

    # turn off logging and command line output
    # m = DumpMaster(opts)

    m.addons.add(ActionFilter(cards))

    try:
        await m.run()
    except KeyboardInterrupt:
        print("Finishing Dungeon Drop Data Recording\n")
        await m.shutdown()

if __name__ == "__main__":
    print("Checking to see if card_data.csv file exists for card info parsing.")
    
    csv_path = "csv/card_data.csv"

    if os.path.exists(csv_path):
        print(f"File {csv_path} exists but may not be updated.")
    else:
        try:
            json_to_csv.main()
            print(f"File {csv_path} created using default card_data.json file.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
    # All this work just to make sure card information is accurately printed.
    if not os.path.exists(csv_path):
        print("Something went wrong during .csv file creation. Please check to see if you have the default or self-provided .json file.")
    else:
        cards = {}

        with open('csv/card_data.csv', 'r', encoding='utf8') as f:
            reader = csv.reader(f)
            for i, line in enumerate(reader):
                card = Card(line)
                cards[card.id] = card
        print("Dungeon Drop Data Recorded Below\n")
        asyncio.run(start(cards))