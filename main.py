import discord
from discord.ext import commands
import random
import os
from flask import Flask
import threading
import asyncio
import time

# OWNER ID (you) - always VIP
OWNER_ID = 864380109682900992

# VIP list - starts empty, only added via /addvip
VIP_IDS = []

# Global variables for mimic and autoreact
mimic_target = None           # User ID being mimicked
autoreact_targets = {}        # {user_id: emoji}

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

    # Mimic mode
    global mimic_target
    if mimic_target and message.author.id == mimic_target:
        await message.channel.send(message.content)

    # Auto-react mode
    if message.author.id in autoreact_targets:
        emoji = autoreact_targets[message.author.id]
        await message.add_reaction(emoji)

    await bot.process_commands(message)

# Helper: check if user is VIP or owner
def is_vip(user_id):
    return user_id == OWNER_ID or user_id in VIP_IDS

# !roast - ANYONE can use, but blocks VIPs and owner
@bot.command()
async def roast(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    if member.id == OWNER_ID or member.id in VIP_IDS:
        await ctx.send("Can't roast the owner or VIPs! 👑")
        return

    # 50 ultra-dark roasts
    roast_list = [
        "{user}, you worthless piece of shit, your mom should've swallowed you like the cum you are.",
        "{user}, go fucking hang yourself, you pathetic cunt — no one would miss your retarded ass.",
        "{user}, your dad fucked off for milk because even he couldn't stand your ugly fucking face.",
        "{user}, you're a walking abortion failure, you stupid bitch — the coat hanger should've finished the job.",
        "{user}, kill yourself slowly, you disgusting faggot — make it painful so we can enjoy it.",
        "{user}, your family tree is full of inbred retards because no one else would fuck your ugly ancestors.",
        "{user}, you're the reason rape babies should be drowned at birth, you filthy whore.",
        "{user}, your mom is a cum dumpster and you're the proof she should've used protection, you bastard child.",
        "{user}, go overdose on heroin, you junkie piece of trash — the world would be cleaner without you.",
        "{user}, you're so fucking ugly even blind kids run away screaming, you deformed freak.",
        "{user}, your dad beats you because even he hates the mistake he created, you worthless scum.",
        "{user}, you're a pedo hiding in plain sight — everyone knows you touch kids, you sick fuck.",
        "{user}, your life is so shit even cancer said 'nah, not worth it', you diseased cunt.",
        "{user}, go jump off a bridge, you suicidal emo bitch — do us all a favor.",
        "{user}, your mom spreads her legs for anyone — you're just the cheapest cumshot she ever took.",
        "{user}, you're the type of retard who gets fucked by dogs and enjoys it, you degenerate.",
        "{user}, your whole family should be gassed — starting with your ugly ass.",
        "{user}, you're a nigger-loving whore who deserves to be raped again, you filthy slut.",
        "{user}, go cut your wrists deeper this time, you attention-seeking emo faggot.",
        "{user}, your dad molested you and that's why you're such a broken little bitch.",
        "{user}, you're so fat and ugly even necrophiliacs wouldn't fuck your corpse.",
        "{user}, your life is a mistake — fix it by swallowing bleach, you useless cunt.",
        "{user}, you're the reason why incest should be punishable by death — look at your fucked up face.",
        "{user}, go get AIDS and die slow, you dirty HIV-carrying whore.",
        "{user}, your mom is a crackhead prostitute and you're the result of a $5 trick.",
        "{user}, you're so retarded even special ed schools rejected you, you dumb fuck.",
        "{user}, go shoot up your school, you psychotic little shit — make us proud.",
        "{user}, your dad wishes he pulled out — you're the cum stain he regrets most.",
        "{user}, you're a tranny freak who should be burned alive for existing.",
        "{user}, your whole existence is a hate crime against humanity.",
        "{user}, go get cancer in your asshole, you gay faggot — suffer slow.",
        "{user}, you're the reason why bombs should target retarded families like yours.",
        "{user}, your mom fucked a dog and that's how you were born, you mongrel bastard.",
        "{user}, you're so worthless even Satan wouldn't take your soul.",
        "{user}, go drown in cum, you gangbang slut — that's all you're good for.",
        "{user}, your life is a Holocaust that never happened — too bad.",
        "{user}, you're a child rapist in training — we all see it, you sick pedo cunt.",
        "{user}, go set yourself on fire, you flammable piece of trash.",
        "{user}, your dad beats your mom because even she regrets birthing you.",
        "{user}, you're the cum your dad should've shot in the toilet.",
        "{user}, go get run over by a truck, you roadkill-looking motherfucker.",
        "{user}, your existence is the only argument for genocide.",
        "{user}, you're so ugly even your reflection commits suicide.",
        "{user}, go eat shit and die, you coprophilic freak.",
        "{user}, your mom is a meth whore and you're the crystal baby.",
        "{user}, you're the reason why some people support forced sterilization.",
        "{user}, go fuck your sister again — it's the only action you'll ever get.",
        "{user}, your life is a death sentence that hasn't been carried out yet.",
        "{user}, you're a walking STD — quarantine yourself permanently.",
        "{user}, your dad wishes he was gay so he never would've fucked your mom.",
        "{user}, go choke on a dick and die, you throat cancer candidate."
    ]

    roast_text = random.choice(roast_list).format(user=member.mention)
    await ctx.send(roast_text)

# /say - VIPs ONLY
@bot.tree.command(name="say", description="Make the bot say anything (VIPs only)")
async def say(interaction: discord.Interaction, text: str):
    if not (interaction.user.id == OWNER_ID or interaction.user.id in VIP_IDS):
        await interaction.response.send_message("Only VIPs can use this command.", ephemeral=True)
        return
    await interaction.channel.send(text)
    await interaction.response.send_message("Sent silently! 🔥", ephemeral=True)

# /addvip - OWNER ONLY
@bot.tree.command(name="addvip", description="Add a user to VIP list (owner only)")
async def addvip(interaction: discord.Interaction, member: discord.Member):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("Only the owner can use /addvip.", ephemeral=True)
        return

    if member.id == OWNER_ID:
        await interaction.response.send_message("Owner is already VIP!", ephemeral=True)
        return

    if member.id in VIP_IDS:
        await interaction.response.send_message(f"{member.mention} is already VIP!", ephemeral=True)
        return

    VIP_IDS.append(member.id)
    await interaction.response.send_message(f"{member.mention} is now VIP! 👑", ephemeral=True)

# /removevip - OWNER ONLY
@bot.tree.command(name="removevip", description="Remove a user from VIP list (owner only)")
async def removevip(interaction: discord.Interaction, member: discord.Member):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("Only the owner can use /removevip.", ephemeral=True)
        return

    if member.id == OWNER_ID:
        await interaction.response.send_message("Can't remove owner!", ephemeral=True)
        return

    if member.id not in VIP_IDS:
        await interaction.response.send_message(f"{member.mention} is not VIP!", ephemeral=True)
        return

    VIP_IDS.remove(member.id)
    await interaction.response.send_message(f"{member.mention} is no longer VIP.", ephemeral=True)

# /viplist - PUBLIC
@bot.tree.command(name="viplist", description="Show current VIP list (public)")
async def viplist(interaction: discord.Interaction):
    if not VIP_IDS:
        await interaction.response.send_message("No VIPs yet! 👑", ephemeral=False)
        return

    mentions = [f"<@{uid}>" for uid in VIP_IDS]
    await interaction.response.send_message(f"**Current VIPs:** 👑\n" + "\n".join(mentions), ephemeral=False)

# /mimic - VIPs ONLY
@bot.tree.command(name="mimic", description="Start mimicking a user (VIPs only)")
async def mimic(interaction: discord.Interaction, member: discord.Member):
    if not (interaction.user.id == OWNER_ID or interaction.user.id in VIP_IDS):
        await interaction.response.send_message("Only VIPs can use this command.", ephemeral=True)
        return
    global mimic_target
    mimic_target = member.id
    await interaction.response.send_message(f"Now mimicking {member.mention} silently.", ephemeral=True)

# /stopmimic - VIPs ONLY
@bot.tree.command(name="stopmimic", description="Stop mimicking (VIPs only)")
async def stopmimic(interaction: discord.Interaction):
    if not (interaction.user.id == OWNER_ID or interaction.user.id in VIP_IDS):
        await interaction.response.send_message("Only VIPs can use this command.", ephemeral=True)
        return
    global mimic_target
    mimic_target = None
    await interaction.response.send_message("Mimic stopped.", ephemeral=True)

# /autoreact - VIPs ONLY
@bot.tree.command(name="autoreact", description="Auto-react to a user's messages (VIPs only)")
async def autoreact(interaction: discord.Interaction, member: discord.Member, emoji: str):
    if not (interaction.user.id == OWNER_ID or interaction.user.id in VIP_IDS):
        await interaction.response.send_message("Only VIPs can use this command.", ephemeral=True)
        return
    global autoreact_targets
    autoreact_targets[member.id] = emoji
    await interaction.response.send_message(f"Auto-react set for {member.mention} with {emoji}.", ephemeral=True)

# /stopautoreact - VIPs ONLY
@bot.tree.command(name="stopautoreact", description="Stop auto-react for a user (VIPs only)")
async def stopautoreact(interaction: discord.Interaction, member: discord.Member):
    if not (interaction.user.id == OWNER_ID or interaction.user.id in VIP_IDS):
        await interaction.response.send_message("Only VIPs can use this command.", ephemeral=True)
        return
    global autoreact_targets
    if member.id in autoreact_targets:
        del autoreact_targets[member.id]
        await interaction.response.send_message(f"Auto-react stopped for {member.mention}.", ephemeral=True)
    else:
        await interaction.response.send_message(f"No auto-react set for {member.mention}.", ephemeral=True)

# Run bot in background thread
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
