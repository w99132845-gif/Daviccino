import discord
from discord.ext import commands
import random
import os
from flask import Flask
import threading
import asyncio
import time
from datetime import datetime, timedelta

# OWNER ID (you) - always VIP + can do everything
OWNER_ID = 864380109682900992

# VIP list - starts empty, added via /addvip
VIP_IDS = []

# Blocked words - starts empty, added via /addblock
BLOCKED_WORDS = []

# Last roast tracking to prevent repeats (per user, 2 days)
last_roast = {}  # {target_id: (roast_index, timestamp)}

# Mimic target
mimic_target = None

# Auto-react targets
autoreact_targets = {}  # {user_id: emoji}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")
    await bot.tree.sync()
    print("Slash commands synced!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content_lower = message.content.lower()

    # Blocked words check - delete + warn (VIPs exempt)
    if not is_vip_user(message.author.id):
        for word in BLOCKED_WORDS:
            if word in content_lower.split():
                await message.delete()
                try:
                    await message.author.send("Warning: blocked word used. Your message was deleted.")
                except:
                    pass
                return

    # Mimic mode - bot speaks as the mimicked user
    global mimic_target
    if mimic_target and message.author.id == mimic_target:
        # Bot repeats what they say (as them)
        await message.channel.send(message.content)
        return  # don't process further

    # Auto-react
    if message.author.id in autoreact_targets:
        emoji = autoreact_targets[message.author.id]
        await message.add_reaction(emoji)

    await bot.process_commands(message)

# Helper: is VIP or owner?
def is_vip_user(user_id):
    return user_id == OWNER_ID or user_id in VIP_IDS

# !roast - VIPs can roast anyone, but NO ONE can roast owner
@bot.command()
async def roast(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    # Block roasting the owner
    if member.id == OWNER_ID:
        await ctx.send("Can't roast the owner! 👑")
        return

    # Only VIPs can roast
    if not is_vip_user(ctx.author.id):
        await ctx.send("Only VIPs can roast people.", delete_after=10)
        return

    # 80 normal, savage, non-cancelling roasts
    roast_list = [
        "{user}, bro your aura is negative 1000, go touch grass fr.",
        "{user}, you give main character energy... of a background NPC.",
        "{user}, your jokes are so dry the Sahara called and wants them back.",
        "{user}, bro tried to rizz but ended up in the friendzone lobby.",
        "{user}, your fit is so mid even Shein said no thanks.",
        "{user}, you’re the human version of a 404 error — not found.",
        "{user}, your vibe is so off even your Wi-Fi disconnected.",
        "{user}, bro you’re built like a Discord mod — zero aura.",
        "{user}, your playlist is so trash even Spotify apologised.",
        "{user}, you’re giving low battery energy 24/7.",
        "{user}, bro your haircut said “I can fix him” and failed.",
        "{user}, you’re the reason why mute exists in VC.",
        "{user}, your chat is so dead even ghosts left.",
        "{user}, bro you’re the side character in your own life.",
        "{user}, your drip is so bad even rain avoids you.",
        "{user}, you’re the type to get ratio’d by your own reflection.",
        "{user}, your personality is so dry we need subtitles.",
        "{user}, bro you’re giving “I peaked in high school” energy.",
        "{user}, your memes are so old they need a senior discount.",
        "{user}, you’re the reason why “seen” messages exist.",
        "{user}, bro your game is so weak even bots reject you.",
        "{user}, your style is so basic even NPCs have more drip.",
        "{user}, you’re the human version of Comic Sans — nobody takes you seriously.",
        "{user}, bro your life is on airplane mode — no connection.",
        "{user}, you’re giving “I’m 12 and this is deep” vibes.",
        "{user}, your roasts are so weak even toddlers clap back.",
        "{user}, bro you’re the human version of lag — always behind.",
        "{user}, your energy is so low even ghosts have more aura.",
        "{user}, you’re the reason why “no cap” needs a cap.",
        "{user}, bro your face card declined at birth.",
        "{user}, you’re giving expired milk energy — sour and unwanted.",
        "{user}, your chat is so dry even cactus said “damn”.",
        "{user}, bro you’re built like a participation trophy.",
        "{user}, your vibe is so off even GPS rerouted.",
        "{user}, you’re the type to get ghosted by your own shadow.",
        "{user}, bro your aura is so negative it’s a black hole.",
        "{user}, your personality is so mid even Switzerland called neutral.",
        "{user}, you’re giving “I use light mode” energy — cursed.",
        "{user}, bro your rizz is so bad even mirrors say no.",
        "{user}, your life is so boring even Wikipedia skipped it.",
        "{user}, you’re the reason why “seen” has 3 dots.",
        "{user}, bro your fit is so bad even thrift stores rejected it.",
        "{user}, your energy is so low even zombies have more life.",
        "{user}, you’re giving “default pfp” energy.",
        "{user}, bro your jokes are so old they need a cane.",
        "{user}, your vibe is so off even Spotify skipped your playlist.",
        "{user}, you’re the human version of buffering — always loading.",
        "{user}, bro your game is so weak even tutorial mode beat you.",
        "{user}, your aura is so weak even incense can’t smell it.",
        "{user}, you’re the reason why “no u” exists.",
        "{user}, bro your chat is so dead even crickets left.",
        "{user}, your drip is so bad even rain said “nah”.",
        "{user}, you’re giving “I peaked in preschool” energy.",
        "{user}, bro your roasts are so weak even toast said no.",
        "{user}, your personality is so basic even IKEA has more character.",
        "{user}, you’re the type to get left on read by your own group chat.",
        "{user}, bro your vibe is so mid even average said “step up”.",
        "{user}, your energy is so low even batteries sued you.",
        "{user}, you’re the reason why “seen” needs therapy.",
        "{user}, bro your life is so mid even mid said “damn”.",
        "{user}, your aura is so negative even magnets repelled you.",
        "{user}, you’re giving “I use default skin” energy.",
        "{user}, bro your rizz is so bad even autocorrect said no.",
        "{user}, your jokes are so dry even desert called jealous.",
        "{user}, you’re the human version of a loading screen — forever waiting.",
        "{user}, bro your fit is so bad even fashion police arrested it.",
        "{user}, your vibe is so off even GPS gave up.",
        "{user}, you’re giving “I’m the main character” energy… in a tutorial.",
        "{user}, bro your chat is so dead even zombies left.",
        "{user}, your energy is so low even ghosts said “too dead”.",
        "{user}, you’re the reason why “seen” has trust issues.",
        "{user}, bro your aura is so weak even whispers ignore you.",
        "{user}, your personality is so mid even middle child said no.",
        "{user}, you’re giving “default notification sound” energy.",
        "{user}, bro your roasts are so weak even bread laughed.",
        "{user}, your life is so mid even average said “step aside”.",
        "{user}, you’re the type to get ghosted by your own notifications."
    ]

    roast_text = random.choice(roast_list).format(user=member.mention)
    await ctx.send(roast_text)

# /say - VIPs ONLY
@bot.tree.command(name="say", description="Make the bot say anything (VIPs only)")
async def say(interaction: discord.Interaction, text: str):
    if not is_vip(interaction):
        await interaction.response.send_message("Only VIPs can use this command.", ephemeral=True)
        return
    censored = censor_text(text)
    await interaction.channel.send(censored)
    await interaction.response.send_message("Sent silently! 🔥", ephemeral=True)

# /addvip - OWNER ONLY
@bot.tree.command(name="addvip", description="Add a user to VIP list (owner only)")
async def addvip(interaction: discord.Interaction, member: discord.Member):
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

# /removevip - OWNER ONLY
@bot.tree.command(name="removevip", description="Remove a user from VIP list (owner only)")
async def removevip(interaction: discord.Interaction, member: discord.Member):
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

# /viplist - PUBLIC
@bot.tree.command(name="viplist", description="Show current VIP list (public)")
async def viplist(interaction: discord.Interaction):
    if not VIP_IDS:
        await interaction.response.send_message("No VIPs yet! 👑", ephemeral=False)
        return

    mentions = [f"<@{uid}>" for uid in VIP_IDS]
    await interaction.response.send_message(f"**VIPs:** 👑\n" + "\n".join(mentions), ephemeral=False)

# /mimic - VIPs ONLY
@bot.tree.command(name="mimic", description="Start mimicking a user (VIPs only)")
async def mimic(interaction: discord.Interaction, member: discord.Member):
    if not is_vip(interaction):
        await interaction.response.send_message("Only VIPs can use this.", ephemeral=True)
        return
    global mimic_target
    mimic_target = member.id
    await interaction.response.send_message(f"Now mimicking {member.mention} silently.", ephemeral=True)

# /stopmimic - VIPs ONLY
@bot.tree.command(name="stopmimic", description="Stop mimicking (VIPs only)")
async def stopmimic(interaction: discord.Interaction):
    if not is_vip(interaction):
        await interaction.response.send_message("Only VIPs can use this.", ephemeral=True)
        return
    global mimic_target
    mimic_target = None
    await interaction.response.send_message("Mimic stopped.", ephemeral=True)

# /autoreact - VIPs ONLY
@bot.tree.command(name="autoreact", description="Auto-react to a user's messages (VIPs only)")
async def autoreact(interaction: discord.Interaction, member: discord.Member, emoji: str):
    if not is_vip(interaction):
        await interaction.response.send_message("Only VIPs can use this.", ephemeral=True)
        return
    global autoreact_targets
    autoreact_targets[member.id] = emoji
    await interaction.response.send_message(f"Auto-react set for {member.mention} with {emoji}.", ephemeral=True)

# /stopautoreact - VIPs ONLY
@bot.tree.command(name="stopautoreact", description="Stop auto-react for a user (VIPs only)")
async def stopautoreact(interaction: discord.Interaction, member: discord.Member):
    if not is_vip(interaction):
        await interaction.response.send_message("Only VIPs can use this.", ephemeral=True)
        return
    global autoreact_targets
    if member.id in autoreact_targets:
        del autoreact_targets[member.id]
        await interaction.response.send_message(f"Auto-react stopped for {member.mention}.", ephemeral=True)
    else:
        await interaction.response.send_message(f"No auto-react set for {member.mention}.", ephemeral=True)

# /addblock - OWNER ONLY
@bot.tree.command(name="addblock", description="Add a word to blocked list (owner only)")
async def addblock(interaction: discord.Interaction, word: str):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("Only owner can add blocked words.", ephemeral=True)
        return

    if word.lower() in BLOCKED_WORDS:
        await interaction.response.send_message(f"'{word}' is already blocked.", ephemeral=True)
        return

    BLOCKED_WORDS.append(word.lower())
    await interaction.response.send_message(f"Blocked word added: {word}", ephemeral=True)

# /removeblock - OWNER ONLY
@bot.tree.command(name="removeblock", description="Remove a word from blocked list (owner only)")
async def removeblock(interaction: discord.Interaction, word: str):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("Only owner can remove blocked words.", ephemeral=True)
        return

    if word.lower() not in BLOCKED_WORDS:
        await interaction.response.send_message(f"'{word}' is not blocked.", ephemeral=True)
        return

    BLOCKED_WORDS.remove(word.lower())
    await interaction.response.send_message(f"Blocked word removed: {word}", ephemeral=True)

# /blocklist - PUBLIC
@bot.tree.command(name="blocklist", description="Show blocked words list (public)")
async def blocklist(interaction: discord.Interaction):
    if not BLOCKED_WORDS:
        await interaction.response.send_message("No blocked words yet.", ephemeral=False)
        return

    await interaction.response.send_message(f"**Blocked words:**\n" + ", ".join(BLOCKED_WORDS), ephemeral=False)

# Run bot in background
def run_discord_bot():
    time.sleep(5)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bot.start(os.getenv("DISCORD_TOKEN")))

threading.Thread(target=run_discord_bot, daemon=True).start()

# Flask for Render
app = Flask(__name__)

@app.route("/")
def home():
    return "Phantom Daviccino - safe & controlled mode is alive! 🔥"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
