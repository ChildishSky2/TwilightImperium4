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

    def AwardScore(self, PlayerTrying : Player.Player) -> bool:
        PlayerTrying.VP += self.ObjectiveValue
        self.ScoredBy.append(PlayerTrying.PlayerID)
        if hasattr(PlayerTrying, 'ScoredObjectives'):
            PlayerTrying.ScoredObjectives.append(self)
        return True

    def _count_player_technologies(self, PlayerTrying : Player.Player) -> int:
        return (
            len(PlayerTrying.PropulsionTechs)
            + len(PlayerTrying.BiologicalTechs)
            + len(PlayerTrying.CyberneticTechs)
            + len(PlayerTrying.WarfareTechs)
            + len(PlayerTrying.UnitTechnologies)
        )

    def _count_player_technology_colors(self, PlayerTrying : Player.Player) -> dict:
        return {
            'B': len(PlayerTrying.PropulsionTechs),
            'G': len(PlayerTrying.BiologicalTechs),
            'Y': len(PlayerTrying.CyberneticTechs),
            'R': len(PlayerTrying.WarfareTechs),
        }

    def _count_player_ship_systems(self, PlayerTrying : Player.Player, GameMap : Map.System) -> int:
        count = 0
        for tile in GameMap.tiles:
            if tile.ShipOwner == PlayerTrying.PlayerID and len(tile.ShipsInSpace) > 0:
                count += 1
        return count

    def _player_has_unit_type(self, PlayerTrying : Player.Player, GameMap : Map.System, wanted_types: list[str]) -> bool:
        for tile in GameMap.tiles:
            if tile.ShipOwner != PlayerTrying.PlayerID:
                continue
            for unit in tile.ShipsInSpace:
                if unit.value in wanted_types or unit.name in wanted_types:
                    return True
        return False

    def _evalHaveObjective(self, reqs, PlayerTrying : Player.Player, GameMap : Map.System) -> bool:
        resource = reqs.get('Resource')
        quantity = reqs.get('Quantity')
        conditions = reqs.get('Conditions', []) or []

        if isinstance(quantity, str) and quantity.isdigit():
            quantity = int(quantity)

        if resource in ('Ships', 'Units'):
            count = self._count_player_ship_systems(PlayerTrying, GameMap)
            if 'Do not contain Planets' in conditions:
                count = 0
                for tile in GameMap.tiles:
                    if tile.ShipOwner == PlayerTrying.PlayerID and len(tile.ShipsInSpace) > 0 and len(tile.Planets) == 0:
                        count += 1
            if count >= quantity:
                return self.AwardScore(PlayerTrying)
            return False

        if resource == 'War Sun||FlagShip':
            if self._player_has_unit_type(PlayerTrying, GameMap, ['WarSun', 'Flagship']):
                return self.AwardScore(PlayerTrying)
            return False

        if resource == 'Structures':
            count = 0
            for tile in GameMap.tiles:
                for planet in tile.Planets:
                    if getattr(planet, 'OwnedBy', None) == PlayerTrying.PlayerID and getattr(planet, 'HasStructure', False):
                        if 'IsNonHome' in reqs.get('Filters', {}) and getattr(planet, 'IsNonHome', False) != reqs['Filters']['IsNonHome']:
                            continue
                        count += 1
            if count >= quantity:
                return self.AwardScore(PlayerTrying)
            return False

        print(f"Unsupported HAVE objective resource '{resource}' for scoring.")
        return False

    def _evalOwnObjective(self, reqs, PlayerTrying : Player.Player) -> bool:
        resource = reqs.get('Resource')
        quantity = reqs.get('Quantity', 0)
        conditions = reqs.get('Conditions', []) or []

        if resource == 'technologies':
            if 'in each of 2 colors' in ' '.join(conditions).lower():
                color_counts = self._count_player_technology_colors(PlayerTrying)
                if sum(1 for value in color_counts.values() if value >= quantity) >= 2:
                    return self.AwardScore(PlayerTrying)
                return False

            if 'unit technologies' in ' '.join(conditions).lower():
                if len(PlayerTrying.UnitTechnologies) >= quantity:
                    return self.AwardScore(PlayerTrying)
                return False

            if self._count_player_technologies(PlayerTrying) >= quantity:
                return self.AwardScore(PlayerTrying)
            return False

        print(f"Unsupported OWN objective resource '{resource}' for scoring.")
        return False

    def _evalSpendObjective(self, reqs, PlayerTrying : Player.Player) -> bool:
        if (reqs.get('Resources', 0) <= PlayerTrying.AvailableResources and 
            reqs.get('Influence', 0) <= PlayerTrying.AvailableInfluence and 
            reqs.get('TradeGoods', 0) <= PlayerTrying.TradeGoods and 
            reqs.get('Tokens', 0) <= PlayerTrying.GetScoringTokens()):

            PlayerTrying.AvailableResources -= reqs.get('Resources', 0)
            PlayerTrying.AvailableInfluence -= reqs.get('Influence', 0)
            PlayerTrying.TradeGoods         -= reqs.get('TradeGoods', 0)
            return self.AwardScore(PlayerTrying)

        return False

    def AttemptToScore(self, PlayerTrying : Player.Player, GameMap : Map.System) -> bool:
        if PlayerTrying.PlayerID in self.ScoredBy:
            return False

        if self.ObjectiveReqs is None:
            return False

        objective_type = self.ObjectiveReqs.get('type')
        match objective_type:
            case 'Have':
                return self._evalHaveObjective(self.ObjectiveReqs, PlayerTrying, GameMap)
            case 'Control':
                return self.__evalControlObjective(self.ObjectiveReqs.get('Filters', {}), PlayerTrying, GameMap)
            case 'Own':
                return self._evalOwnObjective(self.ObjectiveReqs, PlayerTrying)
            case 'Spend':
                return self._evalSpendObjective(self.ObjectiveReqs, PlayerTrying)
            case _:
                print(f"Unsupported objective type '{objective_type}'")
                return False

    def __evalControlObjective(self, filters, PlayerTrying, GameMap):
        # Count planets that match the filters
        planet_count = 0
        if filters.get('PlanetTrait') in ('Any', 'Same'):
            trait_counts = {'Red': 0, 'Green': 0, 'Blue': 0}
            for tile in GameMap.tiles:
                for planet in tile.Planets:
                    if planet.OwnedBy != PlayerTrying.PlayerID:
                        continue
                    if not self.__matchesFilters(planet, filters):
                        continue
                    if isinstance(planet.PlanetTrait, str) and planet.PlanetTrait in trait_counts:
                        trait_counts[planet.PlanetTrait] += 1
            print(f"Trait counts for player {PlayerTrying.PlayerID}: {trait_counts}")
            if any(count >= self.ObjectiveReqs.get('Planets', 0) for count in trait_counts.values()):
                return self.AwardScore(PlayerTrying)
            return False

        for tile in GameMap.tiles:
            for planet in tile.Planets:
                if planet.OwnedBy == PlayerTrying.PlayerID and self.__matchesFilters(planet, filters):
                    planet_count += 1

        if planet_count >= self.ObjectiveReqs.get('Planets', 0):
            return self.AwardScore(PlayerTrying)
        return False

    def __matchesFilters(self, planet, filters):
        for key, value in filters.items():
            if key == 'PlanetTrait':

                if value in ('Any', 'Same'):
                    continue
                if not hasattr(planet, 'PlanetTrait') or planet.PlanetType != value:
                    return False
            elif key == 'HasAttachment':
                if not hasattr(planet, 'HasAttachment') or planet.HasAttachment != value:
                    return False
            elif key == 'IsNonHome':
                if not hasattr(planet, 'IsNonHome') or planet.IsNonHome != value:
                    return False
            elif key == 'HasStructure':
                if not hasattr(planet, 'HasStructure') or planet.HasStructure != value:
                    return False
            elif key == 'HasTechSpecialty':
                if not hasattr(planet, 'HasTechSpecialty') or planet.HasTechSpecialty != value:
                    return False
        return True
    
    def __repr__(self):
        return self.ObjectiveName