from Game_Enums import Phases, TechnologyTypes, ActionPhase, MovementPhases, SpaceCombatPhases, InvasionPhases
from Phases import PhaseManager
import json

#write out the technologies as equations
class Technology:
    def __init__(self, TechID : int, TechName : str, TechType : TechnologyTypes, Blue_Prerequisites : int, Green_Prerequisites : int, Yellow_Prerequisites : int, Red_Prerequisites : int, Effect : str | dict = None, IsUnitUpgrade : bool = False, UnitStats : dict | None = None):
        self.TechID = TechID
        self.TechnologyName = TechName
        self.TechType = TechType

        self.BlueReqs = Blue_Prerequisites
        self.GreenReqs = Green_Prerequisites
        self.YellowReqs = Yellow_Prerequisites
        self.RedReqs = Red_Prerequisites

        self.Effect = Effect
        self.IsUnitUpgrade = IsUnitUpgrade
        self.UnitStats = UnitStats

        self.ActivationWindowMajorPhase : set[Phases | ActionPhase] = set()
        self.ActivationWindowMinorPhase : set[MovementPhases | SpaceCombatPhases | InvasionPhases] = set()

    def LoadGeneralTechs():
        AvailableTechs = []
        with open("Technologies.json", "r", encoding="utf-8") as file: 
            tech_data = json.load(file) 
            for tech_id, tech in tech_data.items(): 
                prereqs = tech["Prerequisites"] 
                ty = TechnologyTypes
                ty.value = tech["Type"]

                AvailableTechs.append( 
                    Technology( 
                        TechID=int(tech_id), 
                        TechName=tech["TechName"], 
                        TechType=ty, 
                        Blue_Prerequisites=prereqs["B"], 
                        Green_Prerequisites=prereqs["G"], 
                        Yellow_Prerequisites=prereqs['Y'], 
                        Red_Prerequisites=prereqs["R"], 
                        Effect=tech.get("Effect", None), 
                        IsUnitUpgrade=tech.get("IsUnitUpgrade", False), 
                        UnitStats=tech.get("UnitStats", None) )
                        )
        return AvailableTechs


    def __repr__(self):
        return self.TechnologyName

    def HasPreRequisites(self, Blue_Prerequisites, Green_Prerequisites, Yellow_Prerequisites, Red_Prerequisites):
        """Checks whether a player has the prerequisites"""
        return (Blue_Prerequisites <= self.BlueReqs and
                Green_Prerequisites <= self.GreenReqs and
                Yellow_Prerequisites <= self.YellowReqs and
                Red_Prerequisites <= self.RedReqs)
    
    def DoesTechActivate(self, Phase : PhaseManager):
        return

    

