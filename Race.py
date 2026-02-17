from abc import ABC, abstractmethod
from Game_Enums import UnitType, Race
import os

def GetRaceOptions():
    path = "Assets\\RaceItems"
    races   = [i.replace("_", " ") for i in os.listdir(path) if os.path.isdir(os.path.join(path, i))]
    return races

class Race():
    def __init__(self, RaceName : str):

        self.RaceName = RaceName

        self.PromissaryNote = None

        self.RaceStartingUnits = None

        self.StartingFleet : list[UnitType] = None

        self.Commodities = 0

        self.UniqueTechA = None
        self.UniqueTechB = None
        pass

    def __str__(self):
        return self.RaceName
    
    def SetRace(self, RaceName : str):
        path = f"Assets\\RaceItems\\{RaceName.replace(' ', '_')}"
        if not os.path.exists(path):
            raise ValueError(f"Race '{RaceName}' does not exist!")
        
        self.RaceName = RaceName

    
    def UniqueTechA(self):
        pass

    def UniqueTechB(self):
        pass
        
    def GetInitialTechs(self):
        return
    
    def GetRaceUnits(self):
        """Gets the upgraded units the faction beigns with"""
        return self.RaceStartingUnits
    
    def GetStartingFleet(self):
        return self.StartingFleet
    
    def GetRaceName(self):
        return self.RaceName