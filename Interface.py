import pygame
pygame.init()
pygame.display.set_mode((1, 1), pygame.HIDDEN)

import math

import Game
from ImageCache import ImageCache
from Map import Tile
from Game_Enums import UnitType
#view

class UserInterface():
    def _calculate_hex_grid_positions(self, rings):
        """Generate hexagonal grid positions in TI4 format."""
        center_x = self.width//2.1
        center_y = self.height//2.25
        
        positions = []
    
        # Constants for hexagon geometry
        sqrt_3 = math.sqrt(3)
        offset_factor = 0.8660254037844386  # Precise √3/2 value

        positions.append((center_x, center_y))
        # Generate positions for each ring
        for ring in range(1, rings + 1):
            # Directly above
            x_value = center_x
            y_value = center_y - self.radius * sqrt_3 * ring

            positions.append((x_value, y_value))

            #move down + right
            for _ in range(1, ring + 1):
                x_value += (self.radius * sqrt_3) * offset_factor
                y_value += (self.radius * sqrt_3) * 0.5
                positions.append((x_value, y_value))
            
            #down on the right
            for _ in range(1, ring + 1):
                y_value += (self.radius * sqrt_3)
                positions.append((x_value, y_value))

            #down moving left
            for _ in range(1, ring+1):
                x_value -= (self.radius * sqrt_3) * offset_factor
                y_value += (self.radius * sqrt_3) * 0.5
                positions.append((x_value, y_value))

            #move up + left
            for _ in range(1, ring + 1):
                x_value -= (self.radius * sqrt_3) * offset_factor
                y_value -= (self.radius * sqrt_3) * 0.5
                positions.append((x_value, y_value))
            
            #up on the left
            for _ in range(1, ring + 1):
                y_value -= (self.radius * sqrt_3)
                positions.append((x_value, y_value))

            #up and right
            for _ in range(1, ring):
                x_value += (self.radius * sqrt_3) * offset_factor
                y_value -= (self.radius * sqrt_3) * 0.5
                positions.append((x_value, y_value))

        return positions

    def _calculate_player_areas(self, NumberofPlayers):
    
        # Calculate available space for boxes
        start_x = int(self.width * 0.775)
        start_y = int(self.height * 0.1)
        available_height = self.height - (start_y * 2)  # Leave 10% at top and bottom
    
        # Calculate box size and spacing
        box_height = int(available_height / (NumberofPlayers * 1.2))  # 1.2 = box + spacing
        box_width = self.width - (start_x * 1.005)  # Fill to right edge
        spacing = int(box_height * 0.2)  # 20% of box height
    
        # Calculate starting position
        total_height = (box_height + spacing) * NumberofPlayers - spacing
        start_y = (self.height - total_height) // 2  # Center vertically
    
        positions = []
        for i in range(NumberofPlayers):
            y_position = start_y + (i * (box_height + spacing))
            positions.append((start_x, y_position, box_width, box_height))
    
        return positions

    def _calculate_active_system(self):
        self.PassTurnButton = pygame.Rect(self.width * 0.045, self.height * 0.8, 110, 30)
        self.ActivateSystemButton = pygame.Rect(self.width * 0.045, self.height * 0.6, 210, 30)
        self.EndTurnButton = pygame.Rect(self.width * 0.045, self.height * 0.8, 110, 30)

    def _calc_resize(self):
        self.width = self.Screen.get_width()
        self.height = self.Screen.get_height()
        self.radius = int(0.06 * min(self.width, self.height))

        self.MapHexPositions = self._calculate_hex_grid_positions(self.Game.Map.max_rings)
        self.PlayerAreaPositions = self._calculate_player_areas(len(self.Game.Players))
        self._calculate_active_system()

    def _draw_Map(self):
        """Draw a circular grid of hexagons using cached tiles."""
        circle_radius = self.radius / 1.75
        token_size = int(self.radius / 4)
        ship_circle_radius = circle_radius * 0.75

        def GetTokenPos(blits : list, tile, center_x, center_y):
            activated_players = tile.GetPlayersWhoActivatedSystem()
            if len(activated_players) == 0:
                return

            num_planets = len(tile.Planets)
            num_tokens = len(activated_players)

            match num_planets:
                case 1:
                    angle_step = math.pi / (num_tokens-1) if num_tokens > 1 else 0
                    angle_adjustment = 60 if int(tile.GetTileNumber()) in [25, 26, 64, 67, 68] else 0
                    for i, player_idx in enumerate(activated_players):
                        angle = math.pi - angle_adjustment + i * angle_step

                        token_x = center_x + circle_radius * math.cos(angle) - token_size / 2
                        token_y = center_y + circle_radius * math.sin(angle) - token_size / 2
                        token_img = self.Game.Players[player_idx].GetTokenImg(token_size)
                        blits.append((token_img, (token_x, token_y)))

                case 2:
                    angle_step = math.pi / (num_tokens - 1) if num_tokens > 1 else 0
                    for i, player_idx in enumerate(activated_players):
                        if i >= 3:
                            angle = math.pi + 22.5 + i * angle_step
                        else:
                            angle = math.pi + 46 + i * angle_step

                        token_x = center_x + circle_radius * math.cos(angle) - token_size / 2
                        token_y = center_y + circle_radius * math.sin(angle) - token_size / 2

                        token_img = self.Game.Players[player_idx].GetTokenImg(token_size)
                        blits.append((token_img, (token_x, token_y)))
                
                case 3:
                    positions = [
                        (center_x - circle_radius * 0.4 - token_size / 2, center_y + circle_radius * 0.8 - token_size / 2),  # Bottom left
                        (center_x - circle_radius * 0.1 - token_size / 2, center_y + circle_radius * 0.85 - token_size / 2),
                        (center_x + circle_radius * 1.3 - token_size / 2, center_y - circle_radius * 0.3 - token_size / 2),
                        (center_x + circle_radius * 0.9 - token_size / 2, center_y - token_size / 2), 
                        (center_x - circle_radius * 0.9 - token_size / 2, center_y - circle_radius - token_size / 2),
                        (center_x - circle_radius * 0.5 - token_size / 2, center_y - circle_radius * 1.1 - token_size / 2)
                    ]
                    for i, player_idx in enumerate(activated_players):
                        token_img = self.Game.Players[player_idx].GetTokenImg(token_size)
                        blits.append((token_img, positions[i]))

                case _:
                    for i, player_idx in enumerate(activated_players):
                        # Calculate angle for each token (360 degrees / number of tokens)
                        angle = (i * 360) / len(activated_players)
                        angle_rad = math.radians(angle)
                        token_x = center_x + circle_radius * math.cos(angle_rad) - token_size / 2
                        token_y = center_y + circle_radius * math.sin(angle_rad) - token_size / 2
                    
                        # Draw the token
                        token_img = self.Game.Players[player_idx].GetTokenImg(token_size)
                        blits.append((token_img, (token_x, token_y)))

        def GetShipBlits(blits : list, tile, center_x, center_y):
            ships = tile.GetShipsInSystem()
            num_ships = len(ships)

            if num_ships == 0:
                return
            
            player_color = self.Game.Players[tile.ShipOwner].Colour
    
    
            if num_ships == 1:
                # Single ship goes in the center
                ship_image = self.Game.UnitManager.get_unit_image(ships[0], player_color, 15)
                blits.append((ship_image, (center_x - 5, center_y - 5)))
            else:
                # Multiple ships arranged in a circle
                for ship_idx, ship in enumerate(ships):
                    # Calculate angle for each ship (evenly distributed around the circle)
                    angle = (ship_idx * 2 * math.pi) / num_ships
            
                    # Calculate position on the circle
                    ship_x = center_x + ship_circle_radius * math.cos(angle) - 5
                    ship_y = center_y + ship_circle_radius * math.sin(angle) - 5
            
                    ship_image = self.Game.UnitManager.get_unit_image(ship, player_color, 15)
                    blits.append((ship_image, (ship_x, ship_y)))

        def GetGFBlits(blits : list, tile : Tile, center_x, center_y): 
            #no planets in system
            if len(tile.Planets) == 0:
                if tile.InfantryInSpace == 0:
                    Inf_image = self.Game.UnitManager.get_unit_image(UnitType.INFANTRY, self.Game.Players[tile.ShipOwner].Colour, 15)
                    blits.append((Inf_image, (center_x, center_y)))

                if tile.MechsInSpace == 0:
                    Mech_image = self.Game.UnitManager.get_unit_image(UnitType.MECH, self.Game.Players[tile.ShipOwner].Colour, 15)
                    blits.append((Mech_image, (center_x, center_y)))
                    pass


            match len(tile.Planets):
                case 0:
                    pass
                case _:
                    pass
            pass

        # Batch collect all blits
        blits = []

        x_adjust = 0.85 * self.radius
        y_adjust = 0.9 * self.radius

        for index, tile in enumerate(self.Game.Map.Map):
            x, y = self.MapHexPositions[index]

            blits.append((tile.TileImage.get_scaled_tile(self.radius), self.MapHexPositions[index]))
            GetTokenPos(blits, tile, x + x_adjust, y + y_adjust)
            GetGFBlits(blits, tile, x + x_adjust, y + y_adjust)
            GetShipBlits(blits, tile, x + x_adjust, y + y_adjust)

        if blits:
            self.Screen.blits(blits)

        return

    def _draw_player_areas(self, Technology_symbols : list):
        # Define minimum dimensions and font sizes
        MIN_FONT_SIZE = 24
        MAX_FONT_SIZE = 72
    
        for i, player in zip(self.PlayerAreaPositions, self.Game.Players):
            # Get the rectangle
            rect = pygame.Rect(*i)
        
            # Calculate dynamic padding (5% of smallest dimension)
            min_window_dim = min(rect.width, rect.height)
            padding = max(2, int(min_window_dim * 0.05))
            colour = player.Colour if player.Colour is not None else (0, 0, 0)

            # Draw the rectangle outline
            pygame.draw.rect(
                self.Screen,
                colour,
                rect,
                width=2,
                border_radius=10
            )

            if self.Game.Players[self.Game.Turn] == player:
                inner_rect = rect.inflate(8, 8)  # Creates a gap of 4 pixels on each side
                pygame.draw.rect(
                    self.Screen,
                    colour,
                    inner_rect,
                    width=2,
                    border_radius=15
                )

            scale_factor = min(min_window_dim / 600, 1.0)
        
            # Calculate font size for player name
            font_size = int(MAX_FONT_SIZE * scale_factor)
            font_size = max(MIN_FONT_SIZE, font_size)
        
            # Create dynamic font object for player name
            font = pygame.font.SysFont(None, font_size)

            VP_surface = font.render(str(player.VP) + "VP", True, colour)
            VP_rect = VP_surface.get_rect(
                topright = (
                    rect.right - padding,
                    rect.top + padding
                )
            )
            self.Screen.blit(VP_surface, VP_rect)

            box_padding = max(3, int(font_size * 0.1))  # Scale padding with font size
            VP_box = VP_rect.inflate(box_padding * 2, box_padding * 2)
            pygame.draw.rect(self.Screen, (255, 0, 0), VP_box, width=3, border_radius=5)  # Orange border
        
            self.Screen.blit(VP_surface, VP_rect)
        
            # Render the player text
            text_surface = font.render(player.PlayerName, True, colour)
            text_rect = text_surface.get_rect(
                topleft=(
                    rect.left + padding,
                    rect.top + padding
                )
            )
            self.Screen.blit(text_surface, text_rect)

            font = pygame.font.SysFont(None, int(font_size * 0.8))

            # Render the Player Race under the Name
            RaceText_surface = font.render(str(player.Race), True, colour)
            RaceText_rect = RaceText_surface.get_rect(
                topleft=(
                    rect.left + padding,
                    rect.top + 3 * padding
                )
            )
            self.Screen.blit(RaceText_surface, RaceText_rect)

            #Marking if player is passed
            if player.Passed:
                Passed_Text = font.render("Passed", True, (255, 0, 0))
                Passed_Rect = Passed_Text.get_rect(
                    bottomleft = (
                        rect.left + padding,
                        rect.bottom - 2*padding
                    )
                )
                self.Screen.blit(Passed_Text, Passed_Rect)

            # Calculate technology font size - make it smaller than player name but still scaled
            tech_font_size = max(12, font_size)  # Minimum tech font size
            tech_font = pygame.font.SysFont(None, tech_font_size)

            # Calculate technology symbol size based on rect size
            tech_symbol_size = int(min_window_dim * 0.08)

            #Green techs - top left
            self.Screen.blit(Technology_symbols[0].get_scaled_tile(tech_symbol_size), (rect.left + rect.width * 0.075, rect.top + rect.height * 0.3))#image
            Green_tech = tech_font.render(str(len(player.PropulsionTechs)), True, colour)
            self.Screen.blit(Green_tech, Green_tech.get_rect(topright = (rect.left + rect.width * 0.06, rect.top + rect.height * 0.3)))#text

            #Yellow techs - top right
            self.Screen.blit(Technology_symbols[1].get_scaled_tile(tech_symbol_size), (rect.left + rect.width * 0.175, rect.top + rect.height * 0.3))
            Yellow_tech = tech_font.render(str(len(player.PropulsionTechs)), True, colour)
            self.Screen.blit(Yellow_tech, Yellow_tech.get_rect(topright = (rect.left + rect.width * 0.3, rect.top + rect.height * 0.3)))

            #Blue Techs - bottom left
            self.Screen.blit(Technology_symbols[2].get_scaled_tile(tech_symbol_size), (rect.left + rect.width * 0.075, rect.top + rect.height * 0.45))
            Blue_tech = tech_font.render(str(len(player.PropulsionTechs)), True, colour)
            self.Screen.blit(Blue_tech, Blue_tech.get_rect(topright = (rect.left + rect.width * 0.06, rect.top + rect.height * 0.45)))

            #Red Techs - bottom right
            self.Screen.blit(Technology_symbols[3].get_scaled_tile(tech_symbol_size), (rect.left + rect.width * 0.175, rect.top + rect.height * 0.45))
            Red_tech = tech_font.render(str(len(player.PropulsionTechs)), True, colour)
            self.Screen.blit(Red_tech, Red_tech.get_rect(topright = (rect.left + rect.width * 0.3, rect.top + rect.height * 0.45)))


            #Resources and Influence
            Resources_text = tech_font.render(str(player.Resources) + "R", True, colour)
            self.Screen.blit(Resources_text, Resources_text.get_rect(topright = (rect.left + rect.width * 0.5, rect.top + rect.height * 0.3)))

            Influences_text = tech_font.render(str(player.Influence) + "I", True, colour)
            self.Screen.blit(Influences_text, Resources_text.get_rect(topright = (rect.left + rect.width * 0.5, rect.top + rect.height * 0.45)))

            #Tokens in each pool
            Tokens = tech_font.render("Tokens", True, colour)
            self.Screen.blit(Tokens, Resources_text.get_rect(topright = (rect.left + rect.width * 0.8, rect.top + rect.height * 0.26)))

            if player.TacticsTokens > 9:
                adjust = 0.04
            else:
                adjust = 0

            Tactic = tech_font.render("Tactic:" + str(player.TacticsTokens), True, colour)
            self.Screen.blit(Tactic, Resources_text.get_rect(topright = (rect.left + rect.width * (0.8 - adjust), rect.top + rect.height * 0.4)))

            #Fleet Tokens
            if player.FleetTokens > 9:
                adjust = 0.02
            else:
                adjust = 0
            Fleet = tech_font.render("Fleet: " + str(player.FleetTokens), True, colour)
            self.Screen.blit(Fleet, Resources_text.get_rect(topright = (rect.left + rect.width * (0.8 - adjust), rect.top + rect.height * 0.54)))

            #Strategy Tokens
            if player.StrategyTokens > 9:
                adjust = 0.02
            else:
                adjust = 0
            Strat = tech_font.render("Strat: " + str(player.StrategyTokens), True, colour)
            self.Screen.blit(Strat, Resources_text.get_rect(topright = (rect.left + rect.width * (0.8 - adjust), rect.top + rect.height * 0.68)))

        pass

    def _handle_click(self, mouse_pos):
        """Detect which hexagon was clicked."""

        if self.selectedTile == None and self.Game.ActiveSystem == None:
            if (self.PassTurnButton.left <= mouse_pos[0] <= self.PassTurnButton.right and
                self.PassTurnButton.top <= mouse_pos[1] <= self.PassTurnButton.bottom):
                self.Game.Pass()
                self.selectedTile = None
                return
            
        if self.selectedTile != None and self.Game.ActiveSystem == None:
            if (self.ActivateSystemButton.left <= mouse_pos[0] <= self.ActivateSystemButton.right and
                self.ActivateSystemButton.top <= mouse_pos[1] <= self.ActivateSystemButton.bottom):

                #player has no tactics tokens left
                if self.Game.Players[self.Game.Turn].TacticsTokens <= 0:
                    return
                
                #Player has previously activated the system
                if self.Game.Map.Map[self.selectedTile].CheckPlayerHasActivatedSystem(self.Game.Players[self.Game.Turn].PlayerID):
                    return
                
                self.Game.ActivateSystem(self.selectedTile)
                return
            pass
        
        if self.Game.ActiveSystem != None:
            if (self.EndTurnButton.left <= mouse_pos[0] <= self.EndTurnButton.right and
                self.EndTurnButton.top <= mouse_pos[1] <= self.EndTurnButton.bottom):

                self.Game.EndTurn()
                self.selectedTile = None
            return

        #calculating from top left of hexagon
        mouse_pos_x, mouse_pos_y = mouse_pos[0] - self.radius, mouse_pos[1] - self.radius
        r2 = self.radius ** 2
        for idx, pos in enumerate(self.MapHexPositions):
            dx = mouse_pos_x - pos[0]
            dy = mouse_pos_y - pos[1]
            distance = dx**2 + dy**2

            # Check if click is within hexagon
            if distance < r2:
                if self.Game.ActiveSystem:
                    print(self.Game.Map.get_tile_distance(self.Game.ActiveSystem, idx))
                else:
                    #selecting a system
                    self.selectedTile = idx
                return
        self.selectedTile = None
        return

    def _draw_Active_System(self):
        #pass, end turn, undo buttons
        font = pygame.font.SysFont(None, 30)
        min_window_dim = min(self.ActivateSystemButton.width, self.ActivateSystemButton.height)
        padding = max(2, int(min_window_dim * 0.2))

        def ActivateSystemButtom(colours : tuple[int, int, int]):
            pygame.draw.rect(self.Screen, colours, self.ActivateSystemButton)
            pygame.draw.rect(self.Screen, (0, 0, 0), self.ActivateSystemButton, 2)
            text_surface = font.render("Activate System", True, (0, 0, 0))
            text_rect = text_surface.get_rect(
                topleft=(
                    self.ActivateSystemButton.left + padding * 3,
                    self.ActivateSystemButton.top + padding
                )
            )
            self.Screen.blit(text_surface, text_rect)

        def EndTurnButton():
            pygame.draw.rect(self.Screen, (255, 255, 255), self.EndTurnButton)
            pygame.draw.rect(self.Screen, (0, 0, 0), self.EndTurnButton, 2)
            EndTurn_surface = font.render("End Turn", True, (0, 0, 0))
            EndTurn_rect = EndTurn_surface.get_rect(
                topleft=(
                    self.EndTurnButton.left + padding * 3,
                    self.EndTurnButton.top + padding
                )
            )
            self.Screen.blit(EndTurn_surface, EndTurn_rect)
        
        def PassTurnButton():
            pygame.draw.rect(self.Screen, (0, 0, 0), self.PassTurnButton, 2)
            text_surface = font.render("Pass Turn", True, (0, 0, 0))
            text_rect = text_surface.get_rect(
            topleft=(
                self.PassTurnButton.left + padding,
                self.PassTurnButton.top + padding
                )
            )
            self.Screen.blit(text_surface, text_rect)
        
        if self.selectedTile == None and self.Game.ActiveSystem == None:
            PassTurnButton()
            return

        img_source = self.Game.Map.Map[self.Game.ActiveSystem].TileImage if self.Game.ActiveSystem != None else self.Game.Map.Map[self.selectedTile].TileImage
        img = img_source.get_scaled_tile(self.radius * 3)
        self.Screen.blit(img, (self.width * 0.02, self.height * 0.2))

        if self.selectedTile != None and self.Game.Map.Map[self.selectedTile].CheckPlayerHasActivatedSystem(self.Game.Players[self.Game.Turn].PlayerID):
            ActivateSystemButtom((100, 100, 100))
        else:
            ActivateSystemButtom((255, 255, 255))

        if self.Game.ActiveSystem != None:
            EndTurnButton()

        pass

    def __init__(self, Game : Game.Game):
        self.Screen = pygame.display.set_mode(
            (1000, 720),
            pygame.RESIZABLE | pygame.SRCALPHA
        )
        pygame.display.set_caption('Twilight Imperium 4th edition')

        self.selectedTile = None
        self.Game = Game

        self._calc_resize()

        assert len(self.Game.Map.Map) == len(self.MapHexPositions), "Faiiled to intialise"

    def Main(self):
        Running = True
        Technology_symbols = [ImageCache("Assets\\Images\\biotic_symbol.png", self.radius), 
                              ImageCache("Assets\\Images\\cybernetic_symbol.png", self.radius), 
                              ImageCache("Assets\\Images\\propulsion_symbol.png", self.radius), 
                              ImageCache("Assets\\Images\\warfare_symbol.png", self.radius)]

        while Running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.Screen = pygame.display.set_mode(
                        (event.w, event.h),
                        pygame.RESIZABLE | pygame.SRCALPHA
                    )
                    self._calc_resize()
                elif event.type == pygame.MOUSEBUTTONDOWN:

                    self._handle_click(event.pos)

            self.Screen.fill((200, 200, 200))

            self._draw_Map()
            self._draw_player_areas(Technology_symbols)
            self._draw_Active_System()
            pygame.display.flip()

        pygame.quit()


G = Game.Game(10)
G.SetPlayerNumbers(4)
G.GenerateMap()


u = UserInterface(G)
u.Main()

