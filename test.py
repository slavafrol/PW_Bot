import discord
import mysql.connector
import helper
from discord.ext import commands

db = mysql.connector.connect(host="localhost", port="3300", user="root", password="1234")
db_cursor = db.cursor()
db_cursor.execute("USE pw_test")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = '!', intents=intents)

@bot.event
async def on_ready():
    print("Бот запущен...")
    synced = await bot.tree.sync()

@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    embed = discord.Embed(title=f"Добро пожаловать {member.name}", description=f"Спасибо, что присоединился к {member.guild.name}")
    embed.set_thumbnail(url=member.avatar)
    embed.set_image(url="https://github.com/GalchenkoIurii/cybersport/blob/main/public/images/bg-1.jpg?raw=true")
    await channel.send(embed=embed)
    await member.send(f"Приветствую {member.name}!")

@bot.event
async def on_command_error(ctx, exception):
    if isinstance(exception, commands.PrivateMessageOnly):
        await ctx.send("DM me this command to use it.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    channel = message.channel
    if "?" in message.content:
        ans = helper.detect_question(message.content)
        if ans == None:
            await channel.send("Мой процессор перегрелся, сейчас позову кого-нибудь из человекообразных")
            await bot.get_channel(1075028976717791342).send("Пользователь " + message.author.name + " #" + message.author.discriminator + " задал вопрос:\n\"" + message.content + "\"")
        else:
            await channel.send(ans)
    if helper.to_alpha(message.content.lower()) in helper.greet:
        await channel.send("Привет!") #Сделать рандомизацию ответа?

@bot.event
async def on_raw_reaction_add(payload):
    print(payload.emoji)
    if payload.message_id != 1075033406339022888: #ID сообщения для реакции1075033406339022888
        return
    if payload.emoji.name == '👋':
        await payload.member.send("Привет! Как я могу помочь?")

@bot.tree.command(name="hello", description="Скажи привет боту!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Привет!")

@bot.tree.command(name="application", description="Подать заявку на участие")
async def application(interaction: discord.Interaction):
    data = [interaction.user.id, "Null"]
    channel = interaction.channel
    if channel.guild != None:
        await interaction.response.send_message("Эту команду можно использовать только в личных сообщениях с ботом!")
        return
    user_id = interaction.user.id
    valid_name = False
    initial = True
    while not valid_name:
        if initial:
            await interaction.response.send_message("Напиши свое имя")
        else:
            await channel.send("Имя введено неправильно, попробуй еще раз (пример: Александр)")
        def check(m):
            return channel.id == m.channel.id
        msg = await bot.wait_for("message", check=check)
        if (helper.check_name(msg.content)):
            data[1] = msg.content
            valid_name = True
            initial = True
        else:
            initial = False
        try:
            db_cursor.execute("INSERT INTO users (DiscordID, FirstName) VALUES (%s, %s)", tuple(data))
            db.commit()
        except mysql.connector.IntegrityError as e:
            await channel.send("Пользователь с таким Дискордом уже существует")


bot.run('MTA3MjI3MDkwNzY3MTg0NjkyMg.G9SGMx.n2NESZf_sVZLUqOE4EpeCg6VyAU2DB9MqKA3xc') 