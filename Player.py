# Player will have list of planets
# List of techs
# Units

from ImageCache import ImageCache
import Race
import random

class Player:
    def __init__(self, ID):
        self.PlayerID = ID

        self.PlayerName : str = "AlmondSpring250"
        self.Colour : tuple = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        self.Race : Race = None

        self.VP : int = random.randint(0, 10) # initial victory points - always starts at 0
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

        self.OwnerToken : ImageCache = None

        self.Resources          : int = 10
        self.AvailableResources : int = 10
        self.Influence          : int = 10
        self.AvailableInfluence : int = 10


        self.CommodityLimit = 0
        self.Commodities    = 0
        self.TradeGoods     = 10

        self.SetRace(random.choice(self.GetRaceOptions()))


        self.PlayerHand = []
        pass

    def __eq__(self, Another_Player):
        if not isinstance(Another_Player, Player):
            raise TypeError(f"Unable to Compare Player object with type {type(Another_Player)}")
        
        return self.PlayerID == Another_Player.PlayerID
    
    def GetRaceOptions(self):
        return Race.GetRaceOptions()
    
    def SetRace(self, RaceName):
        assert RaceName in self.GetRaceOptions(), f"Race '{RaceName}' is not a valid option! Valid options are: {', '.join(self.GetRaceOptions())}"
        self.Race = Race.Race(RaceName)
        self.Token = ImageCache(f"Assets\\RaceItems\\{RaceName.replace(' ', '_')}\\TacticsToken.png", 10)
        self.OwnerToken = ImageCache(f"Assets\\RaceItems\\{RaceName.replace(' ', '_')}\\OwnerToken.png", 10)

        

    def GetTokenImg(self, radius):
        return self.Token.get_scaled_tile(radius)
    
    def GetOwnerTokenImg(self, radius):
        return self.OwnerToken.get_scaled_tile(radius)
    
    def Select_Strategy_Cards(self, CardID):
        #sets strategy card for player
        self.StrategyCard = CardID
        pass

    def GetPlayerColour(self):
        return self.Colour

    def GetScoringTokens(self):
        return self.TacticsTokens + self.StrategyTokens