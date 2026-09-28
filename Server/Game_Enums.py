from enum import Enum

class Phases(Enum):
    Strategy = "Strategy"
    Action = "Action"
    Status = "Status"
    Agenda  = "Agenda"

class ActionType(Enum):
    Component = "Component"
    Strategic = "Strategic"
    Tactical = "Tactical"

class ActionPhase(Enum):
    Start_Turn = 0
    Activate_System = 1
    Movement = 2
    Space_Combat = 3
    Invasion = 4
    Production = 5

class MovementPhases(Enum):
    MoveShips = 0
    SpaceCannonOffense = 1

class SpaceCombatPhases(Enum):
    Anti_fighter = 0
    Announce_retreat = 1
    CombatRolls = 2
    AssignHits = 3
    Retreat = 4

class InvasionPhases(Enum):
    Bombardment = 0
    CommitGroundForces = 1
    SpaceCannonDefence = 2
    GroundCombat = 3
    EstablishControl = 4


class PlanetTypes(Enum):
    NoType = 0
    Hazardous = 1
    Cultural = 2
    Industrial = 3
    All = 4

class Anomalies(Enum):
    NoAnomaly = 0
    Nebulae = 1
    AsteroidField = 2
    GravityRift = 3
    Supernova = 4

class UnitType(Enum):
    FIGHTER = "Fighter"
    DESTROYER = "Destroyer"
    CRUISER = "Cruiser"
    CARRIER = "Carrier"
    DREADNOUGHT = "Dreadnought"
    FLAGSHIP = "Flagship"
    WAR_SUN = "WarSun"
    INFANTRY = "Infantry"
    SPACE_DOCK = "SpaceDock"
    PDS = "PDS"
    MECH = "Mech"

class Race(Enum):
    Arborec = 1
    BaronyOfLetnev = 2
    ClanOfSaar = 3
    Creuss = 4
    EmiratesOfHacan = 5
    JolNar = 6
    Lizix = 7
    Mentak = 8
    Muatt = 9
    Naalu = 10
    NekroVirus = 11
    SardockNorr = 12
    Sol = 13
    Winnu = 14
    Yin = 15
    Yssaril = 16

class TechnologyTypes(Enum):
    Propulsion = "B"
    Cybernetic = "Y"
    Biological = "G"
    Warfare = "R"
    Unit = "I"