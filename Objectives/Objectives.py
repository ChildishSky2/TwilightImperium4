import os
import sys
import random
import json

#parent_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
#sys.path.append(parent_dir)

import ImageCache
import Player
import Map


# Have  - Systems
# Own - Technologies
# Control - Planet
# Spend - Resources

class Objective:
    def __init__(self, ObjectiveValue, ObjectiveImage = None, ObjectiveName = None):
        self.ObjectiveValue : int = ObjectiveValue
        self.ObjectiveImage : ImageCache = ObjectiveImage
        self.ObjectiveName : str = ObjectiveName
        self.ObjectiveReqs = None

        self.ScoredBy = []
        pass
    pass

    def LoadRandomObjective(self, ExistingObjectives):

        if not os.path.exists(f"Objectives/{self.ObjectiveValue}Point"):
            print(f"Folder '{self.ObjectiveValue}Point' does not exist!")
            return False
        
        image_extensions = '.png'
        
        images = []

        for f in os.listdir(f"Objectives/{self.ObjectiveValue}Point"):
            TBA = True# Assume the file is a valid image until we check otherwise
            for Existing in ExistingObjectives:
                if Existing.ObjectiveName == os.path.splitext(f)[0]:
                    TBA = False
                    break

            if os.path.splitext(f)[1] in image_extensions and TBA:
                images.append(f.replace(".png", ""))
        
        if not images:
            print(f"No image files found in '{self.ObjectiveValue}Point'!")
            return False
        
        selected_file = random.choice(images)
        
        self.ObjectiveName = selected_file
        self.ObjectiveImage = ImageCache.ImageCache(f"Objectives/{self.ObjectiveValue}Point/{selected_file}.png", 50)

        json_file = f"Objectives/{self.ObjectiveValue}Point/{self.ObjectiveValue}Point.json"
        with open(json_file, 'r', encoding='utf-8') as f:
            self.ObjectiveReqs = json.load(f)[selected_file]
        pass

    def AttemptToScore(self, PlayerTrying : Player.Player, GameMap : Map.System) -> bool:
        if PlayerTrying.PlayerID in self.ScoredBy:
            return False
        match self.ObjectiveReqs['type']:
            case "Have":
                print("Have")
            case "Control":
                return self.__evalControlObjective(self, self.ObjectiveReqs['Filters'], PlayerTrying, GameMap)
            case "Own":
                
                pass
            case "Spend":
                if (self.ObjectiveReqs['Resources']  <= PlayerTrying.AvailableResources and 
                    self.ObjectiveReqs['Influence']  <= PlayerTrying.AvailableInfluence and 
                    self.ObjectiveReqs['TradeGoods'] <= PlayerTrying.TradeGoods and 
                    self.ObjectiveReqs['Tokens']    <= PlayerTrying.GetScoringTokens()):

                    PlayerTrying.AvailableResources -= self.ObjectiveReqs['Resources']
                    PlayerTrying.AvailableInfluence -= self.ObjectiveReqs['Influence']
                    PlayerTrying.TradeGoods         -= self.ObjectiveReqs['TradeGoods']

                    self.ScoredBy.append(PlayerTrying.PlayerID)
                    return True
        
        return False
    
    def __evalControlObjective(self, filters, PlayerTrying, GameMap):
        # Count planets that match the filters
        count = 0
        for tile in GameMap.Tiles:
            for planet in tile.Planets:
                if planet.OwnedBy == PlayerTrying.PlayerID:
                    if self.__matchesFilters(planet, filters):
                        count += 1

        if count >= self.ObjectiveReqs['Planets']:
            self.ScoredBy.append(PlayerTrying.PlayerID)
            return True
        return False

    def __matchesFilters(self, planet, filters):
        for key, value in filters.items():
            if key == "PlanetTrait":
                if not hasattr(planet, 'PlanetTrait') or planet.PlanetTrait != value:
                    return False
            elif key == "HasAttachment":
                if not hasattr(planet, 'HasAttachment') or planet.HasAttachment != value:
                    return False
            elif key == "IsNonHome":
                if not hasattr(planet, 'IsNonHome') or planet.IsNonHome != value:
                    return False
            elif key == "HasStructure":
                if not hasattr(planet, 'HasStructure') or planet.HasStructure != value:
                    return False
            elif key == "HasTechSpecialty":
                if not hasattr(planet, 'HasTechSpecialty') or planet.HasTechSpecialty != value:
                    return False
        return True
    
    def __repr__(self):
        return self.ObjectiveName