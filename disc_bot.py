#!/usr/bin/env python
# -*- coding: utf-8 -*-
import discord
import cassiopeia as cass
import os
from credentials import *
from cassiopeia import Summoner
from discord.ext import commands
from discord.utils import get

description = '''Big boi is here to help you out!'''

#only woking with EUW ATM

bot = commands.Bot(command_prefix="b.", description=description) #b from bigboy
bot.remove_command('help')


##Variables_start
where_i_im=os.path.dirname(os.path.abspath(__file__)) #where is the file/folder of this python document...
user_folder=where_i_im+"/users/"
blacklist_folder=user_folder+"blacklist/"
summonerlist_folder=user_folder+"summonerlist/"
help_file_location=where_i_im+"/help.txt"
client=discord.Client()
#Variables_End

#Config_start
cass.set_riot_api_key(key)
cass.set_default_region("EUW") #Default region
#Config_end

##Commands_start
@bot.event
async def on_ready():
	print('------')
	print('Logged as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')
	game = discord.Game("No worries, im here for you, type \"b.help\" so i can help!")
	await bot.change_presence(status=discord.Status.online, activity=game)

##Check_if_folder_exists_start
if not os.path.isdir(blacklist_folder) or not os.path.isdir(summonerlist_folder):
	print ("if party start")
	if not os.path.isdir(blacklist_folder):
		os.makedirs(blacklist_folder)
	if not os.path.isdir(summonerlist_folder):
		os.makedirs(summonerlist_folder)
	os.walk("chmod 700"+user_folder+" -R && chown "+str(os.geteuid())+":"+str(os.getegid())+" -R")
#Check_if_folder_exists_end

#############################################################################
#				Definitions				    #
#############################################################################


def get_summoner(summoner_input):
	#summoner = Summoner(name=summoner_input)
	summoner = cass.get_summoner(name=summoner_input)
	return(summoner)

@bot.command()
async def suminfo(ctx, arg1):
	"""Prints basic summoner info,  usage: ,suminfo 'summoner'"""
	summoner = get_summoner(arg1)
	summ_info = "Summoner:\t{name}\nLevel:\t\t\t\t{level}\nRegion:\t\t\t{region}".format(name=summoner.name,
																						 level=summoner.level,
																						 region=summoner.region)
	await ctx.send(summ_info)

@bot.command()
async def rankeu(ctx, arg1):
	summoner = get_summoner(arg1)

	entries = summoner.league_entries
	user_rank = ""
	for entry in entries:
		if user_rank == "":
			user_rank = get_queue_rank(ctx,entry)
		else:
			user_rank = user_rank+"\n"+get_queue_rank(ctx,entry)
	if user_rank != "" : #CHECK_if_empty
		await ctx.send ("\nMode\t\t\t\t  Tier\t\tDiv\tlp\t  League Name\n---------------------------------------------------------------\n"+user_rank) #FORMATAT COLUMNES
	else:
		await ctx.send ("Player it's not currentlly ranked")##debugg

#GET_QUEUE_NAME
def get_queue_rank(ctx,entry):
	if ("SOLO" in str([entry.queue])):
		queue_name = "Solo/Duo 5v5"
	elif ("flex" in str([entry.queue])):
		queue_name = "Flex 5v5"
	else:
		queue_name = "NotDetectedQueue"

	#Formating/check_tier
	if (str(entry.tier) == "Diamond"):
		f_tier="Dia\t"
	elif (str(entry.tier) == "Platinum"):
		f_tier="Plat\t"
	elif (str(entry.tier) == "Challenger"):
		f_tier="Chall\t"
	elif (str(entry.tier) == "Grandmaster"):
		f_tier="GrandM\t"
	elif (str(entry.tier) == "Grandmaster"):
		f_tier="Mastr\t"
	elif (str(entry.tier) == "Silver"):
		f_tier="Silv\t"
	else:
		f_tier=str(entry.tier)+"\t"

	queue_values = queue_name+"\t"+f_tier+"\t"+str(entry.division)+"\t\t"+str(entry.league_points)+"\t"+str(entry.league.name)
	return(queue_values)


#Mastery

@bot.command(pass_context=True)
async def mastery(ctx,arg1,arg2,arg3):
	mastery_level = arg3
	print(arg1,arg2,arg3)
	if arg3 is None:
		await ctx.send("Please revise your input and try again")
	else:
		summoner = get_summoner(arg1)
		good_with =eval ("summoner.champion_masteries.filter(lambda cm: cm.level {arg} {mastery_level})".format(arg=arg2,
																												mastery_level=arg3))  #get the info
		text = arg1 +" "+arg2+" "+arg3+"\n"
		text = text +"```"+str([cm.champion.name for cm in good_with])+"``` "+arg2+arg3
		print(text)
		await ctx.send(text)

## Summ List

@bot.command(pass_context=True)
async def list_add(ctx, arg1=None):
	if arg1 is None:	#if not user:
		await ctx.send("Please, introduce a summoner name to add inside the list!")
	else:
		summ_name = arg1
		try:
			summoner_list_file_a = open(summonerlist_folder+str(ctx.author.id), "a")
			summoner_list_file_r = open(summonerlist_folder+str(ctx.author.id), "r")
			file_readed = summoner_list_file_r.read().splitlines()
			exist=False
			for line in file_readed:
				if line == summ_name:
					exist=True
			if not exist:
				summoner_list_file_a.write(summ_name+"\n")
				await ctx.send("["+summ_name+"] added to the summoner list")
			else:
				await ctx.send("["+summ_name+"] is alredy inside the summoner list")
			summoner_list_file_r.close()
			summoner_list_file_a.close()
		except FileNotFoundError:
			await ctx.send ("Wait... what?! contact the administrator this isn't supposed to happen!")

@bot.command(pass_context=True)
async def list(ctx, user: discord.User = None):
	if user is None:	#if not user:
		user=ctx.author
	id=str(user.id)
	try:
		summoner_list_file_r = open(summonerlist_folder+id, "r")
		file_readed = str(summoner_list_file_r.read().splitlines())
		if not file_readed :
			await ctx.send("The user does not have a list, start by adding a summoner name!")
		else:
			await ctx.send(user.mention+"'s summoner list: "+file_readed)
	except FileNotFoundError:
		await ctx.send ("The user does not have a list, start by adding a summoner name!")

	summoner_list_file_r.close()

@bot.command(pass_context=True)
async def list_del(ctx, arg1):
	if arg1 is None:	#if not user:
		await ctx.send("Please, introduce a summoner name to add inside the list!")
	else:
		file = ""
		summ_name = arg1
		try:
			summoner_list_file_r = open(summonerlist_folder+str(ctx.author.id), "r")
			file_readed = summoner_list_file_r.read().splitlines()
			exist=False
			for line in file_readed:
				if line == summ_name:
					exist=True
				else:
					file=(file+line+"\n")
			summoner_list_file_r.close()
			if exist:
				summoner_list_file_w = open(summonerlist_folder+str(ctx.author.id), "w")
				await ctx.send("Removed ["+summ_name+"] from the summoner list")
				summoner_list_file_w.write(file)
				summoner_list_file_w.close()
			else:
				await ctx.send("["+summ_name+"] was not found inside the summoner list")
		except FileNotFoundError:
			await ctx.send ("The user does not have a list, start by adding a summoner name!")



## Black List
@bot.command(pass_context=True)
async def black_add(ctx, arg1=None):
	if arg1 is None:	#if not user:
		await ctx.send("Please, introduce a summoner name to add inside the list!")
	else:
		summ_name = arg1
		try:
			summoner_list_file_a = open(blacklist_folder+str(ctx.author.id), "a")
			summoner_list_file_r = open(blacklist_folder+str(ctx.author.id), "r")
			file_readed = summoner_list_file_r.read().splitlines()
			exist=False
			for line in file_readed:
				if line == summ_name:
					exist=True
			if not exist:
				summoner_list_file_a.write(summ_name+"\n")
				await ctx.send("["+summ_name+"] added to the summoner list")
			else:
				await ctx.send("["+summ_name+"] is alredy inside the summoner list")
			summoner_list_file_r.close()
			summoner_list_file_a.close()
		except FileNotFoundError:
			await ctx.send ("Wait... what?! contact the administrator this isn't supposed to happen!")

@bot.command(pass_context=True)
async def blacklist(ctx, user: discord.User = None):
	if user is None:
		user=ctx.author
	id=str(user.id)
	try:
		summoner_list_file_r = open(blacklist_folder+"+"+id, "r")
		file_readed = str(summoner_list_file_r.read().splitlines())
		if not file_readed :
			await ctx.send("The user does not have a list, start by adding a summoner name!")
		else:
			await ctx.send(user.mention+"'s summoner list: "+file_readed)
		summoner_list_file_r.close()
	except FileNotFoundError:
		await ctx.send ("The user does not have a list, start by adding a summoner name!")


@bot.command(pass_context=True)
async def black_del(ctx, arg1):
	if arg1 is None:	#if not user:
		await ctx.send("Please, introduce a summoner name to add inside the list!")
	else:
		file = ""
		summ_name = arg1
		try:
			summoner_list_file_r = open(blacklist_folder+str(ctx.author.id), "r")
			file_readed = blacklist_folder.read().splitlines()
			exist=False
			for line in file_readed:
				if line == summ_name:
					exist=True
				else:
					file=(file+line+"\n")
			summoner_list_file_r.close()
			if exist:
				summoner_list_file_w = open(summonerlist_folder+str(ctx.author.id), "w")
				await ctx.send("Removed ["+summ_name+"] from the summoner list")
				summoner_list_file_w.write(file)
				summoner_list_file_w.close()
			else:
				await ctx.send("["+summ_name+"] was not found inside the summoner list")
		except FileNotFoundError:
			await ctx.send ("The user does not have a list, start by adding a summoner name!")




### EXTRA ###
@bot.command()
async def ching(ctx, text:str):
	if text=="chong":
		await ctx.send("Your champion is wrong!")


# HELP
@bot.command()
async def help(ctx):

	help_ms = open((help_file_location), "r")
	help_message = help_ms.read()
	help_ms.close()

	await ctx.send(help_message)


bot.run(TOKEN)
