import discord
from discord.ext import commands
import random
import os
from flask import Flask
import threading
import asyncio
import time
from datetime import datetime

OWNER_ID = 864380109682900992
GF_ID = 1425090711019192434

VIP_IDS = []

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

STATUSES = [
    discord.Game(name="Daviccino Daddy 🔥"),
    discord.Game(name="Ohh kevin de brunye ⚽️"),
    discord.Game(name="Listening to Albert Fish")
]

afk_users = {}  # {user_id: (reason, timestamp)}

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
    await bot.tree.sync(guild=None)
    print("Global slash commands synced!")

def is_vip(interaction):
    return interaction.user.id == OWNER_ID or interaction.user.id in VIP_IDS

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
    "{user}, you're the reason warning labels exist on everything",
    "{user}, your rizz is so bad even NPCs reject you in video games",
    "{user}, you're giving 'main character syndrome' but you're an extra with no lines",
    "{user}, your aura is so mid even Switzerland called you neutral",
    "{user}, you're the type of person who gets left on read by your own reflection",
    "{user}, your life is so boring even Wikipedia skipped your page",
    "{user}, you're so forgettable even amnesia patients remember you as 'that guy'",
    "{user}, your personality is so basic even default settings said 'step up'",
    "{user}, you're the human version of Comic Sans — nobody takes you seriously",
    "{user}, your drip is so bad even rain avoids you",
    "{user}, you're the reason 'seen' messages have trust issues",
    "{user}, bro your game is so weak even tutorial mode beat you",
    "{user}, your energy is so low even ghosts have more aura",
    "{user}, you're the reason why 'no cap' needs a cap",
    "{user}, your face card declined harder than your life choices",
    "{user}, you're giving expired milk energy — sour and unwanted",
    "{user}, your chat is so dead even zombies left the group",
    "{user}, bro you're built like a participation trophy — nobody actually wants you",
    "{user}, your vibe is so off even GPS rerouted the entire planet",
    "{user}, you're the type to get ghosted by your own shadow",
    "{user}, your aura is so negative it's classified as a black hole",
    "{user}, your personality is so mid even average said 'step aside'",
    "{user}, you're giving 'I use light mode' energy — cursed",
    "{user}, bro your rizz is so bad even mirrors say no",
    "{user}, your life is so boring even Wikipedia skipped your page",
    "{user}, you're the reason why 'seen' has 3 dots of disappointment",
    "{user}, bro your fit is so bad even thrift stores rejected it",
    "{user}, your energy is so low even batteries sued you for defamation",
    "{user}, you're the type to get left on read by your own group chat",
    "{user}, bro your vibe is so mid even mid said 'damn'",
    "{user}, your aura is so weak even whispers ignore you",
    "{user}, your personality is so basic even IKEA has more character",
    "{user}, you're giving 'default notification sound' energy",
    "{user}, bro your roasts are so weak even bread laughed",
    "{user}, your life is so mid even average said 'step aside'",
    "{user}, you're the type to get ghosted by your own notifications",
    "{user}, bro your energy is so low even ghosts said 'too dead'",
    "{user}, you're the reason why 'seen' needs therapy",
    "{user}, bro your aura is so negative even magnets repelled you",
    "{user}, you're giving 'I use default skin' energy",
    "{user}, bro your rizz is so bad even autocorrect said no",
    "{user}, your jokes are so dry even desert called jealous",
    "{user}, you're the human version of a loading screen — forever waiting",
    "{user}, bro your fit is so bad even fashion police arrested it",
    "{user}, your vibe is so off even GPS gave up",
    "{user}, you're giving 'I'm the main character' energy… in a tutorial",
    "{user}, bro your chat is so dead even zombies left",
    "{user}, your energy is so low even ghosts said 'too dead'",
    "{user}, you're the reason why 'seen' has trust issues",
    "{user}, bro your aura is so weak even whispers ignore you",
    "{user}, your personality is so mid even middle child said no"
]

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Only reply when bot is directly mentioned (no reply to replies)
    if bot.user in message.mentions and not message.reference:
        embed = discord.Embed(
            title="✦ Phantom Daviccino Help ✦",
            description="Chaos, fun & love bot",
            color=0xff3366
        )

        embed.set_thumbnail(url="https://i.imgur.com/7L0fK9L.png")

        embed.add_field(
            name="🔥 Core & VIP Commands",
            value="```"
                  "!roast @user       → savage roast\n"
                  "/say text           → bot says anything (VIPs only)\n"
                  "/dm @user text      → bot DMs someone (VIPs only)\n"
                  "/mimic @user msg    → speak as someone (VIPs only)\n"
                  "/vipadd @user       → add VIP (owner only)\n"
                  "/vipremove @user    → remove VIP (owner only)\n"
                  "/viplist            → show VIPs (public)```",
            inline=False
        )

        embed.add_field(
            name="💘 Fun & Games",
            value="```"
                  "/ship @u1 @u2       → shipping meter\n"
                  "/compliment @user   → wholesome vibes\n"
                  "/8ball question     → magic 8-ball\n"
                  "/coinflip           → heads or tails\n"
                  "/dice [sides]       → roll dice\n"
                  "/rps @user choice   → rock paper scissors\n"
                  "/poll \"q\" opts     → quick poll\n"
                  "/wouldyourather A OR B → would you rather\n"
                  "/truth              → random truth question\n"
                  "/dare               → random dare\n"
                  "/randomfact         → random useless fact\n"
                  "/rate @user/thing   → rate out of 10\n"
                  "/hug /slap /bonk @user → fun reactions```",
            inline=False
        )

        embed.set_footer(text="Made by Kevin • Phantom Daviccino 🔥 • 2026")
        embed.timestamp = discord.utils.utcnow()

        await message.channel.send(embed=embed)

    await bot.process_commands(message)

@bot.command(name="help")
async def help_command(ctx):
    embed = discord.Embed(
        title="✦ Phantom Daviccino Help ✦",
        description="Chaos, fun & love bot",
        color=0xff3366
    )

    embed.set_thumbnail(url="https://i.imgur.com/7L0fK9L.png")

    embed.add_field(
        name="🔥 Core & VIP Commands",
        value="```"
              "!roast @user       → savage roast\n"
              "/say text           → bot says anything (VIPs only)\n"
              "/dm @user text      → bot DMs someone (VIPs only)\n"
              "/mimic @user msg    → speak as someone (VIPs only)\n"
              "/vipadd @user       → add VIP (owner only)\n"
              "/vipremove @user    → remove VIP (owner only)\n"
              "/viplist            → show VIPs (public)```",
        inline=False
    )

    embed.add_field(
        name="💘 Fun & Games",
        value="```"
              "/ship @u1 @u2       → shipping meter\n"
              "/compliment @user   → wholesome vibes\n"
              "/8ball question     → magic 8-ball\n"
              "/coinflip           → heads or tails\n"
              "/dice [sides]       → roll dice\n"
              "/rps @user choice   → rock paper scissors\n"
              "/poll \"q\" opts     → quick poll\n"
              "/wouldyourather A OR B → would you rather\n"
              "/truth              → random truth question\n"
              "/dare               → random dare\n"
              "/randomfact         → random useless fact\n"
              "/rate @user/thing   → rate out of 10\n"
              "/hug /slap /bonk @user → fun reactions```",
        inline=False
    )

    embed.set_footer(text="Made by Kevin • Phantom Daviccino 🔥 • 2026")
    embed.timestamp = discord.utils.utcnow()

    await ctx.send(embed=embed)

@bot.command()
async def roast(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    if member.id == OWNER_ID or member.id == GF_ID:
        await ctx.send("Can't roast that user!")
        return

    roast_text = random.choice(roasts).format(user=member.mention)

    embed = discord.Embed(
        title="🔥 Roast Incoming",
        description=roast_text,
        color=0xff0000
    )
    embed.set_image(url="https://i.imgur.com/QJ0oO.gif")  # working crying Jordan
    await ctx.send(embed=embed)

@bot.tree.command(name="mimic", description="Send message as another user (VIPs only)")
async def mimic(interaction: discord.Interaction, member: discord.Member, message: str):
    if not is_vip(interaction):
        await interaction.response.send_message("Only VIPs can use this.", ephemeral=True)
        return

    if member.id == OWNER_ID:
        await interaction.response.send_message("Can't mimic that user!", ephemeral=True)
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

@bot.tree.command(name="say", description="Bot says something (VIPs only)")
async def say(interaction: discord.Interaction, text: str):
    if not is_vip(interaction):
        await interaction.response.send_message("Only VIPs can use this.", ephemeral=True)
        return
    await interaction.channel.send(text)
    await interaction.response.send_message("Sent.", ephemeral=True)

@bot.tree.command(name="dm", description="Send DM to user (VIPs only)")
async def dm(interaction: discord.Interaction, member: discord.Member, text: str):
    if not is_vip(interaction):
        await interaction.response.send_message("Only VIPs can use this.", ephemeral=True)
        return

    try:
        await member.send(text)
        await interaction.response.send_message(f"DM sent to {member.mention}.", ephemeral=True)
    except:
        await interaction.response.send_message(f"Failed to DM {member.mention} (DMs closed?).", ephemeral=True)

@bot.tree.command(name="viplist", description="Show VIP list (public)")
async def viplist(interaction: discord.Interaction):
    if not VIP_IDS:
        await interaction.response.send_message("No VIPs yet! 👑", ephemeral=False)
        return

    mentions = [f"<@{uid}>" for uid in VIP_IDS]
    await interaction.response.send_message(f"**VIPs:** 👑\n" + "\n".join(mentions), ephemeral=False)

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

@bot.tree.command(name="ship", description="Ship two people")
async def ship(interaction: discord.Interaction, user1: discord.Member, user2: discord.Member = None):
    if user2 is None:
        user2 = user1
        user1 = interaction.user

    u1, u2 = user1.id, user2.id

    if (u1 == OWNER_ID and u2 == GF_ID) or (u1 == GF_ID and u2 == OWNER_ID):
        percentage = 100
        comment = "Perfect match! Power couple vibes 🔥❤️"
    elif OWNER_ID in (u1, u2) or GF_ID in (u1, u2):
        percentage = random.randint(0, 5)
        comment = "Nah... not happening. Chemistry = 404 💀"
    else:
        percentage = random.randint(0, 100)
        if percentage >= 90:
            comment = "Soulmates fr 🔥"
        elif percentage >= 70:
            comment = "Solid vibes ❤️"
        elif percentage >= 40:
            comment = "Mid ship ngl 😭"
        else:
            comment = "Divorce speedrun any% 💀"

    embed = discord.Embed(
        title="💘 Shipping Meter",
        description=f"{user1.mention} x {user2.mention}\n**{percentage}%** {comment}",
        color=discord.Color.green() if percentage >= 70 else discord.Color.red()
    )
    embed.set_thumbnail(url="https://i.imgur.com/heart.png")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="compliment", description="Give someone a compliment")
async def compliment(interaction: discord.Interaction, member: discord.Member):
    replies = [
        "You're actually kinda cool ngl.",
        "Your aura is lowkey fire today.",
        "You're giving main character energy fr.",
        "Bro you're underrated, keep shining."
    ]
    embed = discord.Embed(
        description=random.choice(replies),
        color=0x00ff00
    )
    embed.set_thumbnail(url="https://i.imgur.com/smile.png")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="8ball", description="Ask the magic 8-ball")
async def eightball(interaction: discord.Interaction, question: str):
    replies = [
        "Yes, facts.",
        "Nah, cope.",
        "100% happening.",
        "Signs point to no",
        "Ask again later.",
        "Definitely not.",
        "Outlook good.",
        "My sources say no.",
        "Yes, but touch grass first.",
        "Reply hazy, try again."
    ]
    embed = discord.Embed(
        title="🎱 Magic 8-Ball",
        description=f"**Question:** {question}\n**Answer:** {random.choice(replies)}",
        color=0x0000ff
    )
    embed.set_thumbnail(url="https://i.imgur.com/8ball.png")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="coinflip", description="Flip a coin")
async def coinflip(interaction: discord.Interaction):
    result = random.choice(["Heads 🪙", "Tails 🪙"])
    embed = discord.Embed(
        description=f"Coinflip: **{result}**",
        color=0xffff00
    )
    embed.set_thumbnail(url="https://i.imgur.com/coin.png")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="dice", description="Roll a die (default 6)")
async def dice(interaction: discord.Interaction, sides: int = 6):
    if sides < 2:
        sides = 6
    result = random.randint(1, sides)
    embed = discord.Embed(
        description=f"🎲 Rolled **{sides}-sided die**: **{result}**",
        color=0xff9900
    )
    embed.set_thumbnail(url="https://i.imgur.com/dice.png")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="rps", description="Play rock paper scissors")
async def rps(interaction: discord.Interaction, member: discord.Member, choice: str):
    choices = ["rock", "paper", "scissors"]
    if choice.lower() not in choices:
        await interaction.response.send_message("Choose rock, paper, or scissors!", ephemeral=True)
        return

    bot_choice = random.choice(choices)
    result = "Tie!" if choice.lower() == bot_choice else (
        "You win!" if (choice.lower() == "rock" and bot_choice == "scissors") or
                       (choice.lower() == "paper" and bot_choice == "rock") or
                       (choice.lower() == "scissors" and bot_choice == "paper") else "You lose!"
    )

    embed = discord.Embed(
        description=f"You chose **{choice}**\nI chose **{bot_choice}**\n**{result}**",
        color=0x00ccff
    )
    embed.set_thumbnail(url="https://i.imgur.com/rps.png")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="poll", description="Create a quick poll")
async def poll(interaction: discord.Interaction, question: str, option1: str, option2: str, option3: str = None, option4: str = None):
    embed = discord.Embed(title="📊 Poll", description=question, color=discord.Color.blue())
    embed.add_field(name="1️⃣", value=option1, inline=False)
    embed.add_field(name="2️⃣", value=option2, inline=False)
    if option3:
        embed.add_field(name="3️⃣", value=option3, inline=False)
    if option4:
        embed.add_field(name="4️⃣", value=option4, inline=False)
    embed.set_thumbnail(url="https://i.imgur.com/poll.png")

    msg = await interaction.response.send_message(embed=embed)
    await msg.add_reaction("1️⃣")
    await msg.add_reaction("2️⃣")
    if option3:
        await msg.add_reaction("3️⃣")
    if option4:
        await msg.add_reaction("4️⃣")

@bot.tree.command(name="wouldyourather", description="Would you rather")
async def wouldyourather(interaction: discord.Interaction, option1: str, option2: str):
    embed = discord.Embed(title="🤔 Would You Rather", color=0x9933ff)
    embed.add_field(name="Option A", value=option1, inline=False)
    embed.add_field(name="Option B", value=option2, inline=False)
    embed.set_thumbnail(url="https://i.imgur.com/question.png")
    msg = await interaction.response.send_message(embed=embed)
    await msg.add_reaction("🇦")
    await msg.add_reaction("🇧")

@bot.tree.command(name="truth", description="Get a random truth question")
async def truth(interaction: discord.Interaction):
    truths = [
        "What's the most embarrassing thing you've ever done?",
        "Who was your first crush and why?",
        "What's the weirdest food combo you've tried?",
        "Have you ever lied to get out of trouble?",
        "What's your biggest fear right now?",
        "Who's the last person you stalked on social media?",
        "What's the dumbest thing you've done for a dare?",
        "Have you ever had a crush on a teacher?",
        "What's the most illegal thing you've ever done?",
        "Who in this server would you date if you had to pick?"
    ]
    embed = discord.Embed(
        description=f"Truth: **{random.choice(truths)}**",
        color=0x9933ff
    )
    embed.set_thumbnail(url="https://i.imgur.com/truth.png")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="dare", description="Get a random dare")
async def dare(interaction: discord.Interaction):
    dares = [
        "Send your last selfie in general chat",
        "Type 'I'm a potato' in 5 different channels",
        "Change your nickname to 'Daddy' for 10 minutes",
        "Send 'I love you' to the last person you DM'd",
        "Post 'Rate my fit' with your current pfp",
        "Sing the chorus of your current favorite song in VC",
        "Send a voice message saying 'I'm gay'",
        "DM the person above you 'You're cute'",
        "React with 😂 to the last 10 messages in general",
        "Post 'Who wants to date me?' in general chat"
    ]
    embed = discord.Embed(
        description=f"Dare: **{random.choice(dares)}**",
        color=0xff66cc
    )
    embed.set_thumbnail(url="https://i.imgur.com/dare.png")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="randomfact", description="Get a random useless fact")
async def randomfact(interaction: discord.Interaction):
    facts = [
        "A flock of crows is called a murder.",
        "Octopuses have three hearts.",
        "Bananas are berries, but strawberries aren't.",
        "The unicorn is the national animal of Scotland.",
        "Honey never spoils.",
        "A group of flamingos is called a flamboyance.",
        "Wombat poop is cube-shaped.",
        "The shortest war in history lasted 38 minutes.",
        "The Eiffel Tower can be 15 cm taller during the summer.",
        "A shrimp's heart is in its head."
    ]
    embed = discord.Embed(
        description=f"Random fact: {random.choice(facts)}",
        color=0xffff00
    )
    embed.set_thumbnail(url="https://i.imgur.com/fact.png")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="rate", description="Rate someone or something out of 10")
async def rate(interaction: discord.Interaction, thing: str):
    score = random.randint(0, 10)
    comments = [
        f"{score}/10 - mid af",
        f"{score}/10 - fire ngl",
        f"{score}/10 - trash",
        f"{score}/10 - peak"
    ]
    embed = discord.Embed(
        description=f"{thing}: **{random.choice(comments)}**",
        color=0xffcc00
    )
    embed.set_thumbnail(url="https://i.imgur.com/stars.png")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="hug", description="Hug someone")
async def hug(interaction: discord.Interaction, member: discord.Member):
    embed = discord.Embed(
        description=f"{interaction.user.mention} hugged {member.mention} 🤗",
        color=0xff69b4
    )
    embed.set_image(url="https://i.imgur.com/hug.gif")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="slap", description="Slap someone")
async def slap(interaction: discord.Interaction, member: discord.Member):
    embed = discord.Embed(
        description=f"{interaction.user.mention} slapped {member.mention} 👋",
        color=0xff0000
    )
    embed.set_image(url="https://i.imgur.com/slap.gif")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="bonk", description="Bonk someone")
async def bonk(interaction: discord.Interaction, member: discord.Member):
    embed = discord.Embed(
        description=f"{interaction.user.mention} bonked {member.mention} 🔨",
        color=0x8b4513
    )
    embed.set_image(url="https://i.imgur.com/bonk.gif")
    await interaction.response.send_message(embed=embed)

@bot.command()
async def afk(ctx, *, reason="AFK"):
    if ctx.author.id in afk_users:
        await ctx.send("You're already AFK!")
        return

    afk_users[ctx.author.id] = (reason, time.time())
    embed = discord.Embed(
        title="AFK Status",
        description=f"{ctx.author.mention} is now AFK\n**Reason:** {reason}",
        color=0x808080
    )
    embed.set_thumbnail(url="https://i.imgur.com/grayafk.png")
    await ctx.send(embed=embed)

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
