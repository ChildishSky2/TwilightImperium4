from Game_Enums import Phases, TechnologyTypes, ActionPhase, MovementPhases, SpaceCombatPhases, InvasionPhases
from Phases import PhaseManager

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

    

