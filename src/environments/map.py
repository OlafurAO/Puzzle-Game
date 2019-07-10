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

        #pygame.sprite.Sprite.__init__(self);

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


class Doorway:
    def __init__(self, game, id, name, direction, linked, x, y, w, h):
        pygame.sprite.Sprite.__init__(self);

        #self.name is the name and self.game is my game haha just a little programming joke
        self.game = game;
        self.id = id;
        self.name = name;
        self.direction = direction;
        self.linked = linked;
        self.rect = pygame.Rect(x, y, w, h);
        self.hit_rect = self.rect;

        self.x = x;
        self.y = y;

        self.width = w;
        self.height = h;

        self.rect.x = x;
        self.rect.y = y;

class Door:
    def __init__(self, game, id, direction, condition, x, y, w, h):
        self.game = game;
        self.id = id;
        self.direction = direction;
        self.condition = condition;
        self.rect = pygame.Rect(x, y, w, h);
        self.hit_rect = self.rect;

        self.x = x;
        self.y = y;

        self.width = w;
        self.height = h;

        self.rect.x = x;
        self.rect.y = y;

        self.is_open = False;


    def draw_door(self):
        if not (self.is_door_open()):
            if(self.get_direction() == 'UP' or self.get_direction() == 'DOWN'):
                for i in range(int(self.x), int(self.x + self.width - 10), 10):
                    pygame.draw.rect(self.game.game_display, (108, 60, 0), [i, self.y - 80, 10, 100]);
            else:
                for i in range(int(self.y), int(self.height + self.y - 10), 10):
                    pygame.draw.rect(self.game.game_display, (108, 60, 0), [self.x, i, 100, 10]);


    def open_door(self):
        self.is_open = True;


    def get_condition(self):
        return self.condition;


    def get_direction(self):
        return self.direction;


    def is_door_open(self):
        return self.is_open;
