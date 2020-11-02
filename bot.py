import discord
from discord.ext import commands

import sqlite3
from config import settings

from discord.utils import get
import youtube_dl

import os

import json



client = commands.Bot(command_prefix = settings['PREFIX'])
client.remove_command('help')

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

bad_words = ['бля', 'Пидор', 'Хуило', 'Чмошник', 'Уёбище', 'Гавнище', 'Хуйня', 'Дегенерат', 'Пидорище', 'Педик', 'сука', 'долбаеб', 'пидр', 'cyka', 'dolbaeb', 'pidr', 'уебан', 'yeban', 'ебатся', 'ebatsa', 'сучка', 'sychka', 'ИДИ НАХУЙ', 'иди нахуй', 'Сервер говно!', 'Бот говно', 'Кик бота', 'Создатель долбаеб', 'Все здесь лохи', 'Все здесь долбаебы', 'Пидрила', 'Создатель гандон', 'Гандон', 'ГАНДОН']






hellow_words = [ 'hellow Бот', 'hi Бот', 'hellow Bot', 'hi Bot', 'hellow бот', 'hi бот', 'Hellow bot', 'Hi bot', 'Hellow Бот', 'Hi Бот', 'Hellow Bot', 'Hi Bot', 'Hellow бот', 'Hi бот', 'Привет Бот', 'Привет бот', 'привет бот', 'привет Бот']


@client.event

async def on_ready():
    print('Bot connected, you can started')

    await client.change_presence( status = discord.Status.online, activity = discord.Game( '.help' ) )

@client.event
async def on_command_error( ctx, error ):
	pass

#Auto role
@client.event
async def on_member_join( member ):
    channel = client.get_channel( 767971262680924200 )
 
    role = discord.utils.get( member.guild.roles, id = 767828985714573360 )
 
    await member.add_roles( role )
    await channel.send( embed = discord.Embed( description = f'Пользователь ``{ member.name }``, присоеденился к нам!', color = 0x3ec95d ) )

#Вход бота в войс
@client.command()
async def join(ctx):
	global voice
	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild = ctx.guild)

	if voice and voice.is_connected():
		await voice.move_to(channel)
	else:
		voice = await channel.connect()
		await ctx.send(f'Бот присоеделился к каналу {channel}')

#Выход из войса
@client.command()
async def leave(ctx):
	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild = ctx.guild)

	if voice and voice.is_connected():
		await voice.disconnect()
	else:
		voice = await connect.channel()
		await ctx.send(f'Бот отключился от канала {channel}')

#общение бота
@client.event

async def on_message( message ):
	msg1 = message.content.lower()

	if msg1 in hellow_words:
	    await message.channel.send( 'Здравствуйте! Вам чтонибудь нужно?' )
#фильтр
@client.event
async def on_message( message ):
	await client.process_commands( message )

	msg = message.content.lower()

	if msg in bad_words:
		await message.delete()
		await message.author.send( f'{ message.author.name }, не нужно так писать в чат! Если вы продолжите то получите мут или еще хуже БАН ' )

#Очистить сообщения
@client.command( pass_context = True )
@commands.has_any_role( 767982859792941086, 767828673842642945, 769440573618126888, 769440464393863208, 772187416885985290 )

async def очистить( ctx, amount : int ):
	await ctx.channel.purge( limit = amount )

	await ctx.send(embed = discord.Embed(description = f':white_check_mark: Удалено {amount} сообщений', color = 0x0c0c0c))

#кик
@client.command( pass_context = True )
@commands.has_any_role( 767982859792941086, 767828673842642945, 769440573618126888, 769440464393863208, 772187416885985290 )

async def kick( ctx, member: discord.Member, *, reason = None ):
	await ctx.channel.purge( limit = 1 )

	await member.kick( reason = reason )
	await ctx.send(f'Был кикнут { member.mention }!')

#бан
@client.command( pass_context = True )
@commands.has_any_role( 767982859792941086, 767828673842642945, 769440573618126888, 769440464393863208, 772187416885985290 )

async def ban( ctx, member: discord.Member, *, reason = None ):
	await ctx.channel.purge( limit = 1 )

	await member.ban( reason = reason )
	await ctx.send(f'Был забанен { member.mention }!')

#unbun
@client.command( pass_context = True )
@commands.has_any_role( 767982859792941086, 767828673842642945, 769440573618126888, 769440464393863208, 772187416885985290 )

async def unban( ctx, *, member ):
	await ctx.channel.purge( limit = 1 )

	banned_users = await ctx.guild.bans()

	for ban_entry in banned_users:
		user = ban_entry.user

		await ctx.guild.unban( user )
		await ctx.send( f'Разбанен пользователь { user.mention }' )

		return

#mute
@client.command( pass_context = True )
@commands.has_any_role( 767982859792941086, 767828673842642945, 769440573618126888, 769440464393863208, 772187416885985290 )

async def mute( ctx, member: discord.Member ):
	await ctx.channel.purge( limit = 1 )

	mute_role = discord.utils.get( ctx.message.guild.roles, name = 'Мут' )

	await member.add_roles( mute_role )
	await ctx.send( f'Теперь { member.mention } замучен' )

#unmute
@client.command( pass_context = True )
@commands.has_any_role( 767982859792941086, 767828673842642945, 769440573618126888, 769440464393863208, 772187416885985290 )

async def unmute( ctx, member: discord.Member ):
	await ctx.channel.purge( limit = 1 )

	mute_role = discord.utils.get( ctx.message.guild.roles, name = 'Мут' )

	await member.remove_roles( mute_role )
	await ctx.send( f'Теперь { member.mention } размучен' )


#help
@client.command(pass_context = True)
@commands.has_any_role( 769440625497210891, 769440464393863208, 769440573618126888, 772016404588396564, 772187416885985290 )

async def help( ctx ):
	emb = discord.Embed( title = 'Помощь по командам' )

	emb.add_field( name = '.help', value = 'Показать это меню' )
	emb.add_field( name = '.rules', value = 'Показать правила дискорда' )
	emb.add_field( name = '.help_adm', value = 'Помощь администрации' )

	await ctx.send( embed = emb )

#help_adm
@client.command(pass_context = True)
@commands.has_any_role( 767982859792941086, 767828673842642945, 769440573618126888, 772187416885985290 )

async def help_adm( ctx ):
	emba = discord.Embed( title = 'Помощь по командам для администрации' )

	emba.add_field( name = '.очистить', value = 'Очистить сообщения' )
	emba.add_field( name = '.kick', value = 'Кикнуть игрока с сервера' )
	emba.add_field( name = '.ban', value = 'Забанить игрока' )
	emba.add_field( name = '.unban', value = 'Разбанить игрока' )
	emba.add_field( name = '.mute', value = 'Замутить игрока' )
	emba.add_field( name = '.unmute', value = 'Размутить игрока' )

	await ctx.send( embed = emba )

#rules
@client.command(pass_context = True)

async def rules( ctx ):
	embr = discord.Embed( title = 'Правила дискорда' )

	embr.add_field( name = '1', value = 'Не матерится [Предупреждение --> Мут на 1 час --> Мут на 3 часа]' )
	embr.add_field( name = '2', value = 'Не пинговать просто так [Предупреждение --> Мут на 1 час --> Мут на день]' )
	embr.add_field( name = '3', value = 'Оффтоп, спам, флуд, капс [Предупреждение --> мут на 30мин --> Мут на 2 часа]' )
	embr.add_field( name = '4', value = 'Не просить дать роль [Мут 30 минут]' )
	embr.add_field( name = '5', value = 'Не флудить командами [Мут на час --> Мут на 2 часа]' )
	embr.add_field( name = '6', value = 'Оскорбление родственников или учасников сообщества карается [мут 1 день --> мут 3 дня]' )

	await ctx.send( embed = embr )

#ошибки:

#ошибка очсистить
@очистить.error
async def clear_error( ctx, error ):
	if isinstance( error, commands.MissingRequiredArgument ):
		await ctx.send( f'{ctx.author.name} пожалуйста укажите количество очищаемых сообщений!' )
#ошибка мут
@mute.error
async def mute_error( ctx, error ):
	if isinstance( error, commands.MissingRequiredArgument ):
		await ctx.send( f'{ctx.author.name} пожалуйста укажите учасника которого нужно замутить!' )
#ошибка бан
@ban.error
async def ban_error( ctx, error ):
	if isinstance( error, commands.MissingRequiredArgument ):
		await ctx.send( f'{ctx.author.name} пожалуйста укажите учасника которого нужно забанить!' )
#ошибка кик
@kick.error
async def kick_error( ctx, error ):
	if isinstance( error, commands.MissingRequiredArgument ):
		await ctx.send( f'{ctx.author.name} пожалуйста укажите учасника которого нужно кикнуть!' )
#ошибка разбан
@unban.error
async def unban_error( ctx, error ):
	if isinstance( error, commands.MissingRequiredArgument ):
		await ctx.send( f'{ctx.author.name} пожалуйста укажите учасника которого нужно размутить!' )


client.run(settings['TOKEN'])