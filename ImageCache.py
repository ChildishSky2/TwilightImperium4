import pygame


class ImageCache:
    """Base class for caching scaled images with color variations"""
   
    def __init__(self, path: str, base_size: int, alpha: int = 255):
        self.original_image = pygame.image.load(path).convert_alpha()
        self.alpha = alpha
        self.image = self.original_image.copy()  # Working copy
        self._process_transparency()
        self.cache = {}  # For scaled images: {radius: surface}
        self.color_cache = {}  # For colored images: {(r,g,b): surface}
        self.colored_scale_cache = {}  # For colored+scaled: {(radius, r,g,b): surface}
        self._generate_base_scale(base_size)
   
    def _process_transparency(self):
        """Convert pure white pixels to transparent and set colorkey"""
        for x in range(self.image.get_width()):
            for y in range(self.image.get_height()):
                if self.image.get_at((x, y)) == (255, 255, 255, 255):
                    self.image.set_at((x, y), (255, 255, 255, 0))
        self.image.set_colorkey((255, 255, 255))
   
    def _generate_base_scale(self, base_radius: int):
        """Generate and cache a scaled version of the image"""
        tile_size = int(base_radius * 2)
        scaled_tile = pygame.transform.smoothscale(
            self.image,
            (tile_size, tile_size)
        )
        if self.alpha < 255:
            scaled_tile.set_alpha(self.alpha)
       
        self.cache[base_radius] = scaled_tile
   
    def get_scaled_tile(self, radius: int) -> pygame.Surface:
        """Get a scaled tile, generating it if not cached"""
        if radius not in self.cache:
            self._generate_base_scale(radius)
        return self.cache[radius]
   
    def _create_colored_image(self, colour: tuple) -> pygame.Surface:
        """Create a colored version of the original image"""
        # Create a copy of the original processed image
        colored_image = self.image.copy()
        
        width = colored_image.get_width()
        height = colored_image.get_height()
        
        for x in range(width):
            for y in range(height):
                pixel = colored_image.get_at((x, y))
               
                # Skip fully transparent pixels
                if pixel.a == 0:
                    continue
               
                # Calculate brightness of the original pixel (grayscale value)
                brightness = (pixel.r * 0.299 + pixel.g * 0.587 + pixel.b * 0.114) / 255.0
               
                # Apply the target color scaled by brightness
                new_r = int(colour[0] * brightness)
                new_g = int(colour[1] * brightness)
                new_b = int(colour[2] * brightness)
               
                # Keep the original alpha value
                colored_image.set_at((x, y), (new_r, new_g, new_b, pixel.a))
        
        return colored_image
   
    def get_image_override_colours(self, colour: tuple) -> pygame.Surface:
        """Get a colored version of the image, using cache if available"""
        # Convert to tuple if it's a list for consistent hashing
        color_key = tuple(colour[:3])  # Take only RGB components
        
        # Check if we already have this color cached
        if color_key not in self.color_cache:
            self.color_cache[color_key] = self._create_colored_image(color_key)
        
        return self.color_cache[color_key]
    
    def get_colored_scaled_tile(self, radius: int, colour: tuple) -> pygame.Surface:
        """Get a colored and scaled tile, using cache if available"""
        # Convert to tuple for consistent hashing
        color_key = tuple(colour[:3])
        cache_key = (radius, color_key)
        
        # Check if we already have this combination cached
        if cache_key not in self.colored_scale_cache:
            # Get the colored image first
            colored_image = self.get_image_override_colours(color_key)
            
            # Scale the colored image
            tile_size = int(radius * 2)
            scaled_colored_tile = pygame.transform.smoothscale(
                colored_image,
                (tile_size, tile_size)
            )
            
            # Apply alpha if needed
            if self.alpha < 255:
                scaled_colored_tile.set_alpha(self.alpha)
            
            self.colored_scale_cache[cache_key] = scaled_colored_tile
        
        return self.colored_scale_cache[cache_key]
   
    def clear_cache(self):
        """Clear all caches to free memory"""
        self.cache.clear()
        self.color_cache.clear()
        self.colored_scale_cache.clear()
   
    def clear_color_cache(self):
        """Clear only the color caches"""
        self.color_cache.clear()
        self.colored_scale_cache.clear()
    
    def clear_scale_cache(self):
        """Clear only the scale caches"""
        self.cache.clear()
        self.colored_scale_cache.clear()
   
    def get_cache_size(self) -> dict:
        """Get the number of cached images in each cache"""
        return {
            "scale_cache": len(self.cache),
            "color_cache": len(self.color_cache),
            "colored_scale_cache": len(self.colored_scale_cache),
            "total": len(self.cache) + len(self.color_cache) + len(self.colored_scale_cache)
        }
    
    def preload_colors(self, colors: list):
        """Preload multiple colors into the cache"""
        for color in colors:
            self.get_image_override_colours(color)
    
    def preload_colored_scales(self, radius_color_pairs: list):
        """Preload multiple radius-color combinations
        
        Args:
            radius_color_pairs: List of (radius, color) tuples
        """
        for radius, color in radius_color_pairs:
            self.get_colored_scaled_tile(radius, color)

    def get_cache_memory_estimate(self) -> dict:
        """Get an estimate of memory usage by each cache"""
        def surface_memory(surface):
            return surface.get_width() * surface.get_height() * surface.get_bytesize()
        
        scale_memory = sum(surface_memory(surf) for surf in self.cache.values())
        color_memory = sum(surface_memory(surf) for surf in self.color_cache.values())
        colored_scale_memory = sum(surface_memory(surf) for surf in self.colored_scale_cache.values())
        
        return {
            "scale_cache_bytes": scale_memory,
            "color_cache_bytes": color_memory,
            "colored_scale_cache_bytes": colored_scale_memory,
            "total_bytes": scale_memory + color_memory + colored_scale_memory
        }
