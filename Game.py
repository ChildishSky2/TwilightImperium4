#need to represent game board
#hexagonal pieces

import Map
import Player
import Technologies
import BasicUnits
from typing import Literal
from Phases import PhaseManager
import json
#https://www.redblobgames.com/grids/hexagons/

from Objectives.Objectives import Objective
# Controls the game and acts as a manager for the map, players and units

class Game:
    def __init__(self, VPtoWin : Literal[10, 14]):
        self.Map : Map.System = None
        
        #player will be none is not in use
        self.Players : list[Player.Player] = None
        self.SetPlayerNumbers(6)
        self.VPtoWin : int = VPtoWin

        self.Turn = 0 # idx of the current player to action game
        self.PhaseManager : PhaseManager = PhaseManager("Status") # go through all phases of the turn

        self.Speaker = 2 # idx of current speaker

        self.SelectedSystem    : int = None
        self.SelectedStratCard : int = None
        self.SelectedObjective : int = None

        self.ActiveSystem : int = None

        self.PublicObjectives = [[], []]
        self.AddNewPublicObjective()
        self.AddNewPublicObjective()

        self.AvailableGeneralTechs = self._LoadTechs()

        self.UnitManager = BasicUnits.UnitManager()
        #print(self.PublicObjectives)
        pass

    def SetPlayerNumbers(self, NumberOfPlayers):
        self.Players = [Player.Player(i) for i in range(NumberOfPlayers)]
    
    def GetNumberOfPlayers(self):
        return len(self.Players)
    
    def GenerateMap(self):
        self.Map = Map.System()
        self.Map.LoadMap("Auto")

        self.Map.SetHomeSystems([i.Race.RaceName for i in self.Players])

    def Pass(self):
        self.Players[self.Turn].Passed = True
        self.EndTurn()

    def EndTurn(self):
        start_turn = self.Turn
    
        while True:
            self.Turn = (self.Turn + 1) % len(self.Players)
        
            # If we found an active player or completed a full loop, break
            if not self.Players[self.Turn].Passed or self.Turn == start_turn:
                break
        self.ActiveSystem = None

    def SelectSystem(self, system_idx : int):
        self.SelectedSystem = system_idx

    def ActivateSystem(self):
        self.ActiveSystem = self.SelectedSystem
        self.Map.Map[self.ActiveSystem].ActivateSystem(self.Turn)
        self.Players[self.Turn].TacticsTokens -= 1

        self.PhaseManager.SetTurnActionType("Tactical")

    def _LoadTechs(self): 
        self.AvailableTechs = [] 
        with open("Technologies.json", "r", encoding="utf-8") as file: 
            tech_data = json.load(file) 
            for tech_id, tech in tech_data.items(): 
                prereqs = tech["Prerequisites"] 
                ty = Technologies.TechnologyTypes
                ty.value = tech["Type"]

                self.AvailableTechs.append( 
                    Technologies.Technology( 
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
    
    def GetPlayerColour(self, PlayerID):
        return self.Players[PlayerID].GetPlayerColour()
    
    def ConfirmStratCard(self):
        self.Players[self.Turn].Select_Strategy_Cards(self.SelectedStratCard)

    def AddNewPublicObjective(self):
        if len(self.PublicObjectives[0]) < 5:
            New_Obj = Objective(1)
            New_Obj.LoadRandomObjective(self.PublicObjectives[0])
            self.PublicObjectives[0].append(New_Obj)

            return
        
        if len(self.PublicObjectives[1]) < 5:
            New_Obj = Objective(2)
            New_Obj.LoadRandomObjective(self.PublicObjectives[1])
            self.PublicObjectives[1].append(New_Obj)

            return
    
