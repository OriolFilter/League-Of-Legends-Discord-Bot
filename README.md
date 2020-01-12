# Big boi [discord bot]

	Discord bot which uses RIOT Games api to extract info


## Utilities

	Each discord can have a list of accounts, which every user can look at, so everyone can check lists in case they want to add each others or somthing, there is also a blacklist, so every user can add whoever they want, it jus acts as a list anyway, users can also delete the accounts previouslly added.

	Users can get information about league of legends accounts, checking masterys, ranked elo and account level.

## Commands

### Summoner_list:


	accounts_list: 		{list|list_add|list_del}

	blacklist_list: 	{blacklist|black_add|black_del}

## Summoner info

	EUW:		      	{eloeu|suminfo|mastery}

## Misc

	misc:			{ching}

## Help

	help:			{help}

#Requisites

    install cassiopeia library: pip3 install cassiopeia
    
    install discord library:    pip3 install discord
    
    All tested on python3.8, in case you use a previous version, i can't ensure all work correctlly. 
    
#Disclaimer

    I don't own any of the libraries used, and of course i don't work with Riot and im not owner of any of the data about League of Legends



## Patch notes

    #1.0
    
    	accounts_list: 		{list|list_add|list_del}
       	blacklist_list: 	{blacklist|black_add|black_del}
	        EUW:		      	{eloeu|suminfo|mastery}
		misc:		    	{ching|free|new}
		help:                   {help}
	
	#1.1
	    
	    suminfo,eloeu       Now reply error message if 'summoner_name' was not found in EUW
	    
	                        Using the command without argument will return the command for each of the account inside your 'summoner_list'
	    
	                        Using the command with a user as a argument withll return the comaman for each of the accounts inside their 'summoner_list'
        
        free                *added command* Returns the weekly champion rotation
        
        new                 *added command* Returns the champion rotation for new players
        
        help                Updated help with the actual changes
        
                            

#Possible future updates

    Being able to vinculate your account, so you don't have to rename the list when you change you name
    
    status command to check server status