#!/usr/bin/env python
# -*- coding: utf-8 -*-
import discord
import random
import cassiopeia as cass
from credentials import *
from cassiopeia import Summoner
from discord.ext import commands
from discord.utils import get

description = '''Big boi is here boys'''

#only woking with EUW ATM

#help command must DM a text with the help (pretty cool actually)

bot = commands.Bot(command_prefix=",", description=description)

##Variables
where_i_im="/var/git/lol_somthing/" #where is the file/folder of this python document...
user_folder=where_i_im+"users/"
blacklist_folder=user_folder+"blacklist/"
summonerlist_folder=user_folder+"summonerlist/"

client = discord.Client()

#Config_start
cass.set_riot_api_key(key)  # This overrides the value set in your configuration/settings.
cass.set_default_region("EUW") #Regio per defecte
#Config_end

##Commands

@bot.event
async def on_ready():
	print('Logged as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')

@bot.command() #0
async def hello(ctx):
	await ctx.send('Hello world') #T




#############################################################################
#								Definitions									#
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
	"""use 'rankeu *account*' to check the elo from this account (in the EWU server)"""
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
	if ("SOLO" in str([entry.queue])):	##podria fer una variable que emmagatzemes el format
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
	#"""syntax: ',mastery summoner_name comparative_argument number' where summoner_name it's a summoner name, comparative_argument it's one of this options {== (equal),< (smaller than), > (bigger than), >= bigger (than or equal), <= (smaller than or equal)}"""
	"""usage: ',mastery summoner_name '>/</>=/<=/==/!=' number' where summoner_name it's a summoner name, comparative_argument it's one of this options {== (equal),< (smaller than), > (bigger than), >= bigger (than or equal), <= (smaller than or equal)}"""
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
async def list_add(ctx, arg1):
	if arg1 is None:	#if not user:
		await ctx.send("Please, introduce a summoner name to add inside the list!")
	else:
		summ_name = arg1
		try:
			summoner_list_file_a = open(summonerlist_folder+""+str(ctx.author.id), "a")
			summoner_list_file_r = open(summonerlist_folder+""+str(ctx.author.id), "r")
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
		except FileNotFoundError:
			await ctx.send ("Wait... what?! contact the administrator this isn't supposed to happen!")

@bot.command(pass_context=True)
async def list(ctx, user: discord.User = None):
	"""use 'list' to check your list, or use 'list @somone' to see his list"""
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
	#except AttributeError:
	#	await ctx.send ("Fi Fa Fum what u did wrong?")
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
			summoner_list_file_r = open(summonerlist_folder+""+str(ctx.author.id), "r")
			file_readed = summoner_list_file_r.read().splitlines()
			exist=False
			for line in file_readed:
				if line == summ_name:
					exist=True
				else:
					file=(file+line+"\n")
			summoner_list_file_r.close()
			if exist:
				summoner_list_file_w = open(summonerlist_folder+""+str(ctx.author.id), "w")
				await ctx.send("Removed ["+summ_name+"] from the summoner list")
				summoner_list_file_w.write(file)
				summoner_list_file_w.close()
			else:
				await ctx.send("["+summ_name+"] was not found inside the summoner list")



		except FileNotFoundError:
			await ctx.send ("The user does not have a list, start by adding a summoner name!")



## Black List
@bot.command()
async def blacklist(ctx):
	await ctx.send("Coming soon")





### EXTRA ###
@bot.command()
async def ching(ctx, text:str):
	"""call me .ching chong"""
	if text=="chong":
		await ctx.send("Your champion is wrong!")


bot.run(TOKEN)
