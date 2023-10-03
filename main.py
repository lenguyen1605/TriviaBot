# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import discord
from decouple import Config
import requests

config = Config('.env')


TOKEN = config.get('DISCORD_TOKEN')
GUILD = 'Ahihi'
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)


def get_questions():
    response = requests.request("GET", 'https://the-trivia-api.com/v2/questions')
    if response.status_code == 200:
        print("success")
        data = response.json()
        print(data)
        return data


questions_set = get_questions()


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            print(f'{guild.name}(id: {guild.id})')
            print("guild users", sum([guild.member_count for guild in bot.guilds]))
            break
    print(f'{bot.user} has connected to discord')
    # print(f'{guild.name}(id: {guild.id})')
    # print("guild users", len(guild.members))


@bot.event
async def on_message(message):
    num_q = 0
    score = 0
    print("message listened")
    print("message content", message.content)
    if message.author == bot.user:
        return
    if message.content == "$hello":
        print("yay")
        await message.channel.send("hey babes")
    if message.content == "$trivia":
        await message.channel.send("Type $answer YOUR ANSWER to answer the questions")
        await message.channel.send(questions_set[0]['question']['text'])
    if message.content.startswith("$answer"):
        ans = message.content[8:].lower()
        print("my ans ", ans)
        print("cor ans ", questions_set[0]['correctAnswer'].lower())
        if ans != questions_set[0]['correctAnswer'].lower():
            await message.channel.send("incorrect!")
        else:
            score += 1
            num_q = num_q + 1
            questions_set.pop(0)
            await message.channel.send("correct!")

            await message.channel.send(questions_set[0]['question']['text'])


bot.run(TOKEN)
