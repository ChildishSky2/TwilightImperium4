#need to represent game board
#hexagonal pieces

import Map
import Player
import Technologies
import BasicUnits
from typing import Literal
from Phases import PhaseManager
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
        self.PhaseManager : PhaseManager = PhaseManager("Strategy") # go through all phases of the turn

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
        Techs = []
        with open("Technologies.txt", "r") as file:
            line = file.readline().strip()
            while line != "":
                t = line.split(", ")
                tech = Technologies.Technology(*t)
                Techs.append(tech)

                line = file.readline().strip()
        return Techs
    
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