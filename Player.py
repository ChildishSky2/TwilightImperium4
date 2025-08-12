# Player will have list of planets
# List of techs
# Units

from ImageCache import ImageCache
import Race
from typing import Literal
import random

class Player:
    def __init__(self, ID):
        self.PlayerID = ID

        self.PlayerToken = None

        self.PlayerName : str = "AlmondSpring250"
        self.Colour : tuple = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        self.Race : Race = None
        
        self.SetRace(random.choice(["Arborec", "BaronyOfLetnev", "Lizix"]))

        self.VP : int = 0 # initial victory points - always starts at 0
        self.StrategyCard = None
        self.Priority = None

        self.Eliminated = False
        self.Passed     = False

        self.PropulsionTechs  : list = []
        self.BiologicalTechs  : list = []
        self.CyberneticTechs  : list = []
        self.WarfareTechs     : list = []
        self.UnitTechnologies : list = []

        self.TotalTechs = 0

        self.TacticsTokens  = 3
        self.FleetTokens    = 3
        self.StrategyTokens = 2

        self.Token : ImageCache = None
        self.SetStrategyToken()

        self.OwnerToken : ImageCache = None

        self.Resources          : int = 10
        self.AvailableResources : int = 10
        self.Influence          : int = 10
        self.AvailableInfluence : int = 10


        self.CommodityLimit = 0
        self.Commodities    = 0
        self.TradeGoods     = 10
        pass

    def __eq__(self, Another_Player):
        if not isinstance(Another_Player, Player):
            raise TypeError(f"Unable to Compare Player object with type {type(Another_Player)}")
        
        return self.PlayerID == Another_Player.PlayerID
    
    def SetRace(self, RaceName : Literal["Arborec", "BaronyOfLetnev", "Lizix"]):
        match RaceName:
            case "Arborec":
                self.Race = Race.Arborec()
            case "BaronyOfLetnev":
                self.Race = Race.Letnev()
            case "Lizix":
                self.Race = Race.Lizix()
    
    def SetStrategyToken(self, path = "Assets\\RaceItems\\TacticsToken.png"):
        self.Token = ImageCache(path, 10)

    def GetTokenImg(self, radius):
        return self.Token.get_scaled_tile(radius)
    
    def Select_Strategy_Cards(self, CardID):
        #sets strategy card for player
        self.StrategyCard = CardID
        pass

    def GetPlayerColour(self):
        return self.Colour

    def GetScoringTokens(self):
        return self.TacticsTokens + self.StrategyTokens