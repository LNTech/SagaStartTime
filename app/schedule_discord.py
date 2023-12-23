"""Gets data from API and then sends it to Discord"""
from threading import Thread
from datetime import datetime
from time import sleep
from os.path import exists
from os import _exit

import requests
import schedule
import discord

class Embed:
    """Wrapper for Discord.py Embeds"""
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
        self.__connector()

    def __connector(self):
        """Creates partial webhook from webhook url"""
        webhook = self.webhook_url.split("/")
        self.webhook = discord.SyncWebhook.partial(webhook[-2], webhook[-1])

    def send_embed(self, location):
        """Creates discord embed and sends it to webhook url"""
        if len(location['locations']) == 0:
            return

        embed = discord.Embed(title=f"Treatment Start Time for {location['name']} (UTC)")

        for farm in location['locations']: # Add each farm field to the embed object
            embed.add_field(
                name=farm['name'],
                value=f"Start: {farm['times']['twilight_start']}\nEnd: {farm['times']['twilight_end']}",
                inline=False
            )

        embed.set_footer(text=f"Date: {datetime.today().date()}")
        self.webhook.send(embed=embed, avatar_url="https://yt3.googleusercontent.com/AY_S_jhwJz9jIxfQ-yyKr5AvbsHRrzS1h5bjOMcBEDd2DRTd-WLYsxznRWzAdZZlmPX1_yksdQ=s900-c-k-c0x00ffffff-no-rj")


def load_config():
    """Loads webhook URL from file"""

    if not exists("WEBHOOK.txt"):
        print("WEBHOOK.txt could not be found.")
        _exit(0)

    with open("WEBHOOK.txt", "r", encoding="utf-8") as file:
        file_lines =  [_.strip() for _ in file.readlines()]
        if len(file_lines) == 0:
            print("WEBHOOK.txt is empty.")
            _exit(0)

        return file_lines[0] # Return first line in file


def get_location(location, results):
    """Threaded function for getting location details from local API"""

    params={"loc_id": location['id']}

    start_time = requests.get(
        url=f"http://127.0.0.1:5000/api/start_time",
        timeout=9
    ).json()

    results.append({"name": location['name'], "times": start_time['times']})


def get_start_times():
    """Gets start times from countries /locations"""

    print("Getting treatment times!", end="", flush=True)
    WEBHOOK_URL = load_config()
    webhook = Embed(WEBHOOK_URL)

    countries = requests.get(url="http://127.0.0.1:5000/api/countries", timeout=9).json()
    for country in countries:
        params = {"country_id": country['id']}

        locations = requests.get(
            url=f"http://127.0.0.1:5000/api/locations/by_country",
            params=params,
            timeout=9
        ).json()

        locations = locations['locations']

        results = []
        threads = []

        # Threaded, in case there are a LOT of fields in a country, which is likely.
        for location in locations:
            thread = Thread(target=get_location, args=(location, results))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        webhook.send_embed({"name": country['name'], "locations": results})

    print("... Done!")


def main():
    """Main function handler"""

    print("[Started Script]")

    schedule.every().day.at("12:00").do(get_start_times)
    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == "__main__":
    main()
