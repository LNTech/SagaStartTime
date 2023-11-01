"""Gets data from API and then sends it to Discord"""

import requests
from datetime import datetime
from time import sleep
import schedule
import discord


with open("WEBHOOK_URL", "r", encoding="UTF-8") as file:
	if len(file.readlines()) > 0:
		WEBHOOk_URL = [_.strip() for _ in file.readlines()][0]
	else:
		print("WEBHOOK NOT PRESENT IN FILE")


class Embed:
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
        	embed.add_field(name=farm['name'], value=f"Start: {farm['times']['twilight_start']}\nEnd: {farm['times']['twilight_end']}", inline=False)

        embed.set_footer(text=f"Date: {datetime.today().date()}")
        self.webhook.send(embed=embed, avatar_url="https://yt3.googleusercontent.com/AY_S_jhwJz9jIxfQ-yyKr5AvbsHRrzS1h5bjOMcBEDd2DRTd-WLYsxznRWzAdZZlmPX1_yksdQ=s900-c-k-c0x00ffffff-no-rj")


webhook = Embed(WEBHOOk_URL)

def get_start_times():
    countries = requests.get("http://127.0.0.1:5000/api/countries").json()
    for country in countries:
        locations = requests.get(f"http://127.0.0.1:5000/api/locations/by_country/{country['id']}").json()
        locations = locations['locations']
        cleaned = []
        for location in locations:
            start_time = requests.get(f"http://127.0.0.1:5000/api/start_time/{location['id']}").json()
            cleaned.append({"name": location['name'], "times": start_time['times']})

        webhook.send_embed({"name": country['name'], "locations": cleaned})

def main():
    """Main function handler"""
    schedule.every().day.at("12:00").do(get_start_times)
    while True:
        schedule.run_pending()
        sleep(1)

if __name__ == "__main__":
    main()
