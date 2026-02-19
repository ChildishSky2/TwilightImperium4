from Game_Enums import Phases, ActionType, ActionPhase, MovementPhases, SpaceCombatPhases, InvasionPhases
from typing import Literal

class PhaseManager:
    def __init__(self, MainPhase : Phases = "Strategy", SubPhase = None):
        self.MainPhase : Phases = MainPhase

        self.ActionType: ActionType = SubPhase # Strategic, tactical or Component


        self.SubPhaseAction = None #Actions for Tactical action
        self.SubPhaseProgress = None
        pass

    def NewPlayersTurn(self):
        self.ActionType = None
        self.SubPhaseAction = ActionPhase.Start_Turn

    
    def SetTurnActionType(self, Action_Type : Literal["Strategic", "Tactical", "Component"]):
        self.ActionType = ActionType[Action_Type]

        if Action_Type == "Tactical":
            self.SubPhaseAction = ActionPhase.Movement
    
    def SetMinorPhase(self, PhaseToBeSet : MovementPhases | SpaceCombatPhases | InvasionPhases):
        self.SubPhaseProgress = PhaseToBeSet
    
    def SetMajorPhase(self, PhaseToBeSet : ActionPhase):
        self.SubPhaseAction = PhaseToBeSet
