#need to represent game board
#hexagonal pieces

import Map
import Player
import Technologies
import BasicUnits
from Phases import PhaseManager
#https://www.redblobgames.com/grids/hexagons/

import json
import random
# Controls the game and acts as a manager for the map, players and units

class Game:
    def __init__(self, VPtoWin):
        self.Map : Map.System = None
        
        #player will be none is not in use
        self.Players : list[Player.Player] = None
        self.VPtoWin : int = VPtoWin

        self.Turn = 0 # idx of the current player to action game
        self.PhaseManager : PhaseManager = PhaseManager("Action") # go through all phases of the turn

        self.Speaker = 2 # idx of current speaker

        self.SelectedSystem : int = None
        self.ActiveSystem : int = None

        self.PublicObjectives = [[], []]
        self.AddPublicObjective()
        self.AddPublicObjective()

        self.AvailableGeneralTechs = self._LoadTechs()

        self.UnitManager = BasicUnits.UnitManager()
        pass

    def SetPlayerNumbers(self, NumberOfPlayers):
        self.Players = [Player.Player(i) for i in range(NumberOfPlayers)]
    
    def GetNumberOfPlayers(self):
        return len(self.Players)
    
    def GenerateMap(self):
        self.Map = Map.System()
        self.Map.LoadMap("Auto")

        self.Map.SetHomeSystems([i.Race.RaceName for i in self.Players])

    def AddPublicObjective(self):
        def Load(self, file):
            data = json.load(file)
            chosen = random.randint(1, len(data))
            while data.get(str(chosen)) in self.PublicObjectives[0]:
                chosen = random.randint(1, len(data))
            self.PublicObjectives[0].append(data.get(str(chosen)))

        if len(self.PublicObjectives[0]) < 5:
            with open("Objectives\\Objectives_1Point.json", "r") as file:
                Load(self, file)

        elif len(self.PublicObjectives[1]) < 5:
            with open("Objectives\\Objectives_2Point.json", "r") as file:
                Load(self, file)

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
    