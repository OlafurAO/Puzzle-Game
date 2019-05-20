import pygame;
import pytmx;

class Camera:
    def __init__(self, game_display, screen_size, player_one, player_two, map_art, location):
        self.game_display = game_display;
        self.screen_size = screen_size;

        self.player_one = player_one;
        self.player_two = player_two;

        self.map_location = location;
        #self.game = game;

        self.map = map_art;


    def update_map(self):
        self.draw_map();

    def draw_map(self):
        self.game_display.blit(self.map, (self.map_location[0], self.map_location[1]));


class Map:
    def __init__(self, file_name):
        map = pytmx.load_pygame(file_name, pixelalpha=True);

        self.width = map.width * map.tilewidth;
        self.height = map.height * map.tileheight;
        self.tmxdata = map;


    def draw_map(self, surface):
        tile_id = self.tmxdata.get_tile_image_by_gid;

        for layer in self.tmxdata.visible_layers:
            if (isinstance(layer, pytmx.TiledTileLayer)):
                for x, y, gid, in layer:
                    tile = tile_id(gid);

                    if (tile):
                        surface.blit(tile, [x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight]);


    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height));
        self.draw_map(temp_surface);

        return temp_surface;


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, name, x, y, w, h):
        #self.groups = game.walls;
        #pygame.sprite.Sprite.__init__(self, self.groups);

        pygame.sprite.Sprite.__init__(self);

        #self.name is the name and self.game is my game haha just a little programming joke
        self.game = game;
        self.name = name;
        self.rect = pygame.Rect(x, y, w, h);
        self.hit_rect = self.rect;

        self.x = x;
        self.y = y;

        self.width = w;
        self.height = h;

        self.rect.x = x;
        self.rect.y = y;