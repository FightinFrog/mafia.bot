import discord
from discord.ext import commands
import random
TOKEN = 'NzE3NDU5NjU2NzUwMDA2MzE0.XtaooA.3bsf0SoKYVNhOCwh7llJquxPpYs'
bot = commands.Bot(command_prefix='!')
num_maf = 2
fut_cor = 0
num_fir = 1
i = -1
a = []
per_id = []
per_dict = dict()
g = 0
num_day = 0
num_she = 0
num_don = 0
@bot.command(pass_context=True)
async def roles(ctx2, n):
    global a
    global num_maf
    global g
    global num_day
    global num_she
    global per_id
    num_day = 0
    num_she = 0
    n = int(n)
    for j in range(n):
        a.append('Мирный')
    if n == 10 or n == 9:
        a[0] = 'Шериф'
        a[1] = 'Дон'
        a[2] = 'Мафия'
        a[3] = 'Мафия'
        num_maf = 3
    elif n == 8:
        a[0] = 'Шериф'
        a[1] = 'Дон'
        a[2] = 'Мафия'
        num_maf = 2
    else:
        a[0] = 'Дон'
        a[1] = 'Мафия'
        num_maf = 2
    random.shuffle(a)
    g = 0
    per_id = ["0"]*len(a)
    await ctx2.send('Роли готовы, можете разбирать')
@bot.command(pass_context=True)
async def my_role(ctx3):
    global a
    global g
    global per_dict
    await ctx3.author.send(a[g])
    per_dict[ctx3.author.id] = a[g]
    #print(per_dict)
    #print(per_dict.get(ctx3.author.id))
    if g == len(a)-1:
        await ctx3.send('Все роли розданы, можете начинать игру')
    g += 1
@bot.command(pass_context=True)
async def kill(ctx1, arg):
    #await ctx1.channel.purge(limit = 1)
    #print('агась')
    global i
    global fut_cor
    global per_dict
    global num_fir
    if per_dict.get(ctx1.author.id) == 'Мафия' or per_dict.get(ctx1.author.id) == 'Дон':
        i += 1
        if i == 0:
            fut_cor = arg
        else:
            if arg == fut_cor:
                num_fir+=1
    else:
        await ctx1.author.send('Ля ты крыса') 

@bot.command(pass_context=True)
async def day(ctx5):
    # await ctx1.channel.purge(limit = 1)
    # print('агась')
    global i
    global fut_cor
    global num_fir
    global num_day
    global num_don
    global num_she
    num_day += 1
    await ctx5.send('Город просыпается')
    print(num_fir)
    print(num_maf)
    print(fut_cor)
    if num_fir == num_maf:
        print('sdsd')
        await ctx5.send('утро сегодня далеко не доброе, был убит игрок '+fut_cor)
        num_fir = 0
        i = -1
    else:
        await ctx5.send('утро сегодня доброе, в городе несострел')
        num_fir = 0
        i = -1
@bot.command(pass_context=True)
async def voting(ctx4, hanged):
    global a
    global num_maf
    h = int(hanged)
    if a[h-1] == 'Мафия' or a[h-1] == 'Дон':
        num_maf-=1
@bot.command(pass_context=True)
async def sheriff(ctx, arg):
    global a
    global num_day
    global num_she
    global per_dict
    if per_dict.get(ctx.author.id) == 'Шериф':
        if num_she <= num_day:
            if a[int(arg)-1] == 'Мирный':
                await ctx.author.send('Красный')
            else:
                await ctx.author.send('Черный')
            num_she += 1
        else:
            await ctx.author.send('прикольно вторую проверку за ночь делать?')
    else:
        await ctx.author.send('ты кто такой, чтобы шерифскую проверку делать?')
@bot.command(pass_context=True)
async def don(ctx5, arg):
    global a
    global num_day
    global num_don
    global per_dict
    if per_dict.get(ctx5.author.id) == 'Дон':
        if num_don <= num_day:
            if a[int(arg)-1] == 'Шериф':
                await ctx5.author.send('Шериф')
            else:
                await ctx5.author.send('Не шериф')
            num_don+=1
        else:
            await ctx5.author.send('прикольно вторую проверку за ночь делать?')
    else:
        await ctx5.author.send('ты кто такой, чтобы донскую проверку делать?')
bot.run(TOKEN)
