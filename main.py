#  coding: utf-8
import sys, os, time, discord
from discord.ext import commands, tasks
from easy_events import AsyncEvents, Parameters
import asyncio
import threading


version = "0.0.2"
prefix = "-"

with open("bot_token", "r") as f:
    bot_token = f.readlines()[0].strip()


intents = discord.Intents.all()

client = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), intents=intents, activity=discord.Game("Started!"), status=discord.Status.online)
client.remove_command('help')

cmd = AsyncEvents()

base_path = os.getcwd().replace("\\", "/")


help_msg = """
>>> **Commands**

-ver    : show version info
-reboot : restart the bot
-help   : show this message
"""


def convert_time(value):
    val2, val = int(value//60), int(value % 60)
    message = f"{val2}min {val}s."

    if val2 > 60:
        val3, val2 = int(val2//60), int(val2 % 60)
        message = f"{val3}h {val2}min {val}s."

    return message


def is_cmd(ctx):
    return isinstance(ctx, Parameters)


# -----------------------------EVENTS--------------------------------


@client.event
async def on_ready():
    run_cmd.start()

    print("version : ", f"{os.path.basename(sys.argv[0])} {version}")
    print("Logged in as : ", client.user.name)
    print("ID : ", client.user.id)


@client.event
async def on_command_error(ctx,  error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all required arguments')

# -----------------------------COMMANDS----------------------------


timer = time.time()


@client.command(aliases=["version", "ping"])
@cmd.event(aliases=["version", "ping"])
async def ver(ctx):
    text = f"version : {version}\nping : {round(client.latency * 1000)}ms :ping_pong:\ntime up : {convert_time(int(time.time()-timer))}"

    if is_cmd(ctx):
        print(f"\n{text}\n")
        return

    await ctx.send(text)


@client.command(aliases=["help"])
@cmd.event(aliases=["help"])
async def h(ctx):
    if is_cmd(ctx):
        print(help_msg)
        return

    await ctx.send(help_msg)


@client.command()
@cmd.event()
async def reboot(ctx):
    text = "Restarting bot..."
    if is_cmd(ctx):
        print(text)
    else:
        await ctx.send(text)

    await client.change_presence(activity=discord.Game("Shutting down..."), status=discord.Status.dnd)
    os.execv(sys.executable, ["None", os.path.basename(sys.argv[0])])


@tasks.loop(seconds=.5)
async def run_cmd():
    # execute the commands in the waiting list
    await cmd.run_task()


def _inputs():
    time.sleep(4)
    while True:
        command = input("> ")

        if not command:
            continue

        # add command to the waiting list
        cmd.trigger(command)
        time.sleep(.5)


threading.Thread(target=_inputs).start()
client.run(bot_token , log_handler=None)
# code by ThePhoenix78 on GitHub
