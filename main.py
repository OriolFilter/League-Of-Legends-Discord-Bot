#!/usr/bin/env python -*- coding: utf-8 -*-
import discord
import pymysql.cursors
import cassiopeia as cass
import arrow
from credentials import *
from cassiopeia import Summoner,Match
from discord.ext import commands
from datapipelines.common import NotFoundError

# Connect to the database

connection=pymysql.connect(host=HOST,
port=PORT,
user=userDB,
password=passDB,
db=dbName,
charset='utf8mb4',
cursorclass=pymysql.cursors.DictCursor)


#Discord Things
description = '''DB test'''

#only woking with EUW ATM

bot = commands.Bot(command_prefix="b.", description=description) #b from bigboy
#bot.remove_command('help')

##Commands_start
@bot.event
async def on_ready():
	print('------')
	print('Logged as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')
	game = discord.Game("disc bot start")
	await bot.change_presence(status=discord.Status.online, activity=game)


###LOL API
cass.set_riot_api_key(key)
cass.set_default_region("EUW") #Default region



#############################################################################
#								    SQL 								    #
#############################################################################

#Select
class updateDB:
    def __init__(self,dic):
        self.summoner=dic['summoner']
        self.soloq=dic['Queue.ranked_solo_fives']
        self.flexq=dic['Queue.ranked_flex_fives']
    
    def entryExists(self,table=None):
        SID=self.summoner["summoner_id"]
        with connection.cursor() as cursor:
            if table is 'INFO':
                sql = "SELECT SID from SUMMONERINFO where SID='{SID}'"
            elif table is 'SOLOQ':
                sql = "SELECT SID from SOLOQINFO where SID='{SID}'"
            elif table is 'FLEXQ':
                sql = "SELECT SID from FLEXQINFO where SID='{SID}'"
            elif table is 'REVISIONDATE':
                sql = "SELECT SID from REVISIONDATE where SID='{SID}'"
            else: return -2
            sql=sql.format(SID=SID)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is not None:
                return 1
            else:
                return 0
            
    
    def importSummonerInfo(self):
        if self.entryExists('INFO'): #update
            try:
                with connection.cursor() as cursor:
                    sql="UPDATE SUMMONERINFO SET SNAME='{SNAME}', LEVEL={LVL}, ICON={ICON},region=upper('{REGION}') WHERE SID='{SID}'".format(SID=self.summoner['summoner_id'],
                                                                                                                                               SNAME=self.summoner['name'],
                                                                                                                                               LVL=self.summoner['level'],
                                                                                                                                               ICON=self.summoner['icon'],
                                                                                                                                               REGION=self.summoner['region'])
                    cursor.execute(sql)
                    connection.commit()  
            except:
                connection.rollback()
                return -1
        else: #Import
            try:
                with connection.cursor() as cursor:
                    sql="INSERT INTO SUMMONERINFO VALUES ('{SID}', '{SNAME}', {LVL}, {ICON}, upper('{REGION}') )".format(SID=self.summoner['summoner_id'],
                                                                                                                         SNAME=self.summoner['name'],
                                                                                                                         LVL=self.summoner['level'],
                                                                                                                         ICON=self.summoner['icon'],
                                                                                                                         REGION=self.summoner['region'])
                    #('{SID}', '{SNAME}', LVL,ICON,upper('REGION') );
                    cursor.execute(sql)
                    connection.commit()
            except:
                connection.rollback()
                return -1
        
        if self.entryExists('SOLOQ'): #update
            try:
                with connection.cursor() as cursor:
                    if self.soloq['tier'] is None:
                        sql="UPDATE SOLOQINFO SET STIER=Null, SDIV=Null',SLP=Null,SLNAME=Null WHERE SID='{SID}'".format(SID=self.summoner['summoner_id'])
                    else:
                        sql="UPDATE SOLOQINFO SET STIER='{TIER}', SDIV='{DIV}',SLP={LP},SLNAME=\"{LNAME}\" WHERE SID='{SID}'".format(SID=self.summoner['summoner_id'],
                                                                                                                                TIER=self.soloq['tier'],
                                                                                                                                DIV=self.soloq['div'],
                                                                                                                                LP=self.soloq['lp'],
                                                                                                                                LNAME=self.soloq['leagueName'])
                    cursor.execute(sql)
                    connection.commit()  
            except:
                connection.rollback()
                return -1

        else: #Import
            try:

                with connection.cursor() as cursor:
                    if self.soloq['tier'] is None:
                        sql="INSERT INTO SOLOQINFO VALUES ('{SID}', Null, Null, Null, Null)".format(SID=self.summoner['summoner_id'])
                    else:
                        sql="INSERT INTO SOLOQINFO VALUES ('{SID}', '{TIER}', '{DIV}', {LP}, \"{LNAME}\")".format(SID=self.summoner['summoner_id'],
                                                                                                                    TIER=self.soloq['tier'],
                                                                                                                    DIV=self.soloq['div'],
                                                                                                                    LP=self.soloq['lp'],
                                                                                                                    LNAME=self.soloq['leagueName'])
                    cursor.execute(sql)
                    connection.commit()

            except:
                connection.rollback()
                return -1

        if self.entryExists('FLEXQ'): #update
            try:
                with connection.cursor() as cursor:
                    if self.flexq['tier'] is None:
                        sql="UPDATE FLEXQINFO SET FTIER=Null, FDIV=Null,FLP=Null,FLNAME=Null WHERE SID='{SID}'".format(SID=self.summoner['summoner_id'])
                    else:
                        sql="UPDATE FLEXQINFO SET FTIER='{TIER}', FDIV='{DIV}',FLP={LP},FLNAME=\"{LNAME}\" WHERE SID='{SID}'".format(SID=self.summoner['summoner_id'],
                                                                                                                                TIER=self.flexq['tier'],
                                                                                                                                DIV=self.flexq['div'],
                                                                                                                                LP=self.flexq['lp'],
                                                                                                                                LNAME=self.flexq['leagueName'])
                    cursor.execute(sql)
                    connection.commit()  
            except:
                connection.rollback()
                return -1

        else: #Import
            try:
                with connection.cursor() as cursor:
                    if self.flexq['tier'] is None:
                        sql="INSERT INTO FLEXQINFO VALUES ('{SID}', Null, Null, Null, Null)".format(SID=self.summoner['summoner_id'])
                    else:
                        sql="INSERT INTO FLEXQINFO VALUES ('{SID}', '{TIER}', '{DIV}', {LP}, \"{LNAME}\")".format(SID=self.summoner['summoner_id'],
                                                                                                                 TIER=self.flexq['tier'],
                                                                                                                 DIV=self.flexq['div'],
                                                                                                                 LP=self.flexq['lp'],
                                                                                                                 LNAME=self.flexq['leagueName'])
                    cursor.execute(sql)
                    connection.commit()

            except:
                connection.rollback()
                return -1
            
        if self.entryExists('REVISIONDATE'): #update
            try:
                with connection.cursor() as cursor:
                    sql="UPDATE REVISIONDATE SET DATE='{DATE}'WHERE SID='{SID}'".format(SID=self.summoner['summoner_id'],
                                                                                        DATE=self.summoner['revision_date'])
                    cursor.execute(sql)
                    connection.commit()  
            except:
                connection.rollback()
                return -1


        else: #Import
            try:
                with connection.cursor() as cursor:
                    sql="INSERT INTO REVISIONDATE VALUES ('{SID}','{DATE}')".format(SID=self.summoner['summoner_id'],
                                                                                    DATE=self.summoner['revision_date'])
                    cursor.execute(sql)
                    connection.commit()

            except:
                connection.rollback()
                return -1
        return 1
        

#Insert


#############################################################################
#								Definitions								    #
#############################################################################
def printDic(dic): #D
	for queue in dic:
		print(queue)
		for info in dic[queue]:
			print (info,dic[queue][info])
			

def checkRev_date(id,date):
    with connection.cursor() as cursor:
        sql = "SELECT DATE from REVISIONDATE where SID='{SID}'"
        sql=sql.format(SID=id)
        cursor.execute(sql)
        try:
            result = arrow.get(cursor.fetchone()['DATE'])
            if date<=result: return 1 #Casos que no ha dactualitzar
        except: pass
    return 0

def updateSummoner(sum,srv='EUW'):
    if checkRev_date(sum.id,sum.revision_date): return 1#dateInTheBDDIsNewerOrEqualToTheGiven  #Returns 1 if needs to update
    summonerInfoDic={
    'summoner':{
            "account_id":None,
            "summoner_id":None,
            "name":None,
            "level":None,
            "icon":None,
            "region":None,
            "revision_date":None
            },
    'Queue.ranked_solo_fives':{
            "tier":None,
            "div":None,
            "lp":None,
            "leagueName":None,
            },
    'Queue.ranked_flex_fives':{
            "tier":None,
            "div":None,
            "lp":None,
            "leagueName":None,
            },
    }
    
    def getSumInfo(summoner,dic):
        dic.update({"account_id": summoner.account_id})        
        dic.update({"summoner_id": summoner.id})        
        dic.update({"name": summoner.name})
        dic.update({"level": summoner.level})
        dic.update({"icon": summoner.profile_icon.id})
        dic.update({"revision_date": summoner.revision_date.format('YYYY-MM-DD HH:mm:ss')})
    
        if str(summoner.region) == "Region.europe_west":
            dic.update({"region": "EUW"})
        else:
            dic.update({"region": "NA"}) #upgrade #?¿?¿pa que
        return dic
    
    def getEloApi(summoner, summonerInfoDic):
        leaguesInfo = summoner.league_entries
        for queue in leaguesInfo:
                summonerInfoDic[str(queue.queue)].update({"tier": queue.tier})
                summonerInfoDic[str(queue.queue)].update({"div": queue.division})
                summonerInfoDic[str(queue.queue)].update({"lp": queue.league_points})
                summonerInfoDic[str(queue.queue)].update({"leagueName": queue.league.name})
        return summonerInfoDic


    try:
        summonerInfoDic['summoner']=getSumInfo(sum,summonerInfoDic['summoner'])
        summonerInfoDic=getEloApi(sum,summonerInfoDic)

        #printDic(summonerInfoDic)
        update = updateDB(summonerInfoDic)
        return update.importSummonerInfo()
    except: return 0

def getSummoner(usr):
	summoner = cass.get_summoner(name=usr)
	return(summoner)

class selectUsr:
        def __init__(self,id,inGame):
            with connection.cursor() as cursor:
                sql = "select * from SUMMONERINFO INNER JOIN (SOLOQINFO) USING (SID) JOIN (FLEXQINFO) USING (SID) where SID='{SID}';".format(SID=id)
                cursor.execute(sql)
                self.select = cursor.fetchone()
                self.ingame=inGame

                
        def formatEmbed(self):
            def fastForm(string):
                return string.format(   NAME=self.select['SNAME'],
                                        LVL=self.select['LEVEL'],
                                        ICON=self.select['ICON'],
                                        REGION=self.select['REGION'],
                                        STIER=self.select['STIER'],
                                        SDIV=self.select['SDIV'],
                                        SLP=self.select['SLP'],
                                        SLNAME=self.select['SLNAME'],
                                        FTIER=self.select['FTIER'],
                                        FDIV=self.select['FDIV'],
                                        FLP=self.select['FLP'],
                                        FLNAME=self.select['FLNAME']
                                        )
        
            msgSumm="lvl:      {LVL}\nregion:   {REGION}\n\n"
            if self.select['STIER']is not None:
                msgSolo="**Solo Q**\n{STIER} {SDIV}\n{SLP} LP\n*{SLNAME}*\n\n"
            else:
                msgSolo="**Solo Q**\n<currently unranked>\n\n"
                
            if self.select['FTIER']is not None:    
                msgFlex="**Flex Q**\n{FTIER} {FDIV}\n{FLP} LP\n*{FLNAME}*\n\n"
            else:
                msgFlex="**Flex Q**\n<currently unranked>\n\n"
            if self.ingame:
                msgIng="*{NAME} it's currently in-game*\n"
                color=0xF93228
            else:
                msgIng="*{NAME} it's not currently in-game*\n"
                color=0x3edc71
            ("Maybe check if in game?¿, maybe in footer") 
                        
            msg=msgSumm+msgSolo+msgFlex+msgIng
            embed=discord.Embed(title=fastForm("{NAME}"), description=fastForm(msg), color=color)
            if self.select['REGION'] == 'EUW':
                linkOPGG="https://euw.op.gg/summoner/userName={NAME}"
            elif self.select['REGION'] == 'NA':
                linkOPGG="https://na.op.gg/summoner/userName={NAME}"
            else:
                linkOPGG=""
                
            linkOPGG=fastForm(linkOPGG).replace(" ","%20")
            embed.set_author(name="OPGG",url=linkOPGG,  icon_url=fastForm("https://opgg-static.akamaized.net/images/profile_icons/profileIcon{ICON}.jpg"))
            return (embed)
            
            

#############################################################################
#								Commands								    #
#############################################################################


@bot.command()
async def info(ctx, usr=None):
    summoner=getSummoner(usr)
    if summoner.exists:
        #check revision date
        if not updateSummoner(summoner):
            ctx.send('There was an error updating the summoner information')
        try:
            instance = selectUsr(summoner.id,summoner.current_match.exists)
        
        except NotFoundError:
            instance = selectUsr(summoner.id,False)
        except:
            instance='There was an error, contact the administor'
        try:
            await ctx.send(embed=instance.formatEmbed())
        except:
            await ctx.send(instance)
    else:
        await ctx.send('Summoner not found')




#async def time():
        
#Run bot
try:
	bot.run(TOKEN)

finally:
		connection.close()
		print('The End')
