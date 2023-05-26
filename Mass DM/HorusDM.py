import discord
from discord.ext import commands
import os
import time
import random
import platform
import sys
import json

bot = commands.Bot(command_prefix=":", intents=discord.Intents.all())

# Charger les paramètres à partir du fichier config.json
with open('config.json', 'r') as f:
    config = json.load(f)

bot_token = config.get('bot_token')
webhook_url = config.get('webhook_url')
webhook_logs_enabled = config.get('webhooklogs', True)
blacklisted_ids = config.get('blacklisted_ids', [])

def clear_screen():
    os_name = platform.system()
    if os_name == "Windows":
        os.system("cls")
    else:  # Linux, macOS, etc.
        os.system("clear")

def send_webhook_message(content):
    if webhook_logs_enabled:
        webhook = discord.Webhook.from_url(webhook_url, adapter=discord.RequestsWebhookAdapter())
        webhook.send(content)

def print_ascii_message():
    ascii_message = r"""
██╗░░██╗░█████╗░██████╗░██╗░░░██╗░██████╗
██║░░██║██╔══██╗██╔══██╗██║░░░██║██╔════╝
███████║██║░░██║██████╔╝██║░░░██║╚█████╗░
██╔══██║██║░░██║██╔══██╗██║░░░██║░╚═══██╗
██║░░██║╚█████╔╝██║░░██║╚██████╔╝██████╔╝
╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝░╚═════╝░╚═════╝░
DM Tool made by $heldon_#1705
"""
    sys.stdout.write("\033[1;37m" + ascii_message + "\n")
    sys.stdout.flush()

@bot.event
async def on_connect():
    clear_screen()
    print_ascii_message()
    print(f"Connecté au bot : {bot.user.name}")

@bot.event
async def on_ready():
    message = input('Message : ')
    total_members = sum(len(guild.members) for guild in bot.guilds)
    dmed = 0
    failed = 0
    for guild in bot.guilds:
        for member in guild.members:
            if member.id not in blacklisted_ids:
                try:
                    await member.send(message)
                    print_success(member.name)
                    dmed += 1
                    time.sleep(random.uniform(0.5, 1.5))
                except:
                    print_failure(member.name)
                    failed += 1

    print_status(dmed, failed, total_members)

def print_status(success_count, failure_count, total):
    status_message = f"DM Réussi : {success_count} / DM Fail : {failure_count} (TOTAL : {total})"
    send_webhook_message(status_message)

def print_success(member_name):
    success_messages = ["a été DM avec succès !", "a reçu le message avec succès !", "a bien reçu le DM !"]
    message = random.choice(success_messages)
    success_message = member_name +" " + message
    sys.stdout.write("\033[0;32m" + success_message + "\n")
    sys.stdout.flush()
    send_webhook_message(success_message)

def print_failure(member_name):
    failure_messages = ["n'a pas reçu le DM !", "n'a pas pu recevoir le message.", "n'a pas été atteint."]
    message = random.choice(failure_messages)
    failure_message = member_name + " " + message
    sys.stdout.write("\033[0;31m" + failure_message + "\n")
    sys.stdout.flush()
    send_webhook_message(failure_message)

bot.run(bot_token)
