import os
import requests
import structures
from nicegui import ui

HEADERS = {'X-API-KEY': os.getenv("bungie_token"), 'Content-Type': 'application/json'}

class AccountStats():
    def __init__(self, name):
        """
        Takes user full name ex// khazicus#9648
        and sets bungie membership id, platform, destiny membership id, and your name,
        DOES NOT USE SEARCHUSERBYGLOBALNAME AS IT LITERALLY DOES NOT WORK FOR EVERY USER

        """
        if '#' not in name:
            ui.notify("Invalid user, please properly input the bungie name of the user you are searching.")
            raise Exception("Invalid user, please properly input the bungie name of the user you are searching.")
        
        # get prefix and numbers
        splitString = name.split("#")
        displayName = splitString[0]
        displayNameCode = splitString[1]

        url = f'https://www.bungie.net/Platform/User/Search/Prefix/{displayName}/0/'
        response = requests.get(url, headers=HEADERS)
        response = response.json()

        # get any user with that prefix, then specifically search for the user with the numbers provided
        listOfUsers = response['Response']['searchResults']
        for user in listOfUsers:
            if user['bungieGlobalDisplayName'] == displayName and user['bungieGlobalDisplayNameCode'] == int(displayNameCode):
                self.bungie_membership_id  =  user['bungieNetMembershipId']
                self.platform              =  user['destinyMemberships'][0]['membershipType']
                self.destiny_membership_id =  user['destinyMemberships'][0]['membershipId']
                self.bungie_name           =  name
        try:
            self.bungie_name
        except AttributeError:
            ui.notify("Invalid user, please properly input the bungie name of the user you are searching.")
            raise Exception("Invalid user, please properly input the bungie name of the user you are searching.")
            

        # initialization stuff
        self.titleStatus = []
        self.most_used_exotic_dict = {}
        self.raidClears = {
                      'Last Wish': 0, 
                      'Garden of Salvation': 0,
                      'Deep Stone Crypt': 0,
                      'Vault of Glass': 0,
                      'Vow of the Disciple': 0,
                      "King's Fall": 0,
                      'Root of Nightmares': 0,
                      "Crota's End": 0,
                      "Salvation's Edge": 0,
                      'The Pantheon': 0
                     }
        self.total_lowmans = {4: [],
                              3: [],
                              2: [],
                              1: []}
        self.dungeon_completions = {}
        self.flawlessRaidClears = []
        self.SoloFlawlessDungeonClears = []
        self.all_character_ids = ''
        self.highest_guardian_rank = ''
        self.seasons_played = ''
        self.glimmer = ''
        self.shards = ''
        self.bright_dust = ''
        self.favorite_element = ''
        self.favorite_element_kills = 0
    
    def grabCharacterInfo(self):
        """"
        Grabs general character info, such as character ids, guardian rank, and seasons played.
        Also gets play time, equipped emblem, and title.

        """
        try:
            response = requests.get(url=f"https://www.bungie.net/Platform/Destiny2/{self.platform}/Profile/{self.destiny_membership_id}/?components=Profiles,Characters", headers=HEADERS)
        except:
            print("Unable to get character information. Exiting...")
            exit()
            # exits because there is no point if character ids can not be accessed
        
        profileData = response.json()

        data = profileData['Response']['profile']['data']
        # general profile data

        self.all_character_ids      =  data['characterIds']
        self.highest_guardian_rank  =  data['lifetimeHighestGuardianRank']
        self.seasons_played         =  data['seasonHashes']
        # hashes of all seasons participated in

        character_ids = profileData['Response']['characters']['data']
        self.totalPlaytime = 0
        max = 0
        
        # loop gets total play time and character with most play time + that character's emblem
        for character in self.all_character_ids:
            total_minutes_per_char = int(character_ids[character]['minutesPlayedTotal'])
            self.totalPlaytime      = self.totalPlaytime + total_minutes_per_char
            if total_minutes_per_char > max:
                max = total_minutes_per_char
                self.main           = character_ids[character]['classType']
                self.main_emblem    = character_ids[character]['emblemHash']
                try:
                    self.main_title = character_ids[character]['titleRecordHash']
                except:
                    self.main_title = 'No Title Equipped'


    
    def grabTenFavoriteWeapons(self):
        """
        Searches exotic weapon usage for 10 most kills exotics, dependent upon grabCharacterInfo() for character ids.

        """
        counter = 1
        
        for character in self.all_character_ids:
            try:
                response = requests.get(f"https://www.bungie.net/Platform/Destiny2/{self.platform}/Account/{self.destiny_membership_id}/Character/{character}/Stats/UniqueWeapons/", headers=HEADERS)
            except:
                print("Failed to get character data. Exiting... \n")
                exit()
            characterData = response.json()
            i = 0
            try:
                # if a character has no exotic weapon data then this if will fail causing the exception to occur without failing the program
                if (characterData['Response']['weapons']):
                    while i < len(characterData['Response']['weapons']):
                        # get the stuff we are interested in (weapon hash and its respective kills)
                        weapon_hash  = str(characterData['Response']['weapons'][i]['referenceId'])
                        weapon_kills = characterData['Response']['weapons'][i]['values']['uniqueWeaponKills']['basic']['value']
                        # if existing weapon hash, add the kills to the existing value, else append it to the dict
                        if weapon_hash in self.most_used_exotic_dict:
                            self.most_used_exotic_dict[weapon_hash] = self.most_used_exotic_dict[weapon_hash] + weapon_kills
                        else:
                            self.most_used_exotic_dict[weapon_hash] = weapon_kills
                        i = i + 1
                    # sort the weapons by descending since we want most kills at the top
                    self.most_used_exotic_dict = {exotic: kills for exotic, kills in sorted(self.most_used_exotic_dict.items(), key=lambda item: item[1], reverse=True)}
                counter = counter + 1
            except:
                print(f"Weapon data for character {counter} does not exist. This corresponds to their order on the game screen, top to bottom. ")
                counter = counter + 1

            # configured to only show the top 10; change if statement parameter if you want more
            f = 0
            for exotic in list(self.most_used_exotic_dict.keys()):
                if f >= 10:
                    del self.most_used_exotic_dict[exotic]
                f = f + 1              
    
    # def grabGlimmerShardsDust(self):
    #     """
    #     Gets remarkable currencies.

    #     """
    #     try:
    #         response = requests.get(f"https://www.bungie.net/Platform/Destiny2/{self.platform}/Profile/{self.destiny_membership_id}/?components=ProfileCurrencies", headers=HEADERS)
    #     except:
    #         print("Currency Finder Failed.")
    #         exit()

    #     currencyFinder = response.json()
    #     print(currencyFinder['Response'])
    #     self.glimmer        = currencyFinder['Response']['profileCurrencies']['data']['items'][0]['quantity']
    #     self.shards         = currencyFinder['Response']['profileCurrencies']['data']['items'][1]['quantity']
    #     self.bright_dust    = currencyFinder['Response']['profileCurrencies']['data']['items'][2]['quantity']
    #     # I feel like these are the most significant currencies...
                    
    def grabRaidInfo(self):
        """
        Gets total clears for each raid, dependent upon grabCharacterInfo() for character ids.
        """
        for character in self.all_character_ids:
            response = requests.get(f"https://www.bungie.net/Platform/Destiny2/{self.platform}/Account/{self.destiny_membership_id}/Character/{character}/Stats/AggregateActivityStats/", headers=HEADERS)
            # request for ALL activity data; has every single activity in an array each with its own unique hash
            activities = response.json()
            # we just want the raids
            for activity in activities['Response']['activities']:
                # 'displayValue' has the clear number for each hash
                # checks if hash is a raid hash, if it is then adds its clear value
                if activity['activityHash'] in structures.raid_completion_hashes.keys():
                    clearsNum = int(activity['values']['activityCompletions']['basic']['displayValue'])
                    self.raidClears[structures.raid_completion_hashes[activity['activityHash']]] = self.raidClears[structures.raid_completion_hashes[activity['activityHash']]] + clearsNum


    def grabAcquiredTitles(self):
        """
        Sets user titles as an array of the titles they have earned.

        """
        try:
            response = requests.get(url=f"https://www.bungie.net/Platform/Destiny2/{self.platform}/Profile/{self.destiny_membership_id}/?components=Records", headers=HEADERS)
        except:
            print("Unable to get title information. Exiting...")
            exit()     
        response = response.json()    
        profileRecords = response['Response']['profileRecords']['data']

        self.active_triumph_score   = profileRecords['activeScore']
        self.legacy_triumph_score   = profileRecords['legacyScore']
        self.total_triumph_score    = profileRecords['lifetimeScore']
        # all variations of triumph score
        # now, go through records and match titles, appending when acquired
        for title in structures.title_hashes:
            try:
                status = profileRecords['records'][title]['objectives'][0]['complete']
                if status == True:
                    self.titleStatus.append(title)
            except:
                # Moments of Triumph 2023 just doesn't work.. sorry Moments of Triumph 2023-ers
                print(title, ": Skipped")

    def grabFlawlessRaids(self):
        """
        Sets flawless raid clears as an array of each raid that has been flawlessed.

        """
        try:
            response = requests.get(url=f"https://www.bungie.net/Platform/Destiny2/{self.platform}/Profile/{self.destiny_membership_id}/?components=Records", headers=HEADERS)
        except:
            print("Unable to get flawless raid information. Exiting...")
            exit()     

        record_getter = response.json()

        records = record_getter['Response']['profileRecords']['data']['records']
        # go through records for raids and find flawless hashes, append to array if completed
        for hash in structures.flawless_raid_completion_hashes:
            if records[hash]['objectives'][0]['complete'] == True:
                self.flawlessRaidClears.append(structures.flawless_raid_completion_hashes[hash])

    def grabDungeonInfo(self):
        """
        Sets dungeon completions as a dictionary, defining each dungeon with their total number of clears by the user.

        """
        response = requests.get(f"https://www.bungie.net/Platform/Destiny2/{self.platform}/Profile/{self.destiny_membership_id}/?components=1100", headers=HEADERS)
        activities = response.json()
        metrics = activities['Response']['metrics']['data']['metrics']
        # go through metrics and find "____ completions metrics, hashes in structures.py"
        for metric in metrics:
            if metric in structures.dungeon_completion_hashes:
                self.dungeon_completions[structures.dungeon_completion_hashes[metric]] = metrics[metric]['objectiveProgress']['progress']

    def grabSoloFlawlessDungeons(self):
        """
        Sets flawless dungeon clears as an array of each dungeon that has been flawlessed.

        """
        response = requests.get(url=f"https://www.bungie.net/Platform/Destiny2/{self.platform}/Profile/{self.destiny_membership_id}/?components=Records", headers=HEADERS)
        record_getter = response.json()

        # exact same process as grabbing flawless dungeons, goes through hashes from structures.py flawless_dungeon_completion_hashes and checks if complete
        records = record_getter['Response']['profileRecords']['data']['records']
        for hash in structures.flawless_dungeon_completion_hashes:
            if records[hash]['objectives'][0]['complete'] == True:
                self.SoloFlawlessDungeonClears.append(structures.flawless_dungeon_completion_hashes[hash])
    
    def favoriteElement(self):
        """
        Sets your favorite element as the one with the most kills by going through metric data.

        """
        response = requests.get(f"https://www.bungie.net/Platform/Destiny2/{self.platform}/Profile/{self.destiny_membership_id}/?components=1100", headers=HEADERS)
        metric_getter = response.json()
        metrics = metric_getter['Response']['metrics']['data']['metrics']
        for hash in structures.element_kills_metric_hashes:
            if metrics[hash]['objectiveProgress']['progress'] > self.favorite_element_kills:
                self.favorite_element_kills = metrics[hash]['objectiveProgress']['progress']
                self.favorite_element       = structures.element_kills_metric_hashes[hash]
    
    def grabRaidLowmans(self):
        """
        DATA PROVIDED BY LOWMAN-CENTRAL.COM 
        if this returns an empty array then try to search your name up on their website, probably due to not being in the database
        quad (in self.total_lowmans dict) only applies to SE

        """
        lowmanHeaders = {"membershipID": self.destiny_membership_id}
        response = requests.get(f"https://api.lowman-central.com/getPlayerData", headers=lowmanHeaders)
        lowman_clears = response.json()
        if lowman_clears == "[]":
            print("Please search yourself up on lowman-central.com in order for lowman data to be found.")
        else:
            for clear in lowman_clears:
                if clear['raid'] not in self.total_lowmans[clear['fireteamSize']]:
                    self.total_lowmans[clear['fireteamSize']].append(clear['raid'])
