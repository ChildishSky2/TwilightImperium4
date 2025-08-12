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
            TBA = True
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

        print(self.ObjectiveReqs)
        pass

    def AttemptToScore(self, PlayerTrying : Player.Player, GameMap : Map.System) -> bool:
        if PlayerTrying.PlayerID in self.ScoredBy:
            return False
        match self.ObjectiveReqs['type']:
            case "Have":
                print("Have")
            case "Control":
                print("Control")
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
    
    
    def __repr__(self):
        return self.ObjectiveName