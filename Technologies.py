from enum import Enum
from Game_Enums import Tactical_Action_Phases
class TechnologyTypes(Enum):
    Propulsion = 1
    Cybernetic = 2
    Biological = 3
    Warfare = 4

#technologies.txt - 
#write out the technologies as equations
class Technology:
    def __init__(self, TechName : str, TechType : TechnologyTypes, Blue_Prerequisites : int, Green_Prerequisites : int, Yellow_Prerequisites : int, Red_Prerequisites : int):
        self.TechnologyName = TechName
        self.TechType = TechType

        self.BlueReqs = Blue_Prerequisites
        self.GreenReqs = Green_Prerequisites
        self.YellowReqs = Yellow_Prerequisites
        self.RedReqs = Red_Prerequisites


    def __repr__(self):
        return self.TechnologyName

    def HasPreRequisites(self, Blue_Prerequisites, Green_Prerequisites, Yellow_Prerequisites, Red_Prerequisites):
        """Checks whether a player has the prerequisites"""
        return (Blue_Prerequisites <= self.BlueReqs and
                Green_Prerequisites <= self.GreenReqs and
                Yellow_Prerequisites <= self.YellowReqs and 
                Red_Prerequisites <= self.RedReqs)
    
    def DoesTechActivate(self, Phase : Tactical_Action_Phases):
        return Phase in self.ActivationWindow

    

