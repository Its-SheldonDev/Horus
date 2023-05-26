import os
import discord
import json
import re
from colorama import Fore

client = discord.Client()

def center(var, space=None):
    if not space:
        space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines()) / 2)])) / 2

    return "\n".join((' ' * int(space)) + line for line in var.splitlines())

class Console:
    def __init__(self, username, id):
        self.username = username
        self.id = id

    def print_header(self):
        os.system('cls && title Discord Message Searcher - Made By Kaneki Web')
        header = f"""
        ███████╗███████╗ █████╗ ██████╗  ██████╗██╗  ██╗███████╗██████╗ 
        ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝██║  ██║██╔════╝██╔══██╗
        ███████╗█████╗  ███████║██████╔╝██║     ███████║█████╗  ██████╔╝  
        ╚════██║██╔══╝  ██╔══██║██╔══██╗██║     ██╔══██║██╔══╝  ██╔══██╗
        ███████║███████╗██║  ██║██║  ██║╚██████╗██║  ██║███████╗██║  ██║  
        ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
        
        Login as: {Fore.CYAN}{self.username}{Fore.RESET} ({Fore.CYAN}{self.id}{Fore.RESET})
        """
        print(center(header).replace('█', Fore.RED + "█" + Fore.RESET))

    def print_message(self, message, message_type):
        print(f"[{Fore.GREEN}{message_type}{Fore.RESET}] Message Found: {message.content}")
        with open('found.txt', 'a+') as file:
            file.write(f"{message.author.name}: {message.content}\n")

class DiscordMessageSearcher:
    def __init__(self, config):
        self.config = config

    async def search_text_channels(self, guild):
        for channel in guild.text_channels:
            print(f"[{Fore.CYAN}CHANNEL{Fore.RESET}] Scan du salon: {channel.name}", end="\r")
            async for message in channel.history(limit=99999):
                self.search_message(message)

    async def search_dm_channels(self, client):
        for prv_channel in client.private_channels:
            print(f"[{Fore.CYAN}CHANNEL{Fore.RESET}] Scan du DM: {str(prv_channel).replace('Direct Message with ', '')}", end="\r")
            channel = client.get_channel(prv_channel.id)
            async for message in channel.history(limit=99999):
                self.search_message(message)

    def search_message(self, message):
        for search_message in self.config['words']:
            if search_message in message.content:
                Console().print_message(message, 'MESSAGE')

        for regex in self.config['regex']:
            if re.match(r"" + regex, message.content):
                Console().print_message(message, 'MESSAGE')

@client.event
async def on_ready():
    console = Console(str(client.user), str(client.user.id))
    console.print_header()

    searcher = DiscordMessageSearcher(config)

    if config['type']['servers'].lower() == "yes":
        serveur_count = 0
        channels_count = 0
        messages_count = 0
        for guild in client.guilds:
            print(f"[{Fore.RED}SERVER{Fore.RESET}] Scan du serveur: {guild.name}")
            serveur_count += 1
            await searcher.search_text_channels(guild)
            channels_count += len(guild.text_channels)
            messages_count += len(await guild.fetch_message())

    if config['type']['dm'].lower() == "yes":
        dm_count = 0
        await searcher.search_dm_channels(client)
        dm_count += len(client.private_channels)

    input(f"{Fore.RED}{messages_count}{Fore.RESET} Messages ont été scanné depuis {Fore.RED}{channels_count}{Fore.RESET} Salons ({Fore.RED}{serveur_count}{Fore.RESET} Serveurs, {Fore.RED}{dm_count}{Fore.RESET} DMs)")

client.run(config["token"], bot=False)
