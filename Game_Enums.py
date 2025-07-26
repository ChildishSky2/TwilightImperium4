from enum import Enum

class Phases(Enum):
    Strategy : 1
    Action : 2
    Status : 3
    Agenda : 4

class ActionPhase(Enum):
    Activate_Action_Card : 0
    Activate_Strategy_Card : 1
    Activate_System : 2
    Move_Ships : 3
    Offense_Space_Cannon : 4
    Space_Combat : 5
    Commit_GF : 6
    Defensive_Space_Cannon : 7
    Ground_Combat : 8
    Production : 9

class PlanetTypes(Enum):
    NoType  = 0
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