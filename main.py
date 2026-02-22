import discord
from discord.ext import commands
import random
import os
from flask import Flask
import threading
import asyncio
import time

# OWNER ID (you) - always protected, can do everything
OWNER_ID = 864380109682900992  # CHANGE THIS TO YOUR REAL ID

# VIP list - starts empty, added via /vipadd
VIP_IDS = []

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")
    await bot.tree.sync()
    print("Slash commands synced!")

# Harsh roasts for normal people
harsh_roasts = [
    "{user}, bro your aura is so negative even black holes said 'damn'.",
    "{user}, you give main character energy... of a background NPC that dies in chapter 1.",
    "{user}, your jokes are so dry the Sahara called and wants royalties.",
    "{user}, bro tried to rizz but got sent to the shadow realm.",
    "{user}, your fit is so mid even Wish said 'nah'.",
    "{user}, you're the human version of a 404 error — not found and nobody cares.",
    "{user}, your vibe is so off even your Wi-Fi ghosted you.",
    "{user}, bro you're built like a Discord mod — zero aura, infinite ego.",
    "{user}, your playlist is so trash even autoplay apologised.",
    "{user}, you're giving low battery energy 24/7.",
    "{user}, bro your haircut said 'I can fix him' and failed miserably.",
    "{user}, you're the reason 'mute' exists in every VC.",
    "{user}, your chat is so dead even ghosts left the server.",
    "{user}, bro you're the side character in your own life story.",
    "{user}, your drip is so bad even rain avoids you.",
    "{user}, you're the type to get ratio'd by your own reflection.",
    "{user}, your personality is so dry we need subtitles.",
    "{user}, bro you’re giving 'I peaked in high school' energy.",
    "{user}, your memes are so old they need a senior discount.",
    "{user}, you're the reason 'seen' messages exist.",
    "{user}, bro your game is so weak even bots reject you.",
    "{user}, your style is so basic even NPCs have more drip.",
    "{user}, you're the human version of Comic Sans — nobody takes you seriously.",
    "{user}, bro your life is on airplane mode — no connection.",
    "{user}, you're giving 'I'm 12 and this is deep' vibes.",
    "{user}, your roasts are so weak even toddlers clap back.",
    "{user}, bro you're the human version of lag — always behind.",
    "{user}, your energy is so low even ghosts have more aura.",
    "{user}, you're the reason why 'no cap' needs a cap.",
    "{user}, bro your face card declined at birth."
]

# Light roasts for VIPs
light_roasts = [
    "{user}, bro your aura is lowkey mid today.",
    "{user}, you give background character energy fr.",
    "{user}, your jokes are kinda dry ngl.",
    "{user}, bro tried to rizz but got curved.",
    "{user}, your fit is mid, step up.",
    "{user}, you're giving NPC vibes.",
    "{user}, your vibe is off a little.",
    "{user}, bro you're built like a sidekick.",
    "{user}, your playlist needs work.",
    "{user}, you're low battery energy.",
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

# !roast - anyone can use, but VIPs get light roast, owner blocked
@bot.command()
async def roast(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    # Block roasting owner
    if member.id == OWNER_ID:
        await ctx.send("Can't roast the owner! 👑")
        return

    # Choose roast list based on target
    if member.id in VIP_IDS:
        roast_text = random.choice(light_roasts).format(user=member.mention)
    else:
        roast_text = random.choice(harsh_roasts).format(user=member.mention)

    await ctx.send(roast_text)

# /say - VIPs only
@bot.tree.command(name="say", description="Make bot say something (VIPs only)")
async def say(interaction: discord.Interaction, text: str):
    if interaction.user.id != OWNER_ID and interaction.user.id not in VIP_IDS:
        await interaction.response.send_message("Only VIPs can use this.", ephemeral=True)
        return
    await interaction.channel.send(text)
    await interaction.response.send_message("Sent silently.", ephemeral=True)

# /dm - VIPs only
@bot.tree.command(name="dm", description="Send DM to user (VIPs only)")
async def dm(interaction: discord.Interaction, member: discord.Member, text: str):
    if interaction.user.id != OWNER_ID and interaction.user.id not in VIP_IDS:
        await interaction.response.send_message("Only VIPs can use this.", ephemeral=True)
        return

    try:
        await member.send(text)
        await interaction.response.send_message(f"DM sent to {member.mention} silently.", ephemeral=True)
    except:
        await interaction.response.send_message(f"Failed to DM {member.mention} (DMs closed?).", ephemeral=True)

# /viplist - public
@bot.tree.command(name="viplist", description="Show current VIP list (public)")
async def viplist(interaction: discord.Interaction):
    if not VIP_IDS:
        await interaction.response.send_message("No VIPs yet! 👑", ephemeral=False)
        return

    mentions = [f"<@{uid}>" for uid in VIP_IDS]
    await interaction.response.send_message(f"**VIPs:** 👑\n" + "\n".join(mentions), ephemeral=False)

# /vipadd - owner only
@bot.tree.command(name="vipadd", description="Add user to VIP list (owner only)")
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
@bot.tree.command(name="vipremove", description="Remove user from VIP list (owner only)")
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

# Flask for Render keep-alive
app = Flask(__name__)

@app.route("/")
def home():
    return "Phantom Daviccino is alive! 🔥"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
