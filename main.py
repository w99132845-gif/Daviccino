import discord
from discord.ext import commands
import random
import os
from flask import Flask
import threading
import asyncio
import time

# OWNER (Kevin)
OWNER_ID = 864380109682900992

# GF ID
GF_ID = 1425090711019192434

# VIP list - starts empty
VIP_IDS = []

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Rotating DND status every 5 seconds
STATUSES = [
    discord.Game(name="Daviccino Daddy 🔥"),
    discord.Game(name="Ohh kevin de brunye ⚽️"),
    discord.Game(name="Listening to Albert Fish")
]

async def rotate_status():
    i = 0
    while True:
        await bot.change_presence(status=discord.Status.dnd, activity=STATUSES[i])
        i = (i + 1) % len(STATUSES)
        await asyncio.sleep(5)

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")
    bot.loop.create_task(rotate_status())
    await bot.tree.sync()
    print("Slash commands synced!")

# Helper: is VIP or Kevin?
def is_vip(interaction):
    return interaction.user.id == OWNER_ID or interaction.user.id in VIP_IDS

# ────────────────────────────────────────────────
#  !help - beautiful embed
# ────────────────────────────────────────────────

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="✦ Phantom Daviccino Help ✦",
        description="Chaos, fun & love bot made with ❤️ by **Kevin**",
        color=0xff3366
    )

    embed.set_thumbnail(url="https://i.imgur.com/0X0X0X0.png")  # optional cool icon

    embed.add_field(
        name="🔥 Core & VIP Commands",
        value="```"
              "!roast @user       → savage roast (harsh for normies, soft for VIPs)\n"
              "/say text           → bot says anything (VIPs only)\n"
              "/dm @user text      → bot DMs someone (VIPs only)\n"
              "/mimic @user msg    → speak as someone (VIPs only)\n"
              "/vipadd /vipremove  → manage VIPs (Kevin only)\n"
              "/viplist            → show VIPs (public)```",
        inline=False
    )

    embed.add_field(
        name="💘 Romance & Wholesome",
        value="```"
              "/ship @u1 @u2       → shipping meter (Kevin + gf = 100%)\n"
              "/compliment @user   → wholesome vibes (extra sweet for Kevin & gf)```",
        inline=False
    )

    embed.add_field(
        name="🎲 Games & Fun",
        value="```"
              "/8ball question     → magic 8-ball\n"
              "/coinflip           → heads/tails\n"
              "/dice [sides]       → roll dice\n"
              "/rps @user choice   → rock paper scissors\n"
              "/poll \"q\" opts     → quick poll\n"
              "/wouldyourather A OR B → would you rather\n"
              "/truth /dare        → party game\n"
              "/rate @user/thing   → rate out of 10\n"
              "/hug /slap /bonk @user → fun reactions```",
        inline=False
    )

    embed.set_footer(text="Made by Kevin • Phantom Daviccino 🔥 • 2026")
    embed.timestamp = discord.utils.utcnow()

    await ctx.send(embed=embed)

# ────────────────────────────────────────────────
#  Mimic (VIPs only)
# ────────────────────────────────────────────────

@bot.tree.command(name="mimic", description="Send message as another user (VIPs only)")
async def mimic(interaction: discord.Interaction, member: discord.Member, message: str):
    if not is_vip(interaction):
        await interaction.response.send_message("Only VIPs can use this.", ephemeral=True)
        return

    if member.id == OWNER_ID:
        await interaction.response.send_message("Can't mimic Kevin!", ephemeral=True)
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

# ────────────────────────────────────────────────
#  Roast (anyone)
# ────────────────────────────────────────────────

@bot.command()
async def roast(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    if member.id == OWNER_ID:
        await ctx.send("Can't roast Kevin! He's too majestic 👑🔥")
        return

    harsh = [ ... ]  # your 80 harsh roasts (copy from previous messages)
    light = [ ... ]  # your 80 light roasts

    if member.id in VIP_IDS:
        roast_text = random.choice(light).format(user=member.mention)
    else:
        roast_text = random.choice(harsh).format(user=member.mention)

    await ctx.send(roast_text)

# ────────────────────────────────────────────────
#  Ship (special for Kevin + gf)
# ────────────────────────────────────────────────

@bot.tree.command(name="ship", description="Ship two people (Kevin + gf = 100%)")
async def ship(interaction: discord.Interaction, user1: discord.Member, user2: discord.Member = None):
    if user2 is None:
        user2 = user1
        user1 = interaction.user

    u1, u2 = user1.id, user2.id

    if (u1 == OWNER_ID and u2 == GF_ID) or (u1 == GF_ID and u2 == OWNER_ID):
        percentage = 100
        comment = "PERFECT MATCH! Power couple supreme 🔥❤️👑 Kevin & his queen forever"
    elif OWNER_ID in (u1, u2) or GF_ID in (u1, u2):
        percentage = random.randint(0, 5)
        comment = "Nahhh... not happening. Chemistry = 404 💀"
    else:
        percentage = random.randint(0, 100)
        if percentage >= 90:
            comment = "Soulmates fr 🔥"
        elif percentage >= 70:
            comment = "Solid couple vibes ❤️"
        elif percentage >= 40:
            comment = "Mid ship ngl 😭"
        else:
            comment = "Divorce speedrun any% 💀"

    embed = discord.Embed(
        title="💘 Shipping Meter",
        description=f"{user1.mention} x {user2.mention}\n**{percentage}%** {comment}",
        color=discord.Color.green() if percentage >= 70 else discord.Color.red()
    )
    await interaction.response.send_message(embed=embed)

# ────────────────────────────────────────────────
#  Compliment (extra sweet for Kevin & gf)
# ────────────────────────────────────────────────

@bot.tree.command(name="compliment", description="Give someone a compliment")
async def compliment(interaction: discord.Interaction, member: discord.Member):
    if member.id == OWNER_ID:
        replies = [
            "Kevin is literally the king of aura 👑🔥",
            "The man, the myth, the Daviccino legend ❤️",
            "Kevin's rizz is unmatched, respect fr.",
            "You're built different, Kevin — everyone knows it."
        ]
    elif member.id == GF_ID:
        replies = [
            "Queen energy! Prettiest & sweetest in the server ❤️✨",
            "She's literally perfect, no notes.",
            "The vibe is immaculate, goddess fr.",
            "Kevin's gf is a 12/10, he's lucky king."
        ]
    else:
        replies = [
            "You're actually kinda cool ngl.",
            "Your aura is lowkey fire today.",
            "You're giving main character energy fr.",
            "Bro you're underrated, keep shining."
        ]

    await interaction.response.send_message(random.choice(replies))

# ────────────────────────────────────────────────
#  8-Ball
# ────────────────────────────────────────────────

@bot.tree.command(name="8ball", description="Ask the magic 8-ball")
async def eightball(interaction: discord.Interaction, question: str):
    replies = [
        "Yes king, facts.",
        "Nah bro, cope.",
        "100% happening fr.",
        "Signs point to no 💀",
        "Ask again later, I'm busy.",
        "Definitely not.",
        "Outlook good, trust.",
        "My sources say no.",
        "Yes, but touch grass first.",
        "Reply hazy, try again."
    ]
    await interaction.response.send_message(f"🎱 {question}\n**Answer:** {random.choice(replies)}")

# ────────────────────────────────────────────────
#  Coinflip
# ────────────────────────────────────────────────

@bot.tree.command(name="coinflip", description="Flip a coin")
async def coinflip(interaction: discord.Interaction):
    result = random.choice(["Heads 🪙", "Tails 🪙"])
    await interaction.response.send_message(f"Coinflip: **{result}**")

# ────────────────────────────────────────────────
#  Dice
# ────────────────────────────────────────────────

@bot.tree.command(name="dice", description="Roll a die (default 6)")
async def dice(interaction: discord.Interaction, sides: int = 6):
    if sides < 2:
        sides = 6
    result = random.randint(1, sides)
    await interaction.response.send_message(f"🎲 Rolled **{sides}-sided die**: **{result}**")

# ────────────────────────────────────────────────
#  VIP Commands (kept)
# ────────────────────────────────────────────────

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

@bot.tree.command(name="viplist", description="Show VIP list (public)")
async def viplist(interaction: discord.Interaction):
    if not VIP_IDS:
        await interaction.response.send_message("No VIPs yet! 👑", ephemeral=False)
        return

    mentions = [f"<@{uid}>" for uid in VIP_IDS]
    await interaction.response.send_message(f"**VIPs:** 👑\n" + "\n".join(mentions), ephemeral=False)

# ────────────────────────────────────────────────
#  Run bot & Flask
# ────────────────────────────────────────────────

def run_discord_bot():
    time.sleep(5)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bot.start(os.getenv("DISCORD_TOKEN")))

threading.Thread(target=run_discord_bot, daemon=True).start()

app = Flask(__name__)

@app.route("/")
def home():
    return "Phantom Daviccino is alive! 🔥"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
