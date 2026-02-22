import discord
from discord.ext import commands
import random
import os
from flask import Flask
import threading
import asyncio
import time

# OWNER ID (you) - always protected, can do everything
OWNER_ID = 864380109682900992  # ← CHANGE TO YOUR REAL DISCORD ID IF NEEDED

# VIP list - starts empty, added via /vipadd
VIP_IDS = []

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Mimic target
mimic_target = None

# 3 rotating playing statuses - changes every 5 seconds
STATUSES = [
    discord.Game(name="Daviccino Daddy 🔥"),
    discord.Game(name="Ohh kevin de brunye ⚽️"),
    discord.Game(name="Listening to Albert Fish")
]

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

    # Set DND + initial status
    await bot.change_presence(
        status=discord.Status.dnd,
        activity=STATUSES[0]
    )

    # Start rotation loop
    bot.loop.create_task(rotate_status())

    await bot.tree.sync()
    print("Slash commands synced!")

async def rotate_status():
    i = 0
    while True:
        await bot.change_presence(
            status=discord.Status.dnd,  # always DND
            activity=STATUSES[i]
        )
        i = (i + 1) % len(STATUSES)
        await asyncio.sleep(5)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Mimic mode
    global mimic_target
    if mimic_target and message.author.id == OWNER_ID:
        if mimic_target:
            webhook = await message.channel.create_webhook(name=bot.get_user(mimic_target).name)
            await webhook.send(
                content=message.content,
                username=bot.get_user(mimic_target).name,
                avatar_url=bot.get_user(mimic_target).avatar.url if bot.get_user(mimic_target).avatar else None
            )
            await webhook.delete()
            await message.delete()  # hide command

    await bot.process_commands(message)

# /mimic @user message - VIPs only
@bot.tree.command(name="mimic", description="Send message as another user (VIPs only)")
async def mimic(interaction: discord.Interaction, member: discord.Member, message: str):
    if interaction.user.id != OWNER_ID and interaction.user.id not in VIP_IDS:
        await interaction.response.send_message("Only VIPs can use this.", ephemeral=True)
        return

    if member.id == OWNER_ID:
        await interaction.response.send_message("Can't mimic the owner!", ephemeral=True)
        return

    if member.bot:
        await interaction.response.send_message("Can't mimic bots!", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)

    webhook = await interaction.channel.create_webhook(name=member.name)
    await webhook.send(
        content=message,
        username=member.name,
        avatar_url=member.avatar.url if member.avatar else None
    )
    await webhook.delete()

    await interaction.followup.send(f"Sent as {member.mention}.", ephemeral=True)

# !roast - anyone can use
@bot.command()
async def roast(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    if member.id == OWNER_ID:
        await ctx.send("Can't roast the owner! 👑")
        return

    harsh = [
        "{user}, bro your aura is negative 1000, touch grass.",
        "{user}, you give NPC energy fr.",
        "{user}, your jokes are drier than Sahara.",
        "{user}, bro tried to rizz but got curved.",
        "{user}, your fit is so mid even Wish said no.",
        "{user}, you're a 404 — not found.",
        "{user}, your vibe is so off Wi-Fi disconnected.",
        "{user}, bro you're built like a mod — zero aura.",
        "{user}, your playlist is trash.",
        "{user}, you're low battery 24/7.",
        "{user}, bro your haircut needs a glow-up.",
        "{user}, you're the reason mute exists sometimes.",
        "{user}, your chat is quiet today.",
        "{user}, bro you're the side character.",
        "{user}, your drip is basic.",
        "{user}, you're getting ratio'd by your mirror.",
        "{user}, your personality is chill but mid.",
        "{user}, bro you peaked somewhere.",
        "{user}, your memes are vintage.",
        "{user}, you're why 'seen' exists.",
        "{user}, bro your game is weak.",
        "{user}, your style is default.",
        "{user}, you're Comic Sans energy.",
        "{user}, bro your life is offline.",
        "{user}, you're 12-year-old deep.",
        "{user}, your roasts need spice.",
        "{user}, bro you're lagging.",
        "{user}, your energy is ghost mode.",
        "{user}, you're 'no cap' but cap.",
        "{user}, bro your face card is declined."
    ]

    light = [
        "{user}, bro your aura is kinda lowkey mid.",
        "{user}, you're giving background character vibes.",
        "{user}, your jokes are dry ngl.",
        "{user}, bro tried to rizz but nah.",
        "{user}, your fit is mid, step up.",
        "{user}, you're NPC energy.",
        "{user}, your vibe is off a bit.",
        "{user}, bro you're sidekick energy.",
        "{user}, your playlist needs work.",
        "{user}, you're low battery mode.",
        "{user}, bro your haircut is okay.",
        "{user}, you're the reason mute exists sometimes.",
        "{user}, your chat is quiet today.",
        "{user}, bro you're side character energy.",
        "{user}, your drip is basic.",
        "{user}, you're getting ratio'd by your mirror.",
        "{user}, your personality is chill.",
        "{user}, bro you peaked somewhere.",
        "{user}, your memes are vintage.",
        "{user}, you're why 'seen' exists.",
        "{user}, bro your game is okay.",
        "{user}, your style is default.",
        "{user}, you're Comic Sans energy.",
        "{user}, bro your life is offline.",
        "{user}, you're 12-year-old deep.",
        "{user}, your roasts are okay.",
        "{user}, bro you're lagging a bit.",
        "{user}, your energy is ghost mode.",
        "{user}, you're 'no cap' but cap.",
        "{user}, bro your face card is declined."
    ]

    if member.id in VIP_IDS:
        roast_text = random.choice(light).format(user=member.mention)
    else:
        roast_text = random.choice(harsh).format(user=member.mention)

    await ctx.send(roast_text)

# /say - VIPs only
@bot.tree.command(name="say", description="Bot says something (VIPs only)")
async def say(interaction: discord.Interaction, text: str):
    if interaction.user.id != OWNER_ID and interaction.user.id not in VIP_IDS:
        await interaction.response.send_message("Only VIPs can use this.", ephemeral=True)
        return
    await interaction.channel.send(text)
    await interaction.response.send_message("Sent.", ephemeral=True)

# /dm - VIPs only
@bot.tree.command(name="dm", description="Send DM to user (VIPs only)")
async def dm(interaction: discord.Interaction, member: discord.Member, text: str):
    if interaction.user.id != OWNER_ID and interaction.user.id not in VIP_IDS:
        await interaction.response.send_message("Only VIPs can use this.", ephemeral=True)
        return

    try:
        await member.send(text)
        await interaction.response.send_message(f"DM sent to {member.mention}.", ephemeral=True)
    except:
        await interaction.response.send_message(f"Failed to DM {member.mention} (DMs closed?).", ephemeral=True)

# /viplist - public
@bot.tree.command(name="viplist", description="Show VIP list (public)")
async def viplist(interaction: discord.Interaction):
    if not VIP_IDS:
        await interaction.response.send_message("No VIPs yet! 👑", ephemeral=False)
        return

    mentions = [f"<@{uid}>" for uid in VIP_IDS]
    await interaction.response.send_message(f"**VIPs:** 👑\n" + "\n".join(mentions), ephemeral=False)

# /vipadd - owner only
@bot.tree.command(name="vipadd", description="Add VIP (owner only)")
async def vipadd(interaction: discord.Interaction, member: discord.Member):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("Only owner can add VIPs.", ephemeral=True)
        return

    if member.id == OWNER_ID:
        await interaction.response.send_message("Owner is already VIP!", ephemeral=True)
        return

    if member.id in VIP_IDS:
        await interaction.response.send_message(f"{member.mention} is already VIP!", ephemeral=True)
        return

    VIP_IDS.append(member.id)
    await interaction.response.send_message(f"{member.mention} added to VIPs! 👑", ephemeral=True)

# /vipremove - owner only
@bot.tree.command(name="vipremove", description="Remove VIP (owner only)")
async def vipremove(interaction: discord.Interaction, member: discord.Member):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("Only owner can remove VIPs.", ephemeral=True)
        return

    if member.id == OWNER_ID:
        await interaction.response.send_message("Can't remove owner!", ephemeral=True)
        return

    if member.id not in VIP_IDS:
        await interaction.response.send_message(f"{member.mention} is not VIP!", ephemeral=True)
        return

    VIP_IDS.remove(member.id)
    await interaction.response.send_message(f"{member.mention} removed from VIPs.", ephemeral=True)

# Run bot in background
def run_discord_bot():
    time.sleep(5)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bot.start(os.getenv("DISCORD_TOKEN")))

threading.Thread(target=run_discord_bot, daemon=True).start()

# Flask keep-alive
app = Flask(__name__)

@app.route("/")
def home():
    return "Phantom Daviccino is alive! 🔥"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
