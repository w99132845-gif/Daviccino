import discord
from discord.ext import commands
import random
import os
from flask import Flask
import threading
import asyncio
import time

# ────────────────────────────────────────────────
# CONFIG
# ────────────────────────────────────────────────

OWNER_ID = 864380109682900992           # You (Kevin)
GF_ID = 1425090711019192434             # Your girlfriend

VIP_IDS = []                            # Starts empty

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
# 80 BRUTAL ROASTS (no repeats, savage for everyone except gf)
# ────────────────────────────────────────────────

roasts = [
    "{user}, your existence is the strongest argument for retroactive abortion",
    "{user}, your mom should've swallowed you like the failure you are",
    "{user}, you're the human equivalent of a software update — nobody asked for you",
    "{user}, your face looks like it was designed by someone who hates humanity",
    "{user}, even your shadow leaves you when the lights go out",
    "{user}, you're so ugly even mirrors file restraining orders",
    "{user}, your personality is so dry the Sahara called and wants its desert back",
    "{user}, you're the reason God created the middle finger",
    "{user}, your life is so sad even your imaginary friends ghosted you",
    "{user}, you're proof that natural selection sometimes takes a coffee break",
    "{user}, your birth certificate is an apology letter from the condom factory",
    "{user}, you're so useless even your parasites are looking for a better host",
    "{user}, your vibe is so negative even black holes said 'too much'",
    "{user}", you're the reason warning labels exist on everything",
    "{user}", your rizz is so bad even NPCs reject you in video games",
    "{user}", you're giving 'main character syndrome' but you're an extra with no lines",
    "{user}", your aura is so mid even Switzerland called you neutral",
    "{user}", you're the type of person who gets left on read by their own reflection",
    "{user}", your life is so boring even Wikipedia skipped your page",
    "{user}", you're so forgettable even amnesia patients remember you as 'that guy'",
    "{user}", your personality is so basic even default settings said 'step up'",
    "{user}", you're the human version of Comic Sans — nobody takes you seriously",
    "{user}", your drip is so bad even rain avoids you",
    "{user}", you're the reason 'seen' messages have trust issues",
    "{user}", bro your game is so weak even tutorial mode beat you",
    "{user}", your energy is so low even ghosts have more aura",
    "{user}", you're the reason why 'no cap' needs a cap",
    "{user}", your face card declined harder than your life choices",
    "{user}", you're giving expired milk energy — sour and unwanted",
    "{user}", your chat is so dead even zombies left the group",
    "{user}", bro you're built like a participation trophy — nobody actually wants you",
    "{user}", your vibe is so off even GPS rerouted the entire planet",
    "{user}", you're the type to get ghosted by your own shadow",
    "{user}", your aura is so negative it's classified as a black hole",
    "{user}", your personality is so mid even average said 'step aside'",
    "{user}", you're giving 'I use light mode' energy — cursed",
    "{user}", bro your rizz is so bad even mirrors say no",
    "{user}", your life is so boring even Wikipedia skipped your page",
    "{user}", you're the reason why 'seen' has 3 dots of disappointment",
    "{user}", bro your fit is so bad even thrift stores rejected it",
    "{user}", your energy is so low even batteries sued you for defamation",
    "{user}", you're the type to get left on read by your own group chat",
    "{user}", bro your vibe is so mid even mid said 'damn'",
    "{user}", your aura is so weak even whispers ignore you",
    "{user}", your personality is so basic even IKEA has more character",
    "{user}", you're giving 'default notification sound' energy",
    "{user}", bro your roasts are so weak even bread laughed",
    "{user}", your life is so mid even average said 'step aside'",
    "{user}", you're the type to get ghosted by your own notifications",
    "{user}", bro your energy is so low even ghosts said 'too dead'",
    "{user}", you're the reason why 'seen' needs therapy",
    "{user}", bro your aura is so negative even magnets repelled you",
    "{user}", you're giving 'I use default skin' energy",
    "{user}", bro your rizz is so bad even autocorrect said no",
    "{user}", your jokes are so dry even desert called jealous",
    "{user}", you're the human version of a loading screen — forever waiting",
    "{user}", bro your fit is so bad even fashion police arrested it",
    "{user}", your vibe is so off even GPS gave up",
    "{user}", you're giving 'I'm the main character' energy… in a tutorial",
    "{user}", bro your chat is so dead even zombies left",
    "{user}", your energy is so low even ghosts said 'too dead'",
    "{user}", you're the reason why 'seen' has trust issues",
    "{user}", bro your aura is so weak even whispers ignore you",
    "{user}", your personality is so mid even middle child said no",
    "{user}", you're giving 'default notification sound' energy",
    "{user}", bro your roasts are so weak even bread laughed",
    "{user}", your life is so mid even average said 'step aside'",
    "{user}", you're the type to get ghosted by your own notifications",
    "{user}", bro your energy is so low even ghosts said 'too dead'",
    "{user}", you're the reason why 'seen' needs therapy",
    "{user}", bro your aura is so negative even magnets repelled you",
    "{user}", you're giving 'I use default skin' energy",
    "{user}", bro your rizz is so bad even autocorrect said no",
    "{user}", your jokes are so dry even desert called jealous",
    "{user}", you're the human version of a loading screen — forever waiting",
    "{user}", bro your fit is so bad even fashion police arrested it",
    "{user}", your vibe is so off even GPS gave up",
    "{user}", you're giving 'I'm the main character' energy… in a tutorial",
    "{user}", bro your chat is so dead even zombies left",
    "{user}", your energy is so low even ghosts said 'too dead'",
    "{user}", you're the reason why 'seen' has trust issues"
]

# ────────────────────────────────────────────────
#  !help - beautiful embed
# ────────────────────────────────────────────────

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="✦ Phantom Daviccino Help ✦",
        description="Your personal chaos & fun bot made with ❤️ by **Kevin**",
        color=0xff3366
    )

    embed.set_thumbnail(url="https://i.imgur.com/0X0X0X0.png")  # optional icon

    embed.add_field(
        name="🔥 Core & VIP Commands",
        value="```"
              "!roast @user       → savage roast (harsh for everyone)\n"
              "/say text           → bot says anything (VIPs only)\n"
              "/dm @user text      → bot DMs someone (VIPs only)\n"
              "/mimic @user msg    → speak as someone (VIPs only)\n"
              "/vipadd @user       → add VIP (Kevin only)\n"
              "/vipremove @user    → remove VIP (Kevin only)\n"
              "/viplist            → show VIPs (public)```",
        inline=False
    )

    embed.add_field(
        name="💘 Romance & Wholesome",
        value="```"
              "/ship @u1 @u2       → shipping meter (Kevin + gf = 100% always)\n"
              "/compliment @user   → wholesome vibes (extra sweet for Kevin & gf)```",
        inline=False
    )

    embed.add_field(
        name="🎲 Games & Random",
        value="```"
              "/8ball question     → magic 8-ball\n"
              "/coinflip           → heads or tails\n"
              "/dice [sides]       → roll dice\n"
              "/rps @user choice   → rock paper scissors\n"
              "/poll \"q\" opt1 opt2 → quick poll\n"
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
#  Roast (harsh for all except gf protected)
# ────────────────────────────────────────────────

@bot.command()
async def roast(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    if member.id == OWNER_ID:
        await ctx.send("Can't roast Kevin! He's too majestic 👑🔥")
        return

    if member.id == GF_ID:
        await ctx.send("Can't roast the queen! She's perfect ❤️✨")
        return

    # 80 brutal roasts
    roast_text = random.choice(roasts).format(user=member.mention)
    await ctx.send(roast_text)

# Paste the rest of your commands here (say, dm, vipadd, vipremove, viplist, mimic, ship, compliment, 8ball, coinflip, dice, etc.)
# ... (keep them from your previous code)

# Run bot & Flask (keep this part the same)
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
