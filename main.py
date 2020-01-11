#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import cassiopeia as cass
from credentials import *
from cassiopeia import Summoner
#from cassiopeia import *

#
import simplejson

##Variables
user_folder="users/"
blacklist_folder=user_folder+"blacklist/"
summonerlist_folder=user_folder+"summonerlist/"
#


#Config_start
cass.set_riot_api_key(key)  # This overrides the value set in your configuration/settings.
cass.set_default_region("EUW") #Regio per defecte
#Config_end

### fucntions



def ask_summoner_name():
	global summoner
	global summoner_input
	summoner_input = input("Who you wanna search for? ")
	#summoner = Summoner(name=summoner_input)
	summoner = cass.get_summoner(name=summoner_input)
	print("\nSearching for ",summoner_input)

#Rank

def get_rank():
	entries = summoner.league_entries
	user_rank = ""
	for entry in entries:
		if user_rank == "":
			print ("started user_rank")	#DEBUGG
			user_rank = get_queue_rank(entry)
		else:
			user_rank = user_rank+"\n"+get_queue_rank(entry)
	if user_rank != "" : #CHECK_if_empty 
		print ("\nQueue Name\tTier\t\tDivision\tlp\tLeague Name\n-----------------------------------------------------------------------------------\n"+user_rank) #FORMATAT COLUMNES
	else:
		print("empty_rank")##debugg


#GET_QUEUE_NAME
def get_queue_rank(entry):
	if ("SOLO" in str([entry.queue])):	##podria fer una variable que emmagatzemes el format
		queue_name = "Solo/Duo 5v5"
	elif ("flex" in str([entry.queue])):
		queue_name = "Flex 5v5"
	else:
		queue_name = "NotDetectedQueue"

	#Formating/check_tier
	if (str(entry.tier) == "Diamond"):
		f_tier=str(entry.tier)+"\t"
	elif (str(entry.tier) == "Platinum") or (str(entry.tier) == "Challenger") or (str(entry.tier) == "Grandmaster"):
		f_tier=str(entry.tier)
	else:
		f_tier=str(entry.tier)+"\t"

	queue_values = queue_name+"\t"+f_tier+"\t"+str(entry.division)+"\t\t"+str(entry.league_points)+"\t"+str(entry.league.name)
	return(queue_values)
#Mastery


def summoner_info():
	summ_info = "Summoner:\t{name}\nLevel:\t\t{level}\nRegion:\t\t{region}".format(name=summoner.name,
																			     	level=summoner.level,
									    											region=summoner.region)
	print (summ_info)




def get_mastery_champions_above():
	ask_summoner_name()
	print("Checking mastery from the summoner: "+summoner_input)
	comparative_argument, comparative_text=get_comparative_argument()
	mastery_level=get_mastery_level()
	good_with =eval ("summoner.champion_masteries.filter(lambda cm: cm.level {arg} {mastery_level})".format(arg=comparative_argument,
																											mastery_level=mastery_level))  #get the info
	print("\nPrinting champions from ",summoner_input," which are ",comparative_text," mastery level ",mastery_level)
	print([cm.champion.name for cm in good_with])
	#print(good_with) #List objects, learn to print objects and deal with them!

def get_mastery_level():
	min_menu=0
	max_menu=7
	condition = True
	while condition:  ##do while emulation
		mastery_level = input("Introduce above which mastery level want to filter, by default its 6: ")
		if not mastery_level:
			print("Using the default mastery level")
			mastery_level=6
			condition = False
		else:
			try:
				mastery_level = int(mastery_level)
				if ( mastery_level < min_menu) or ( mastery_level > max_menu):
					print ("Your input wasn't inside the desired range (min ",min_menu," and max ",max_menu,"), please try again")
				else:
					print ("Filtering by level ",mastery_level)
					condition = False
			except ValueError:
				print (mastery_level,' it\'s not a number, please try again')
	return(mastery_level)
	#END_WHILE

def get_comparative_argument():
	max_menu=5
	min_menu=0
	condition = True
	while condition:  ##do while emulation
		argument_menu = input("How you want to filter the values:\n\t1) == 'equal'\n\t2) >  'biger than'\n\t3) <  'smaller than'\n\t4) >= 'equal or bigger than' (default)\n\t5) <= 'equal or smaller than'\n\t")
		if not argument_menu:
			print("Using the default argument value")
			comparative_argument=">="
			condition = False
		else:
			try:
				argument_menu = int(argument_menu)
				if ( argument_menu < min_menu ) or ( argument_menu > max_menu ):
					print ("Your input wasn't inside the desired range (min ",min_menu," and max ",max_menu,"), please try again")
				else:
					if argument_menu == 1:
						comparative_argument="=="
						comparative_text="equal to"
					elif argument_menu == 2:
						comparative_argument=">"
						comparative_text="bigger than"
					elif argument_menu == 3:
						comparative_argument="<"
						comparative_text="smaller than"
					elif argument_menu == 4:
						comparative_argument=">="
						comparative_text="equal or bigger than"
					else:
						comparative_argument="<="
						comparative_text="equal or smaller than"
					condition = False
			except ValueError:
				print (mastery_level,' it\'s not a number, please try again')
	return(comparative_argument, comparative_text)

def summoner_list_menu():
	print("Managing summoner list")
	print("getting discord_user_id") #potser millor despres del menu
	discord_user_id="some_user_id"
	max_menu=3
	min_menu=0
	condition = True
	while condition:  ##do while emulation
		argument_menu = input("Select what you want to do\n\t1)\tList users from your list (default)\n\t2)\tAdd users to your summoner list\n\t3)\tRemove users to your summoner list\n\t")
		if not argument_menu:
			print("Using the default argument value")
			argument_menu="1"
			condition = False
		else:
			try:
				argument_menu = int(argument_menu)
				if ( argument_menu < min_menu ) or ( argument_menu > max_menu ):
					print ("Your input wasn't inside the desired range (min ",min_menu," and max ",max_menu,"), please try again")
				else:
					if argument_menu == 1:
						print("listing summoners in sumoners list")
						list_summoner_list(discord_user_id)
					elif argument_menu == 2:
						print("adding a summoner to your summoner list")
						add_summoner_list(discord_user_id)
					elif argument_menu == 3:
						print("removing a summoner in your summoner list")
					condition = False
			except ValueError:
				print (argument_menu,' it\'s not a number, please try again')
	#FI_MENU

def list_summoner_list(discord_user_id):
	try:
		summoner_list_file_r = open(summonerlist_folder+discord_user_id, "r")
		file_readed = summoner_list_file_r.read().splitlines()
		if not file_readed :
			print("the file is empty!")
		else:
			print (file_readed)

	except ValueError:
		print ("The user does not have a file")
	summoner_list_file_r.close()

##
def add_summoner_list(discord_user_id):
		print("ADDINGTHINGS")
		summoner_list_file_a = open(summonerlist_folder+discord_user_id, "a")
		summoner_list_file_r = open(summonerlist_folder+discord_user_id, "r")
		file_readed = summoner_list_file_r.read().splitlines()
		summ_name = input("Introduce the name of the summoner that you want to add to your summoner list\n").lower()
		##CHECK IF EXISTS
		print("Checking if the summoner is alredy in")

		exist=False
#		while line in file_readed or not exist: #pendent
		for line in file_readed:
			print(line)
			if line == summ_name:
				exist=True
				print("TRUE")
		if not exist:
			summoner_list_file_a.write(summ_name+"\n")
			print ("Added "+summ_name+" to the summoner list")
		else:
			print ("This summoner name is alredy in")

		summoner_list_file_r.close()
		summoner_list_file_a.close()
#Read from summonerlist


def menu():
	max_menu=5
	min_menu=0
	condition = True
	while condition:  ##do while emulation
		argument_menu = input("What do you wanna do? (enabled)\n\t1) Check Summoner information\n\t2) Filter champions by maestry level (default)\n\t3) Manage summoner list\n\t4) Go kys\n\t")
		if not argument_menu:
			print("Using the default argument value")
			argument_menu = "2"
			condition = False
		else:
			try:
				argument_menu = int(argument_menu)
				if ( argument_menu < min_menu ) or ( argument_menu > max_menu ):
					print ("Your input wasn't inside the desired range (min ",min_menu," and max ",max_menu,"), please try again")
				else:
					if argument_menu == 1:
						ask_summoner_name()
						print("Checking Summoner rank")
						#summoner_info()
						get_rank()
					elif argument_menu == 2:
						#ask_summoner_name()
						get_mastery_champions_above()
					elif argument_menu == 3:
						print("Managing user lists")
						summoner_list_menu()
						#function
					else:
						print("going to kill myself")
					condition = False
			except ValueError:
				print (argument_menu,' it\'s not a number, please try again')
	#MENU_END

### Main



#IF MENU





#IF MENU 2


##CallMain

menu()
print("exiting")


########
###Extra
########


#summoner = Summoner(name="username", region)


#print("{name} is a level {level} summoner on the {region} server.".format(name=summoner.name,
#                                                                          level=summoner.level,
#                                                                          region=summoner.region))



#print(draven_games = Summoner(name=username, region='EUW').match_history[draven])
#print(draven_games = Summoner(name=summoner, region).match_history[draven])

#print(draven_games)

#good_with = summoner.champion_masteries.filter(lambda cm: cm.level >= 6)
#print([cm.champion.name for cm in good_with])
#print([cm.champion.name for cm in good_with])

#summoner.champion_masteries
#summoner.match_history
#summoner.current_match
#summoner.leagues


