import discord
from discord.ext import commands
import random

class Game:
    def __init__(self):
        self.players = []
        self.roles = []
        self.num_maf = 2
        self.k = 0
        self.num_day = 0
        self.num_sheriff_checks = 0
        self.num_don_checks = 0
        self.fut_cor = None
        self.num_fir = 0

    def assign_roles(self, n):
        self.roles = ['Мирный'] * n
        if n in [9, 10]:
            self.roles[0] = 'Шериф'
            self.roles[1] = 'Дон'
            self.roles[2] = 'Мафия'
            self.roles[3] = 'Мафия'
            self.num_maf = 3
        elif n == 8:
            self.roles[0] = 'Шериф'
            self.roles[1] = 'Дон'
            self.roles[2] = 'Мафия'
            self.num_maf = 2
        elif n == 7:
            self.roles[0] = 'Дон'
            self.roles[1] = 'Мафия'
            self.num_maf = 2
        else:
            return False
        random.shuffle(self.roles)
        return True

    def get_role(self, player_id):
        return self.roles[player_id]

    def next_player(self):
        if self.k < len(self.roles) - 1:
            self.k += 1
            return True
        return False

    def reset_day(self):
        self.num_day += 1
        self.num_fir = 0
        self.k = 0

game_instance = Game()
bot = commands.Bot(command_prefix='!')

@bot.command(pass_context=True)
async def roles(ctx, n: int):
    if game_instance.assign_roles(n):
        await ctx.send('Роли готовы, можете разбирать')
    else:
        await ctx.send('Проверьте количество игроков')

@bot.command(pass_context=True)
async def my_role(ctx):
    player_id = game_instance.k
    role = game_instance.get_role(player_id)
    await ctx.author.send(role)
    game_instance.next_player()
    if game_instance.k == len(game_instance.roles):
        await ctx.send('Все роли розданы, можете начинать игру')

@bot.command(pass_context=True)
async def kill(ctx, arg):
    role = game_instance.get_role(game_instance.k)
    if role in ['Мафия', 'Дон']:
        if game_instance.fut_cor is None:
            game_instance.fut_cor = arg
        elif arg == game_instance.fut_cor:
            game_instance.num_fir += 1
    else:
        await ctx.author.send('Только мафия может выбирать жертву')

@bot.command(pass_context=True)
async def day(ctx):
    game_instance.reset_day()
    await ctx.send('Город просыпается')
    if game_instance.num_fir == game_instance.num_maf:
        await ctx.send(f'Утро сегодня не доброе, был убит игрок {game_instance.fut_cor}')
    else:
        await ctx.send('Утро сегодня доброе, в городе несострел')

@bot.command(pass_context=True)
async def voting(ctx, hanged: int):
    if game_instance.roles[hanged - 1] in ['Мафия', 'Дон']:
        game_instance.num_maf -= 1

@bot.command(pass_context=True)
async def sheriff(ctx, arg: int):
    role = game_instance.get_role(ctx.author.id)
    if role == 'Шериф':
        if game_instance.num_sheriff_checks < game_instance.num_day:
            result = 'Красный' if game_instance.roles[arg - 1] == 'Мирный' else 'Черный'
            await ctx.author.send(result)
            game_instance.num_sheriff_checks += 1
        else:
            await ctx.author.send('Вы можете совершить только 1 проверку')
    else:
        await ctx.author.send('Только шериф может совершать проверку')

@bot.command(pass_context=True)
async def don(ctx, arg: int):
    role = game_instance.get_role(ctx.author.id)
    if role == 'Дон':
        if game_instance.num_don_checks < game_instance.num_day:
            result = 'Шериф' if game_instance.roles[arg - 1] == 'Шериф' else 'Не шериф'
            await ctx.author.send(result)
            game_instance.num_don_checks += 1
        else:
            await ctx.author.send('Вы можете совершить только 1 проверку')
    else:
        await ctx.author.send('Только дон может совершать проверку')


bot.run(TOKEN)
