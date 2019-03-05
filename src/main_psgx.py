import lxml
import pandas as pd

class League:
    
    def __init__(self, file):
        root = lxml.etree.parse(file).getroot()
        self._doc = root.getchildren()[0] # only one element in the list
        self._params = {}
        for k, v in self._doc.items():
            self._params.update({k: v})
        self.name=self._params['competition_name']
        self.season=self._params['season_id']
        self.season_name=self._params['season_name']
        
        self._club = {}
        self._club_id = {}
        for c in self._doc.findall('Team'):
            club = Club(c)
            if not club.name is None:
                self._club[club.name] = club
                #self._club_id[club.uID] = club.name

            
    def get_club(self, clubname):
        return self._club.get(clubname)
    
    def get_info(self):
        params_dict = []
        for _, club in self._club.items():
            params_dict.append(club._params)
        return pd.DataFrame(params_dict).set_index('uID')
    
    def display(self):
        for k, v in self._params.items():
            print(k, ':', v)
            

class Club:
    
    def __init__(self, etree):
        self._etree=etree
        self._params = {}
        self._params['founded'] = self._etree.findall('Founded')[0].text

        for k, v in etree.items():
            self._params.update({k: v})
        if len(self._params.keys())>0:
            self.name=self._params['short_club_name']
            self.tID=self._params['uID']
        else:
            self.name=None
        
        self._params['symid'] = self._etree.findall('SYMID')[0].text
        
        self._player={}
        for p in self._etree.findall('Player'):
            player = Player(p)
            self._player[player.name] = player
            
    def get_player(self, playername):
        return self._player.get(playername)
    
    def get_info(self):
        params_dict = []
        for _, player in self._player.items():
            params_dict.append(player._params)
        df=pd.DataFrame(params_dict).set_index('uID')
        df['tID']=self.tID
        return df
    
    def display(self):
        for k, v in self._params.items():
            print(k, ':', v)
    
class Player:
    
    def __init__(self, etree):
        self._etree=etree
        self._params={}
        self._params.update(dict(self._etree.items()))
        self._params['name'] = self._etree.findall('Name')[0].text
        self.name = self._params['name']
        self._params['position'] = self._etree.findall('Position')[0].text
        for c in self._etree.findall('Stat'):
            _, stat = c.items()[0]
            self._params[stat] = c.text

            
    def display(self):
        for k, v in self._params.items():
            print(k, ':', v)
        
        
class TeamOfficial:
    # President, Manager
    
    def __init__(self, etree):
        pass
    
class TeamKits:
    
    def __init__(self, etree):
        pass
       
