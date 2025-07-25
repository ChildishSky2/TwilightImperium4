from enum import Enum

class TechnologyTypes(Enum):
    Propulsion = 1
    Cybernetic = 2
    Biological = 3
    Warfare = 4

class ActivationPoint(Enum):
    When_SystemActivation = 1
    After_SystemActivation = 1
    During_Movement = 2
    After_Movement = 3
    Start_SpaceCombat = 4
    Start_Round_SpaceCombat = 5
    End_Round_SpaceCombat = 6
    Start_Invasion = 7
    Start_GroundCombat = 8
    Start_Round_GroundCombat = 9
    End_Round_GroundCombat = 10
    Capture_Planet = 11
    Production = 12
    EndOfTurn = 13

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
    
    def DoesTechActvate(self, Phase : ActivationPoint):
        return Phase in self.ActivationWindow

    

