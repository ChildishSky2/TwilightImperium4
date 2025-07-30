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

        self.Infantry = 0
        self.OwnedBy = None#ID of owning player
        pass

    def __str__(self):
        return f"Planet {self.PlanetName} of type {self.PlanetType} with resources {self.Resources} and Influence {self.Influence}\n"

class Tile:
    #Represents a single System
    def __init__(self):
        self.Planets : list[Planet] = []

        self.ContainsAlpha : bool = False
        self.ContainsBeta : bool = False
        self.ContainsGamma : bool = False

        self.Anomaly = Anomalies.NoAnomaly

        self.TileNumber : int = -1

        self.TileImage : ImageCache = None

        self.ActivatedBy : list[int] = []

        #For controlling the current ships in the space area of the system
        self.ShipsInSpace : list[UnitType] = [UnitType.DREADNOUGHT, UnitType.CARRIER, UnitType.CRUISER, UnitType.WAR_SUN]
        self.InfantryInSpace : int = 2
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
    #For the map to be used in a game
    def __init__(self, max_rings=3):
        self.max_rings : int = max_rings
        self.Map : list[Tile | int] = ['18']
        self._generate_map()
        self._generate_hex_coordinate_mapping()
    
    def _generate_map(self):
        """Generate hexagonal map with rings from center outward"""
        self.Map.extend([None for _ in range(1, 3* self.max_rings * (self.max_rings + 1) + 1)])
    
    def _generate_hex_coordinate_mapping(self):
        """Generate mapping from array index to hex cube coordinates (x, y, z)"""
        self.index_to_coords = {}
        self.coords_to_index = {}
        
        # Center tile at origin
        index = 0
        self.index_to_coords[index] = (0, 0, 0)
        self.coords_to_index[(0, 0, 0)] = index
        index += 1
        
        # Generate coordinates for each ring
        for ring in range(1, self.max_rings + 1):
            # Start at the "top" of the ring
            x, y, z = 0, -ring, ring
            
            # Six directions in cube coordinates
            directions = [
                (1, 0, -1),   # SE
                (0, 1, -1),   # S
                (-1, 1, 0),   # SW
                (-1, 0, 1),   # NW
                (0, -1, 1),   # N
                (1, -1, 0)    # NE
            ]
            
            for direction in directions:
                dx, dy, dz = direction
                for _ in range(ring):
                    self.index_to_coords[index] = (x, y, z)
                    self.coords_to_index[(x, y, z)] = index
                    index += 1
                    x += dx
                    y += dy
                    z += dz
    
    def get_hex_coords(self, tile_index):
        """Get hex cube coordinates for a given tile index"""
        if tile_index not in self.index_to_coords:
            raise ValueError(f"Tile index {tile_index} is out of bounds")
        return self.index_to_coords[tile_index]
    
    def get_tile_index(self, hex_coords):
        """Get tile index for given hex cube coordinates"""
        if hex_coords not in self.coords_to_index:
            raise ValueError(f"Hex coordinates {hex_coords} are out of bounds")
        return self.coords_to_index[hex_coords]
    
    def get_tile_distance(self, tile1_index, tile2_index):
        """
        Calculate the distance between two tiles using their array indices.
        Returns the minimum number of steps to move from tile1 to tile2.
        """
        coords1 = self.get_hex_coords(tile1_index)
        coords2 = self.get_hex_coords(tile2_index)
        
        # Distance in cube coordinates is max of absolute differences
        x1, y1, z1 = coords1
        x2, y2, z2 = coords2
        
        distance = max(abs(x1 - x2), abs(y1 - y2), abs(z1 - z2))
        return distance
    
    def get_adjacent_tiles(self, tile_index):
        """Get all adjacent tile indices (distance 1)"""
        coords = self.get_hex_coords(tile_index)
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
            if neighbor_coords in self.coords_to_index:
                neighbors.append(self.coords_to_index[neighbor_coords])
        
        return neighbors
    
    def get_tiles_at_distance(self, tile_index, distance):
        """Get all tiles at exactly the specified distance"""
        if distance == 0:
            return [tile_index]
        
        tiles_at_distance = []
        for index in self.index_to_coords:
            if self.get_tile_distance(tile_index, index) == distance:
                tiles_at_distance.append(index)
        
        return tiles_at_distance
    
    def get_tiles_in_movement_range(self, tile_index, movement_points):
        """Get all tiles within the specified movement range (inclusive)"""
        tiles_in_range = []
        for index in self.index_to_coords:
            if self.get_tile_distance(tile_index, index) <= movement_points:
                tiles_in_range.append(index)
        
        return tiles_in_range
    
    def LoadMap(self, mode : Literal["Preset", "Auto", "Milty"] = "Auto", MapString : str = None):

        if mode == "Preset" and MapString == None:
            raise ValueError("Cannot create a map from given string")

        if mode == "Preset":
            System_Numbers = MapString.split(" ")
            for idx, system in enumerate(self.Map):
                if system != None:
                    continue
                self.Map[idx] = int(System_Numbers[idx])
        
        if mode == "Auto":
            with open("Systems.json", 'r') as file:
                data = json.load(file)

            available_systems = set(data.keys())
            available_systems.remove('18')
            
            for idx, system in enumerate(self.Map):
                if system != None:#if already present
                    continue

                if not available_systems:
                    raise LookupError("No more unique systems available")
                
                SelectedSystem = random.choice(list(available_systems))
                available_systems.remove(SelectedSystem)
            
                self.Map[idx] = SelectedSystem
            
            #load all tiles selected including mecatol rex and mallice
            for idx, system in enumerate(self.Map):
                tile = Tile()
                tile.LoadSystemFromData(data, system)
                self.Map[idx] = tile
        
        if mode == "Milty":
            raise ValueError("Mode under development")
        pass

    def SetHomeSystems(self, RaceList : list[str]):
        num_players = len(RaceList)
        match num_players:
            case 4:
                positions = [4, 8, 13, 17]
            case 5:
                positions = [0, 3, 7, 11, 15]
            case 6:
                positions = [0, 3, 6, 9, 12, 15]
            case _:
                raise ValueError("Unable to have gae with given numbner of players")
    

        for pos, Race in zip(positions, RaceList):
            T = Tile()
            T.TileImage = ImageCache(f"Races\\{''.join(Race.split(" "))}\\HomeSystem.jpg", 50)
            self.Map[-(pos+1)] = T
            pass
        pass
