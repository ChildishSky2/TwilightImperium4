from abc import ABC, abstractmethod
from Game_Enums import UnitType, Race

class Race(ABC):
    @abstractmethod
    def __init__(self):

        self.RaceName = None

        self.PromissaryNote = None

        self.RaceStartingUnits = None

        self.StartingFleet : list[UnitType] = None

        self.Commodities = 0
        pass

    def __str__(self):
        return self.RaceName
    
    @abstractmethod
    def UniqueTechA(self):
        pass

    @abstractmethod
    def UniqueTechB(self):
        pass
        
    @abstractmethod
    def GetInitialTechs(self):
        return
    
    def GetRaceUnits(self):
        """Gets the upgraded units the faction beigns with"""
        return self.RaceStartingUnits
    
    def GetStartingFleet(self):
        return self.StartingFleet
    
    def GetRaceName(self):
        return self.RaceName

class Arborec(Race):
    # https://twilight-imperium.fandom.com/wiki/The_Arborec
    def __init__(self):
        self.RaceName = "Arborec"
        #All starting units for the player in their Home System
        self.StartingFleet = [UnitType.CARRIER, 
                              UnitType.CRUISER, 
                              UnitType.FIGHTER,
                              UnitType.FIGHTER,
                              UnitType.INFANTRY,
                              UnitType.INFANTRY,
                              UnitType.INFANTRY,
                              UnitType.INFANTRY,
                              UnitType.SPACE_DOCK,
                              UnitType.PDS]

        self.RaceStartingUnits = {
            UnitType.INFANTRY : (128, 0.5, 8),
            UnitType.FLAGSHIP : (8, (7, 7), 1, 5, True)
        }

        self.Commodities = 3
    
    def GetInitialTechs(self):
        return
    
    def UniqueTechA(self):
        #tech is blue, green, yellow, red
        return  "Letani Warrior 2", UnitType.INFANTRY, (128, 0.5, 7) ,(0, 2, 0, 0)
    
    def UniqueTechB(self):
        return "BioPlasmosis", None, None, (0, 2, 0, 0)
    
    def FactionHasAbilitiesInCurrentPhase(self):
        pass
    
    def ActiveFactionAbilities():
        pass


class Letnev(Race):
    #https://twilight-imperium.fandom.com/wiki/The_Barony_of_Letnev
    def __init__(self):
        self.RaceName = "Barony Of Letnev"

        #All starting units for the player in their Home System
        self.StartingFleet = [UnitType.DREADNOUGHT, 
                              UnitType.CARRIER, 
                              UnitType.DESTROYER,
                              UnitType.FIGHTER,
                              UnitType.INFANTRY,
                              UnitType.INFANTRY,
                              UnitType.INFANTRY,
                              UnitType.SPACE_DOCK
                              ]

        self.RaceStartingUnits = {
            UnitType.FLAGSHIP : (8, (7, 7), 1, 5, True)
        }

        self.Commodities = 2
    
    def GetInitialTechs(self):
        return
    
    def UniqueTechA(self):
        #tech is blue, green, yellow, red
        return  "L4 Disruptors", None, None, (0, 0, 1, 0)
    
    def UniqueTechB(self):
        return "Non-Euclidean Shielding", None, None, (0, 0, 0, 2)
    
    def FactionHasAbilitiesInCurrentPhase(self):
        pass
    
    def ActiveFactionAbilities():
        pass


class Lizix(Race):
    # https://twilight-imperium.fandom.com/wiki/The_Arborec
    def __init__(self):
        self.RaceName = "Lizix"


        #All starting units for the player in their Home System
        self.StartingFleet = [UnitType.DREADNOUGHT, 
                              UnitType.CARRIER, 
                              UnitType.FIGHTER,
                              UnitType.FIGHTER,
                              UnitType.FIGHTER,
                              UnitType.INFANTRY,
                              UnitType.INFANTRY,
                              UnitType.INFANTRY,
                              UnitType.INFANTRY,
                              UnitType.INFANTRY,
                              UnitType.SPACE_DOCK,
                              UnitType.PDS]

        self.RaceStartingUnits = {
            UnitType.DREADNOUGHT : (5, 5, 4, 2, 1, True),
            UnitType.FLAGSHIP : (8, (7, 7), 1, 5, True)
        }

        self.Commodities = 3
    
    def GetInitialTechs(self):
        return
    
    def UniqueTechA(self):
        #tech is blue, green, yellow, red
        return  "Super-Dreadnought II", UnitType.INFANTRY, (128, 0.5, 7) ,(0, 2, 0, 0)
    
    def UniqueTechB(self):
        return "Inheritance Systems", None, None, (0, 0, 2, 0)
    
    def FactionHasAbilitiesInCurrentPhase(self):
        pass
    
    def ActiveFactionAbilities():
        pass