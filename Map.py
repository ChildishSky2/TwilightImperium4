from typing import Literal
import json
import random

from Game_Enums import PlanetTypes, Anomalies, UnitType
from ImageCache import ImageCache
#Map - contains information on each tile and how they all link together, as well as details of planets in the tiles

class Planet:
    #Represents an individual Planet in a system
    def __init__(self, PlanetName: str, PlanetType: PlanetTypes, Resources : int, Influence : int):
        self.PlanetName = PlanetName

        self.Resources = Resources
        self.Influence = Influence
        self.PlanetType = PlanetTypes[PlanetType]

        self.Tapped = True

        self.Infantry = 1
        self.Mechs = 1
        self.OwnedBy = random.randint(0, 4)#ID of owning player
        pass

    def __str__(self):
        return f"Planet {self.PlanetName} of type {self.PlanetType} with resources {self.Resources} and Influence {self.Influence}\n"

class Tile:
    #Represents a single System with location on hexagonal grid
    def __init__(self, system_id: int = -1, hex_coords: tuple[int, int, int] = None):
        self.SystemID : int = system_id
        self.HexCoords : tuple[int, int, int] = hex_coords or (0, 0, 0)
        
        self.Planets : list[Planet] = []

        self.ContainsAlpha : bool = False
        self.ContainsBeta : bool = False
        self.ContainsGamma : bool = False

        self.Anomaly = Anomalies.NoAnomaly

        self.TileNumber : int = system_id

        self.TileImage : ImageCache = None

        self.ActivatedBy : list[int] = []

        #For controlling the current ships in the space area of the system
        self.ShipsInSpace : list[UnitType] = []
        self.InfantryInSpace : int = 1
        self.MechsInSpace : int = 1
        self.ShipOwner = 1
    
    def ActivateSystem(self, PlayerID : int):
        self.ActivatedBy.append(PlayerID)

    def LoadSystem(self, TileNumber):
        """Gets data froma specified systme number from loading the systems.json file"""
        # loads an individual system - to add new function to load all systems in single pass
        self.Tile = TileNumber
        self.TileImage = ImageCache.ImageCache(f"System_Tiles\\{str(TileNumber)}.jpg", 50)

        with open("Systems.json", 'r') as file:
            data = json.load(file)
            System = data.get(str(TileNumber))

            if System == None:#Empty System
                raise KeyError(f"Unable to locate system with id {TileNumber}: Make sure that this system exists in the list of systems in Systems.json")
            
            for item in System:
                match item[0]:
                    case "Planet":
                        self.Planets.append(Planet(*item[1:]))

                    case "Wormhole":
                        if item[1] == "Alpha":
                            self.ContainsAlpha = True
                        if item[1] == "Beta":
                            self.ContainsBeta = True

                    case "Anomaly":
                        try:
                            self.Anomaly = Anomalies[item[1]]
                        except KeyError:
                            print(f"Warning: Unknown anomaly type: {item[1]}")
                            self.Anomaly = Anomalies.NoAnomaly
        return
    
    def __str__(self):
        return f"System contains {len(self.Planets)} Planet(s) {"and a wormhole" if self.ContainsAlpha or self.ContainsBeta or self.ContainsGamma else "and no wormholes"}\n"
    
    def __repr__(self):
        return str(self.TileNumber)

    def LoadSystemFromData(self, SystemsData, TileNumber):
        """Gets data from the loaded SystemsData information"""
        self.TileNumber = TileNumber

        if System == None:#Empty System
            raise KeyError(f"Unable to locate system with id {TileNumber}: Make sure that this system exists in the list of systems in Systems.json")
        
        self.TileImage = ImageCache(f"System_Tiles\\{str(TileNumber)}.jpg", 50)

        for item in SystemsData[str(TileNumber)]:
            if item is None:
                continue

            match item[0]:
                case "Planet":
                    self.Planets.append(Planet(*item[1:]))

                case "Wormhole":
                    if item[1] == "Alpha":
                        self.ContainsAlpha = True
                    if item[1] == "Beta":
                        self.ContainsBeta = True

                case "Anomaly":
                    try:
                        self.Anomaly = Anomalies[item[1]]
                    except KeyError:
                        print(f"Warning: Unknown anomaly type: {item[1]}")
                        self.Anomaly = Anomalies.NoAnomaly

    def LoadSystem(self, TileNumber):
        """Gets data from a specified system number from loading the systems.json file"""
        # loads an individual system - to add new function to load all systems in single pass
        self.Tile = TileNumber
        self.TileImage = ImageCache(f"System_Tiles\\{str(TileNumber)}.jpg", 50)
        
        with open("Systems.json", 'r') as file:
            data = json.load(file)
            System = data.get(str(TileNumber))

            if System == None:#Empty System
                raise KeyError(f"Unable to locate system with id {TileNumber}: Make sure that this system exists in the list of systems in Systems.json")
            
            for item in System:
                match item[0]:
                    case "Planet":
                        self.Planets.append(Planet(*item[1:]))

                    case "Wormhole":
                        if item[1] == "Alpha":
                            self.ContainsAlpha = True
                        if item[1] == "Beta":
                            self.ContainsBeta = True

                    case "Anomaly":
                        try:
                            self.Anomaly = Anomalies[item[1]]
                        except KeyError:
                            print(f"Warning: Unknown anomaly type: {item[1]}")
                            self.Anomaly = Anomalies.NoAnomaly
        return

    def GetPlayersWhoActivatedSystem(self):
        return self.ActivatedBy

    def CheckPlayerHasActivatedSystem(self, PlayerID : int):
        return PlayerID in self.ActivatedBy

    def GetTileNumber(self):
        return self.TileNumber

    def GetShipsInSystem(self):
        return self.ShipsInSpace

class System:
    #Represents the hexagonal game map with all systems and their positions
    def __init__(self, max_rings: int = 3):
        self.max_rings: int = max_rings
        self.tiles: list[Tile] = []  # List of tiles in order (index = position on map)
        self.tile_to_coords: dict[Tile, tuple[int, int, int]] = {}  # Maps tile objects to hex coordinates
        self.coords_to_tile: dict[tuple[int, int, int], Tile] = {}  # Maps hex coordinates to tile
        
    def add_tile(self, tile: Tile, hex_coords: tuple[int, int, int]):
        """Add a tile at the specified hex coordinates"""
        tile.HexCoords = hex_coords
        self.tiles.append(tile)
        self.tile_to_coords[tile] = hex_coords
        self.coords_to_tile[hex_coords] = tile
    
    def get_tile_coords(self, tile: Tile) -> tuple[int, int, int]:
        """Get hex coordinates for a tile"""
        if tile not in self.tile_to_coords:
            raise KeyError("Tile not found on map")
        return self.tile_to_coords[tile]
    
    def calculate_distance(self, tile1: Tile, tile2: Tile) -> int:
        """
        Calculate the shortest distance between two tiles on the hexagonal grid.
        Uses cube coordinates where distance = max(|x1-x2|, |y1-y2|, |z1-z2|)
        """
        if tile1 is tile2:
            return 0
        
        coords1 = self.get_tile_coords(tile1)
        coords2 = self.get_tile_coords(tile2)
        
        x1, y1, z1 = coords1
        x2, y2, z2 = coords2
        
        distance = max(abs(x1 - x2), abs(y1 - y2), abs(z1 - z2))
        return distance
    
    def get_adjacent_tiles(self, tile: Tile) -> list[Tile]:
        """Get all adjacent tiles (distance 1)"""
        coords = self.get_tile_coords(tile)
        x, y, z = coords
        
        # Six directions in cube coordinates
        directions = [
            (1, 0, -1),   # SE
            (0, 1, -1),   # S
            (-1, 1, 0),   # SW
            (-1, 0, 1),   # NW
            (0, -1, 1),   # N
            (1, -1, 0)    # NE
        ]
        
        neighbors = []
        for dx, dy, dz in directions:
            neighbor_coords = (x + dx, y + dy, z + dz)
            if neighbor_coords in self.coords_to_tile:
                neighbors.append(self.coords_to_tile[neighbor_coords])
        
        return neighbors
    
    def get_tiles_at_distance(self, tile: Tile, distance: int) -> list[Tile]:
        """Get all tiles at exactly the specified distance"""
        if distance < 0:
            return []
        if distance == 0:
            return [tile]
        
        tiles_at_distance = []
        for other_tile in self.tiles:
            if self.calculate_distance(tile, other_tile) == distance:
                tiles_at_distance.append(other_tile)
        
        return tiles_at_distance
    
    def get_tiles_in_range(self, tile: Tile, distance: int) -> list[Tile]:
        """Get all tiles within the specified distance (inclusive)"""
        tiles_in_range = []
        for other_tile in self.tiles:
            if self.calculate_distance(tile, other_tile) <= distance:
                tiles_in_range.append(other_tile)
        
        return tiles_in_range
    
    def find_path(self, start_tile: Tile, end_tile: Tile) -> list[Tile]:
        """
        Find the shortest path between two tiles using breadth-first search.
        Returns a list of tiles from start to end (inclusive).
        """
        if start_tile is end_tile:
            return [start_tile]
        
        if start_tile not in self.tile_to_coords or end_tile not in self.tile_to_coords:
            raise KeyError("One or both tiles not found on map")
        
        from collections import deque
        
        queue = deque([(start_tile, [start_tile])])
        visited = {start_tile}
        
        while queue:
            current_tile, path = queue.popleft()
            
            for neighbor_tile in self.get_adjacent_tiles(current_tile):
                if neighbor_tile is end_tile:
                    return path + [neighbor_tile]
                
                if neighbor_tile not in visited:
                    visited.add(neighbor_tile)
                    queue.append((neighbor_tile, path + [neighbor_tile]))
        
        raise ValueError("No path found between the two tiles")
    
    def LoadMap(self, mode : Literal["Preset", "Auto", "Milty"] = "Auto", MapString : str = None):

        if mode == "Preset" and MapString == None:
            raise ValueError("Cannot create a map from given string")

        if mode == "Preset":
            System_Numbers = MapString.split(" ")
            for idx, system in enumerate(self.tiles):
                if system != None:
                    continue
                # This mode would need updating for new structure
                raise NotImplementedError("Preset mode needs updating for new System class")
        
        if mode == "Auto":
            with open("Systems.json", 'r') as file:
                data = json.load(file)

            available_systems = set(data.keys())
            available_systems.discard('18')
            
            # Generate a basic circular layout
            systems_to_place = ['18'] + list(available_systems)
            
            # Place center system at origin
            center_tile = Tile()
            center_tile.LoadSystemFromData(data, '18')
            self.add_tile(center_tile, (0, 0, 0))
            
            # Place remaining systems in a spiral pattern
            index = 1
            for ring in range(1, self.max_rings + 1):
                x, y, z = 0, -ring, ring
                directions = [
                    (1, 0, -1),   # SE
                    (0, 1, -1),   # S
                    (-1, 1, 0),   # SW
                    (-1, 0, 1),   # NW
                    (0, -1, 1),   # N
                    (1, -1, 0)    # NE
                ]
                
                for dx, dy, dz in directions:
                    for _ in range(ring):
                        if index >= len(systems_to_place):
                            break
                        
                        system_id = systems_to_place[index]
                        tile = Tile()
                        tile.LoadSystemFromData(data, system_id)
                        self.add_tile(tile, (x, y, z))
                        
                        x += dx
                        y += dy
                        z += dz
                        index += 1
                    
                    if index >= len(systems_to_place):
                        break
                
                if index >= len(systems_to_place):
                    break
        
        if mode == "Milty":
            raise ValueError("Mode under development")

    def SetHomeSystems(self, RaceList : list[str]):
        print(f"Setting home systems for races: {', '.join(RaceList)}")
        num_players = len(RaceList)
        match num_players:
            case 4:
                positions = [4, 8, 13, 17]
            case 5:
                positions = [3, 7, 11, 15, 18]
            case 6:
                positions = [3, 6, 9, 12, 15, 18]
            case _:
                raise ValueError("Unable to have game with given number of players")
    
        for pos, Race in zip(positions, RaceList):
            self.tiles[len(self.tiles) - pos].TileImage = ImageCache(f"Assets\\RaceItems\\{Race.replace(' ', '_')}\\HomeSystem.png", 50)
