from dataclasses import dataclass, field
from typing import Dict, Tuple, Optional
import json
from Game_Enums import UnitType
from ImageCache import ImageCache
from functools import lru_cache

@dataclass
class UnitStats:
    """Standardized unit statistics container"""
    name: str
    cost: int
    combat_value: list[list[int]] = field(default_factory=lambda: [[], []])  # list of [space combat], [ground combat] -> each roll is represented by a value
    movement: Optional[int] = None
    capacity: Optional[int] = None
    RequiresCarry: bool = False
    hits: int = 1  # Hit points/health
    production: Optional[int] = None  # For space docks
    planetary_shield: bool = False  # For PDS
    bombardment: Optional[int] = None
    anti_fighter_barrage: Optional[Tuple[int, int]] = None  # (dice, hit_value)
    sustain_damage: bool = False

    image_path: Optional[str] = None  # Path to unit image
    _image_cache: Optional[ImageCache] = None  # Cached image object
    
    def __post_init__(self):
        """Validate unit stats after initialization"""
        if self.combat_value is not None:
            if isinstance(self.combat_value, int):
                if not (1 <= self.combat_value <= 10):
                    raise ValueError(f"Combat value must be between 1-10, got {self.combat_value}")
            elif isinstance(self.combat_value, (list, tuple)):
                for CombatType in self.combat_value:
                    if CombatType is None:
                        continue

                    for val in CombatType:
                        if val is not None and not (1 <= val <= 10):
                            raise ValueError(f"Combat values must be between 1-10, got {val}")


    def get_image(self, Colours : tuple[int, int, int], size: int = 5) -> ImageCache:
        """Get cached image for this unit"""
        if self._image_cache is None:
            self._image_cache = ImageCache(self.image_path, size)
        
        return self._image_cache.get_colored_scaled_tile(size, Colours)
    
    def has_image(self) -> bool:
        """Check if the unit has a valid image"""
        try:
            import os
            return os.path.exists(self.image_path) if self.image_path else False
        except:
            return False

class UnitManager:
    """Centralized unit information management"""
    
    def __init__(self):
        self._base_units = self._initialize_base_units()
        self._custom_units = {}  # For race-specific unit modifications
        
    def _initialize_base_units(self) -> Dict[UnitType, UnitStats]:
        """Initialize base game unit statistics"""
        return {
            UnitType.FIGHTER: UnitStats(
                name="Fighter",
                cost=0.5,
                combat_value=[[], [9]],
                RequiresCarry=True,
                hits=1,
                image_path=f"Assets\\Units\\Fighter.png"
            ),
            UnitType.DESTROYER: UnitStats(
                name="Destroyer",
                cost=1,
                combat_value=[[], [9]],
                movement=2,
                hits=1,
                anti_fighter_barrage=(2, 9),
                image_path=f"Assets\\Units\\Destroyer.png"
            ),
            UnitType.CRUISER: UnitStats(
                name="Cruiser",
                cost=2,
                combat_value=[[], [7]],
                movement=2,
                hits=1,
                capacity=1,
                image_path=f"Assets\\Units\\Cruiser.png"
            ),
            UnitType.CARRIER: UnitStats(
                name="Carrier",
                cost=3,
                combat_value=[[], [9]],
                movement=1,
                hits=1,
                capacity=4,
                image_path=f"Assets\\Units\\Carrier.png"
            ),
            UnitType.DREADNOUGHT: UnitStats(
                name="Dreadnought",
                cost=4,
                combat_value=[[], [5]],
                movement=1,
                hits=1,
                bombardment=5,
                sustain_damage=True,
                capacity=1,
                image_path="Assets\\Units\\Dreadnought.png"
            ),
            UnitType.FLAGSHIP: UnitStats(
                name="Flagship",
                cost=8,
                combat_value=[[], []],
                movement=1,
                hits=1,
                sustain_damage=True,
                capacity=3,
                image_path="Assets\\Units\\Flagship.png"
            ),
            UnitType.WAR_SUN: UnitStats(
                name="WarSun",
                cost=12,
                combat_value=[[], [3, 3, 3]],
                movement=2,
                hits=1,
                bombardment=3,
                sustain_damage=True,
                capacity=6,
                image_path="Assets\\Units\\WarSun.png"
            ),
            UnitType.INFANTRY: UnitStats(
                name="Infantry",
                cost=0.5,
                combat_value=[[8], []],
                RequiresCarry=True,
                hits=1,
                image_path="Assets\\Units\\Infantry.png"
            ),
            UnitType.MECH: UnitStats(
                name="Mech",
                cost=2,
                combat_value=[[6], []],
                RequiresCarry=True,
                sustain_damage=True,
                hits=1,
                image_path="Assets\\Units\\Mech.png"
            ),
            UnitType.SPACE_DOCK: UnitStats(
                name="SpaceDock",
                cost=4,
                hits=1,
                production=2,
                image_path="Assets\\Units\\SpaceDock.png"
            ),
            UnitType.PDS: UnitStats(
                name="PDS",
                cost=2,
                hits=1,
                planetary_shield=True,
                image_path="Assets\\Units\\PDS.png"
            )
        }
    
    def get_unit_stats(self, unit_type: UnitType, player_id: Optional[int] = None, 
                      race_name: Optional[str] = None) -> UnitStats:
        """
        Get unit statistics, considering race modifications
        
        Args:
            unit_type: The type of unit
            player_id: Player ID for player-specific modifications
            race_name: Race name for race-specific modifications
        
        Returns:
            UnitStats object with current unit statistics
        """
        # Start with base unit stats
        base_stats = self._base_units.get(unit_type)
        if not base_stats:
            raise ValueError(f"Unknown unit type: {unit_type}")
        
        # Create a copy to avoid modifying the original
        stats = UnitStats(
            name=base_stats.name,
            cost=base_stats.cost,
            combat_value=base_stats.combat_value.copy() if base_stats.combat_value else None,
            movement=base_stats.movement,
            RequiresCarry=base_stats.RequiresCarry,
            capacity=base_stats.capacity,
            hits=base_stats.hits,
            production=base_stats.production,
            planetary_shield=base_stats.planetary_shield,
            bombardment=base_stats.bombardment,
            anti_fighter_barrage=base_stats.anti_fighter_barrage,
            sustain_damage=base_stats.sustain_damage,
            image_path=base_stats.image_path
        )
        
        # Apply race-specific modifications
        if race_name:
            race_key = f"{race_name}_{unit_type.value}"
            if race_key in self._custom_units:
                custom_stats = self._custom_units[race_key]
                # Apply custom modifications
                for attr, value in custom_stats.items():
                    if hasattr(stats, attr):
                        setattr(stats, attr, value)
        
        # Apply player-specific modifications (for upgrades, etc.)
        if player_id:
            player_key = f"player_{player_id}_{unit_type.value}"
            if player_key in self._custom_units:
                custom_stats = self._custom_units[player_key]
                for attr, value in custom_stats.items():
                    if hasattr(stats, attr):
                        setattr(stats, attr, value)
        
        return stats
    
    def register_custom_unit(self, key: str, unit_type: UnitType, 
                           modifications: Dict[str, any]):
        """
        Register custom unit modifications for races or players
        
        Args:
            key: Unique identifier (e.g., "Arborec_Infantry", "player_1_Dreadnought")
            unit_type: Base unit type
            modifications: Dictionary of attribute modifications
        """
        self._custom_units[key] = modifications
    
    def register_race_units(self, race_name: str, race_modifications: Dict[UnitType, Dict[str, any]]):
        """
        Register multiple race-specific unit modifications
        
        Args:
            race_name: Name of the race
            race_modifications: Dictionary mapping unit types to their modifications
        """
        for unit_type, modifications in race_modifications.items():
            key = f"{race_name}_{unit_type.value}"
            self._custom_units[key] = modifications
    
    def get_all_unit_types(self) -> list[UnitType]:
        """Get list of all available unit types"""
        return list(self._base_units.keys())
    
    def get_unit_cost(self, unit_type: UnitType, player_id: Optional[int] = None, 
                     race_name: Optional[str] = None) -> int:
        """Get the cost of a specific unit"""
        return self.get_unit_stats(unit_type, player_id, race_name).cost
    
    def get_combat_value(self, unit_type: UnitType, is_space_combat: bool = True,
                        player_id: Optional[int] = None, race_name: Optional[str] = None) -> Optional[list]:
        """Get combat value for a unit in space or ground combat"""
        stats = self.get_unit_stats(unit_type, player_id, race_name)
        if stats.combat_value is None:
            return None
        
        # Return space combat (index 0) or ground combat (index 1)
        combat_index = 0 if is_space_combat else 1
        if len(stats.combat_value) > combat_index:
            return stats.combat_value[combat_index]
        return []
    
    def can_move(self, unit_type: UnitType, player_id: Optional[int] = None, 
                race_name: Optional[str] = None) -> bool:
        """Check if a unit can move"""
        stats = self.get_unit_stats(unit_type, player_id, race_name)
        return stats.movement is not None and stats.movement > 0
    
    def has_capacity(self, unit_type: UnitType, player_id: Optional[int] = None, 
                    race_name: Optional[str] = None) -> bool:
        """Check if a unit has carrying capacity"""
        stats = self.get_unit_stats(unit_type, player_id, race_name)
        return stats.capacity is not None and stats.capacity > 0
    
    def export_unit_data(self, filepath: str):
        """Export unit data to JSON file"""
        export_data = {
            "base_units": {},
            "custom_units": self._custom_units
        }
        
        for unit_type, stats in self._base_units.items():
            export_data["base_units"][unit_type.value] = {
                "name": stats.name,
                "cost": stats.cost,
                "combat_value": stats.combat_value,
                "movement": stats.movement,
                "capacity": stats.capacity,
                "hits": stats.hits,
                "production": stats.production,
                "planetary_shield": stats.planetary_shield,
                "bombardment": stats.bombardment,
                "anti_fighter_barrage": stats.anti_fighter_barrage,
                "sustain_damage": stats.sustain_damage
            }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
    
    def import_unit_data(self, filepath: str):
        """Import unit data from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        if "custom_units" in data:
            self._custom_units.update(data["custom_units"])

    @lru_cache(maxsize=32)
    def get_unit_image(self, unit_type: UnitType, Colour : tuple[int, int, int], size: int = 5) -> Optional[ImageCache]:
        """Get the image for a specific unit"""
        stats = self.get_unit_stats(unit_type)
        return stats.get_image(Colour, size)