from Game_Enums import Phases, Tactical_Action_Phases, ActionType
from typing import Literal

class PhaseManager:
    def __init__(self, MainPhase : Literal["Strategy", "Action", "Status", "Agenda"] = "Strategy", SubPhase = None):
        self.MainPhase : Phases = MainPhase

        self.ActionType: ActionType = SubPhase # Strategic, tactical or Component


        self.SubPhaseAction : Tactical_Action_Phases = None #Actions for Tactical action
        pass

    def NewPlayersTurn(self):
        self.ActionType = None
        self.SubPhaseAction = Tactical_Action_Phases.Start_Turn
    
    def SetTurnActionType(self, Action_Type : Literal["Strategic", "Tactical", "Component"]):
        self.ActionType = ActionType[Action_Type]

        if Action_Type == "Tactical":
            self.SubPhaseAction = Tactical_Action_Phases.Movement
