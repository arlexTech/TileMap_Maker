import pygame
import json
import os
import datetime

#Parameters (all optionnal)
tilesets_folder = "pokemon_tilesets" #Optionnal default is "tilesets"
adapt_to_screen=True #Optionnal default is True
#if False use the following parameters:
ntiles_width=58 #width=ntiles_width*33 by default so 58*33=1914
ntiles_height=32 #height=ntiles_height*33 by default so 32*33=1056

#Controls
move_keys=[
                pygame.K_z,
    pygame.K_q, pygame.K_s,  pygame.K_d
]

map_saves_folder="map_saves/"
temp_map=".temp.json"
map_exports_folder="map_exports/"

pygame.init()
pygame.display.set_caption("Map Editor")


class Game:
    def __init__(self, vel=1, space_between_tiles=1, tile_size=32, ntiles_tileset_width=8,adapt_to_screen=True, ntiles_width=19, ntiles_height=10,font=pygame.font.SysFont("monospace", 10)):
        self.font=font
        self.vel = vel
        self.space_between_tiles = space_between_tiles
        self.tile_size = tile_size
        self.default_tile_size=tile_size
        self.tile_size_p1 = tile_size + space_between_tiles
        self.tile_size_p2 = self.tile_size_p1 + space_between_tiles

        self.ntiles_tileset_width=ntiles_tileset_width
        self.tileset_width=self.tile_size_p1*ntiles_tileset_width

        if adapt_to_screen:
            info = pygame.display.Info()  # Get display info
            win_height=max(info.current_h//4*3,(10)*self.tile_size_p1)
            win_width=max(info.current_w//4*3,(10+1+self.ntiles_tileset_width)*self.tile_size_p1)
            self.win_height=win_height
            self.win_width=win_width
            self.resize_window((win_width,win_height))
        else:
            self.ntiles_height=ntiles_height
            self.ntiles_width=ntiles_width
            self.ntiles_map_width=self.ntiles_width-self.ntiles_tileset_width

            self.map_width=self.tile_size_p1*self.ntiles_map_width

            self.width = self.map_width+self.tile_size_p1+self.tileset_width
            self.height = self.ntiles_height*self.tile_size_p1
            self.win_height=win_height=self.height
            self.win_width=win_width=self.width
        self.win = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        
        self.update_hached_tile()
        self.tileset_index_display=pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)

    def resize_window(self, dims=None):
        if dims:
            self.win_width, self.win_height = win_width, win_height = dims
        
        self.ntiles_height=self.win_height//self.tile_size_p1+1
        self.ntiles_map_width=self.win_width//self.tile_size_p1-self.ntiles_tileset_width-1
        self.ntiles_width=self.ntiles_map_width+self.ntiles_tileset_width+1

        self.map_width=self.tile_size_p1*self.ntiles_map_width

        self.height=self.ntiles_height*self.tile_size_p1
        self.width=self.ntiles_width*self.tile_size_p1

    def update_hached_tile(self):
        self.hatched_tile = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        self.hatched_tile.fill((230, 230, 230))

        step = 10 
        line_color = (240, 240, 240)

        for offset in range(-self.tile_size, self.tile_size, step):
            pygame.draw.line(self.hatched_tile, line_color, (offset, 0), (offset + self.tile_size, self.tile_size), 1)
    
    def update_sizes(self,dims=None):
        self.tile_size_p1 = self.tile_size + self.space_between_tiles
        self.tile_size_p2 = self.tile_size_p1 + self.space_between_tiles
        self.resize_window(dims)
        self.font=pygame.font.SysFont("monospace", self.tile_size//3)
        self.update_hached_tile()

    def resize_tile_add(self,x):
        if 0<self.tile_size+x*5<100:
            self.tile_size+=x*5
        
    def resize_tile_default(self):
        self.tile_size=self.default_tile_size
        self.update_sizes()

    def get_size(self):
        return self.width, self.height

    def get_surface(self):
        return self.win

class Button:
    def __init__(self,surface,dest=0,display_dest=False,tile_size=32,font="monospace",button_type="number",color=(0,0,0),bg_color=(200,200,200)):
        self.surface = surface
        self.dest=dest
        self.display_dest=display_dest
        self.tile_size=tile_size
        self.font=font
        self.button_type=button_type
        self.pyfont=pygame.font.SysFont(self.font, self.tile_size)
        self.color=color
        self.bg_color=bg_color
        self.update_size()

    def def_dest(self,dest):
        self.dest=dest
        self.update_size()

    def update_size(self,size=False):
        if size:
            self.tile_size=size
            self.pyfont=pygame.font.SysFont(self.font, self.tile_size)
        match self.button_type:
            case "number":
                self.number()
            
            case "up_arrow":
                self.up_arrow()

            case "down_arrow":
                self.down_arrow()

            case "double_up_arrow":
                self.double_up_arrow()
            
            case "double_down_arrow":
                self.double_down_arrow()

    def number(self):
        self.surface=pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        self.surface.fill(self.bg_color)
        text_surface = self.pyfont.render(str(self.dest), True, self.color)
        text_rect = text_surface.get_rect(center=(self.tile_size // 2, self.tile_size // 2))
        self.surface.blit(text_surface, text_rect)
        
    def up_arrow(self):
        #Update buttons size
        # Draw up arrow (▲)
        self.surface=pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        self.surface.fill(self.bg_color)
        pygame.draw.polygon(self.surface, self.color, [
            (self.tile_size // 2, self.tile_size // 4),  # Top point
            (self.tile_size // 4, self.tile_size * 3 // 4),  # Bottom left
            (self.tile_size * 3 // 4, self.tile_size * 3 // 4)  # Bottom right
        ])

    def down_arrow(self):
        # Draw down arrow (▼)
        self.surface=pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        self.surface.fill(self.bg_color)
        pygame.draw.polygon(self.surface, self.color, [
            (self.tile_size // 2, self.tile_size * 3 // 4),  # Bottom point
            (self.tile_size // 4, self.tile_size // 4),  # Top left
            (self.tile_size * 3 // 4, self.tile_size // 4)  # Top right
        ])

    def double_up_arrow(self):
        # First arrow (⏫) - Double Up Arrow with better alignment
        self.surface=pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        self.surface.fill(self.bg_color)
        pygame.draw.polygon(self.surface, self.color, [
            (self.tile_size // 2, self.tile_size // 6),  # Top point (higher)
            (self.tile_size // 4, self.tile_size // 2),  # Middle left
            (self.tile_size * 3 // 4, self.tile_size // 2)  # Middle right
        ])
        pygame.draw.polygon(self.surface, self.color, [
            (self.tile_size // 2, self.tile_size * 5 // 12),  # Lower point (moved up slightly)
            (self.tile_size // 4, self.tile_size * 3 // 4),  # Bottom left
            (self.tile_size * 3 // 4, self.tile_size * 3 // 4)  # Bottom right
        ])

    def double_down_arrow(self):
        # Last arrow (⏬) - Double Down Arrow with better alignment
        self.surface=pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        self.surface.fill(self.bg_color)
        pygame.draw.polygon(self.surface, self.color, [
            (self.tile_size // 2, self.tile_size * 5 // 6),  # Bottom point (lower)
            (self.tile_size // 4, self.tile_size // 2),  # Middle left
            (self.tile_size * 3 // 4, self.tile_size // 2)  # Middle right
        ])
        pygame.draw.polygon(self.surface, self.color, [
            (self.tile_size // 2, self.tile_size * 7 // 12),  # Upper point (moved down slightly)
            (self.tile_size // 4, self.tile_size // 4),  # Top left
            (self.tile_size * 3 // 4, self.tile_size // 4)  # Top right
        ])

    def lead(self,data):
        data.goto_tileset(self.dest)

class Coo:
    def __init__(self,x=0,y=0):
        self.x=x
        self.y=y

    def redef(self,c,y=None):
        if type(c)==type(self):
            self.x=c.x
            self.y=c.y
        elif type(c)==type([]):
            self.x=c[0]
            self.y=c[1]
        elif y!=None and type(c)==type(0):
            self.x=c
            self.y=y

    def add(self,c):
        if type(c)==type(self):
            self.x+=c.x
            self.y+=c.y
        else:
            self.x+=c[0]
            self.y+=c[1]
    
    def get(self):
        return [self.x,self.y]

class Data:
    def __init__(self, game, x=0, y=0, selected_map_tile=[0,0], selected_tileset_tile=[0,0], selected_tile_layer=0, x_tileset=0,tilesets_folder="tilesets",start_tile = 0):
        self.game = game
        self.coo = Coo(x,y)
        self.selected_map_tile = selected_map_tile
        self.selected_tile_layer = selected_tile_layer
        self.selected_tileset_tile = selected_tileset_tile
        self.x_tileset = x_tileset
        self.tileset_index = 0
        self.load_map(temp_map)

        # Get all PNG files in the folder
        png_files = sorted([f for f in os.listdir(tilesets_folder) if f.endswith(".png")])
        self.sets = []
        self.tilesets = {}

        for png in png_files:
            name = os.path.splitext(png)[0]  # Remove .png extension
            image = pygame.image.load(os.path.join(tilesets_folder, png)).convert_alpha()
            
            # Get the height in tiles
            height_in_tiles = image.get_height() // self.game.tile_size
            
            # Add entry to sets
            self.sets.append((name, start_tile, start_tile + height_in_tiles))

            # Store in tilesets dictionary
            self.tilesets[name] = image

            # Update start_tile for the next tileset
            start_tile += height_in_tiles

        self.default= [[0,0,""]]

        self.buttons = []
        self.buttons.append(Button(pygame.Surface((self.game.tile_size, self.game.tile_size), pygame.SRCALPHA), 0, color = (30, 30, 120), bg_color = (230, 230, 230)))
        self.buttons.append(Button(pygame.Surface((self.game.tile_size, self.game.tile_size), pygame.SRCALPHA), 0, button_type="double_up_arrow"))
        self.buttons.append(Button(pygame.Surface((self.game.tile_size, self.game.tile_size), pygame.SRCALPHA), 0, button_type="up_arrow"))
        for i in range(4): self.buttons.append(Button(pygame.Surface((self.game.tile_size, self.game.tile_size), pygame.SRCALPHA), i+1))
        self.buttons.append(Button(pygame.Surface((self.game.tile_size, self.game.tile_size), pygame.SRCALPHA), 0, button_type="down_arrow"))
        self.buttons.append(Button(pygame.Surface((self.game.tile_size, self.game.tile_size), pygame.SRCALPHA), -1, button_type="double_down_arrow"))

    def load_map(self,map=False):
        if not map:
            files = [f for f in os.listdir(map_saves_folder) if f.startswith("map_") and f.endswith(".json")]
            print(files)
            if files:
                filename = map_saves_folder+max(files, key=lambda x: int(x.split("_")[-1].split(".")[0]))
            else:
                filename = "map_saves/.temp.json"
        else:
            filename=map_saves_folder+map

        if not os.path.exists(filename):
            print(f"{filename} not found. Creating a new one...")
            with open(filename, "w") as f:
                json.dump([[]], f, indent=4)
        with open(filename,"r") as f:
            self.map=json.loads(f.read())

    def save_map(self,map=False):
        if not map:
            filename = map_saves_folder+f"map_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        else:
            filename=map_saves_folder+map
            
        with open(filename,"w+") as f:
            f.write(json.dumps(self.map))
        
        if map!=temp_map:
            print(f"Map saved as {map_saves_folder}{filename}")

    def export_map(self):
        print("Exporting map")
        map_surface = pygame.Surface((len(self.map[0])*self.game.default_tile_size,len(self.map)*self.game.default_tile_size), pygame.SRCALPHA)
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                for k in range(len(self.map[i][j])):
                    if self.map[i][j][k][2] != "":
                        map_surface.blit(self.tilesets[self.map[i][j][k][2]], (j*self.game.default_tile_size, i*self.game.default_tile_size),(self.map[i][j][k][1]*self.game.default_tile_size,self.map[i][j][k][0]*self.game.default_tile_size,self.game.default_tile_size,self.game.default_tile_size))
        name=f"map_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        pygame.image.save(map_surface, map_exports_folder+name)
        print("Map exported as",name)

    def reduce_map(self):
        shrink=True
        while shrink and len(self.map)>1:
            for j in self.map[0]:
                if j!=self.default:
                    shrink=False
                    break
            if shrink:
                del self.map[0]
                self.coo.x-=1
                self.selected_map_tile[0]-=1

        i=len(self.map)-1
        if i>0:
            shrink=True
            while shrink:
                for j in self.map[i]:
                    if j!=self.default:
                        shrink=False
                        break
                if shrink:
                    del self.map[i]
                    i-=1
                if i<=0:
                    shrink=False

        shrink=True
        while shrink and len(self.map[0])>1:
            for j in self.map:
                if j[0]!=self.default:
                    shrink=False
                    break
            if shrink:
                for j in self.map:
                    del j[0]
                self.coo.y-=1
                self.selected_map_tile[1]-=1

        i=len(self.map[0])-1
        if i>0:
            shrink=True
            while shrink:
                for j in self.map:
                    if j[i]!=self.default:
                        shrink=False
                        break
                if shrink:
                    for j in self.map:
                        del j[i]
                    i-=1
                if i<=0:
                    shrink=False

    def map_is_large_enough(self):
        coo=self.selected_map_tile.copy()
        while coo[0]<0:
            self.map.insert(0,[self.default.copy() for _ in range(len(self.map[0]))])
            coo[0]+=1
            self.coo.x+=1
            self.selected_map_tile[0]+=1
        while coo[1]<0:
            for l in self.map:
                l.insert(0,self.default.copy())
            coo[1]+=1
            self.coo.y+=1
            self.selected_map_tile[1]+=1
        while len(self.map)<=coo[0]:
            self.map.append([self.default.copy() for _ in range(len(self.map[0]))])
        for l in self.map:
            while len(l)<=coo[1]:
                l.append(self.default.copy())

    def remove_layer(self,coo=False,layer=-1,all=False):
        if not coo:
            coo=self.selected_map_tile
        if 0<=coo[0]<len(self.map) and 0<=coo[1]<len(self.map[coo[0]]):
            if all or len(self.map[coo[0]][coo[1]])==1:
                self.map[coo[0]][coo[1]]=self.default.copy()
                self.reduce_map()
            else:
                if len(self.map[coo[0]][coo[1]])>layer:
                    del self.map[coo[0]][coo[1]][layer]
    
    def wich_tile(self):
        for t in self.sets:
            if self.selected_tileset_tile[0]<t[2]:
                return [self.selected_tileset_tile[0]-t[1],self.selected_tileset_tile[1],t[0]]
        
    def map_set_tile(self,use_layer=False,custom_tile=False,replace=False):
        self.map_is_large_enough()
        if custom_tile:
            if replace:
                self.map[self.selected_map_tile[0]][self.selected_map_tile[1]]=custom_tile
            else:
                for t in custom_tile:
                    self.map[self.selected_map_tile[0]][self.selected_map_tile[1]].append(t)
        else:
            if use_layer:
                layer=self.selected_tile_layer
            else:
                layer=len(self.map[self.selected_map_tile[0]][self.selected_map_tile[1]])

            if self.map[self.selected_map_tile[0]][self.selected_map_tile[1]][0]==self.default[0]:
                del self.map[self.selected_map_tile[0]][self.selected_map_tile[1]][0]
                
            if len(self.map[self.selected_map_tile[0]][self.selected_map_tile[1]])>layer:
                self.map[self.selected_map_tile[0]][self.selected_map_tile[1]][layer]=self.wich_tile()
            else:
                self.map[self.selected_map_tile[0]][self.selected_map_tile[1]].append(self.wich_tile())
        self.reduce_map()

    def update_buttons(self):
        self.tileset_index=self.index_of_tileset()
        self.buttons[0].def_dest(self.tileset_index)
        self.buttons[2].def_dest(max(0,self.tileset_index-1))
        self.buttons[7].def_dest(min(len(self.sets)-1,self.tileset_index+1))
        
        if 0==self.tileset_index:
            dests=[2,3,4,5]
        elif 1==self.tileset_index:
            dests=[3,4,5,6]

        elif len(self.sets)-1==self.tileset_index:
            dests=[self.tileset_index-5,self.tileset_index-4,self.tileset_index-3,self.tileset_index-2]
        elif len(self.sets)-2==self.tileset_index:
            dests=[self.tileset_index-6,self.tileset_index-5,self.tileset_index-4,self.tileset_index-3]

        else:
            dests=[self.tileset_index-2,self.tileset_index-1,self.tileset_index+1,self.tileset_index+2]
        
        for i in range(min(4,len(self.sets)-1)):
            self.buttons[i+3].def_dest(dests[i])

    def goto_tileset(self,x):
        self.x_tileset=self.sets[x][1]
        self.update_buttons()

    def index_of_tileset(self):
        for i,t in enumerate(self.sets):
            if t[2]>self.x_tileset:
                return i
        return len(self.sets)-2

    def add_x_tileset(self,x):
        if 0<=self.x_tileset+x:
            self.x_tileset+=x
            self.update_buttons()

    def update_sizes(self,dims=False):
        self.game.update_sizes(dims)
        for b in self.buttons:
            b.update_size(self.game.tile_size)

    def resize_tile_add(self,x):
        self.game.resize_tile_add(x)
        self.update_sizes()


data=Data(Game(ntiles_height=ntiles_height,ntiles_width=ntiles_width),tilesets_folder=tilesets_folder)
data.update_buttons()

move_coo=Coo()
mouse0_last_pos=(pygame.mouse.get_pos(),move_coo.get())
key_released=True

pressed_keys = []
def first_press(key):
    cm=key not in pressed_keys and keys[key]
    if cm:
        pressed_keys.append(key)
    return cm

if not os.path.exists(map_saves_folder):
    os.makedirs(map_saves_folder)
mouse0_released=True
mouse2_released=True
mouse_on_map=False
run = True
clipboard=data.default
win_dimensions=data.game.get_size()


def file_selection_menu(screen):
    BG_COLOR = (30, 30, 30)
    TEXT_COLOR = (255, 255, 255)
    HIGHLIGHT_COLOR = (100, 100, 255)
    font = pygame.font.Font(None, 36)
    fsm = True
    selected_index = None
    files = [f for f in os.listdir(map_saves_folder) if f.endswith(".json")]
    while fsm:
        screen.fill(BG_COLOR)
        y_offset = 50

        for i, file in enumerate(files):
            color = HIGHLIGHT_COLOR if i == selected_index else TEXT_COLOR
            text_surface = font.render(file, True, color)
            screen.blit(text_surface, (50, y_offset))
            y_offset += 40

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None  # User closed the window

            if event.type == pygame.MOUSEMOTION:
                # Highlight file under mouse cursor
                mx, my = event.pos
                selected_index = (my - 50) // 40 if 50 <= my <= 50 + len(files) * 40 else None

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                if selected_index is not None and 0 <= selected_index < len(files):
                    return files[selected_index]


while run:
    data.game.win.fill((255,255,255))
    keys = pygame.key.get_pressed()
    if all(not key for key in keys):
        key_released=True
    
    for i in range(len(pressed_keys)):
        if not keys[pressed_keys[i]]:
            del pressed_keys[i]
            break
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEWHEEL:  # Detect scrolling
            if keys[pygame.K_LCTRL]:
                overed_tile_pos=[pygame.mouse.get_pos()[1]//data.game.tile_size_p1+data.coo.x,pygame.mouse.get_pos()[0]//data.game.tile_size_p1+data.coo.y]
                data.resize_tile_add(event.y)
                new_overed_tile_pos=[pygame.mouse.get_pos()[1]//data.game.tile_size_p1+data.coo.x,pygame.mouse.get_pos()[0]//data.game.tile_size_p1+data.coo.y]
                data.coo.add([overed_tile_pos[i] - new_overed_tile_pos[i] for i in range(len(overed_tile_pos))])
            elif pygame.mouse.get_pos()[0]<data.game.map_width:
                data.coo.add([-event.y,event.x])
            else:
                if keys[pygame.K_LSHIFT]:
                    data.add_x_tileset(-event.y*5)
                else:
                    data.add_x_tileset(-event.y)
        elif event.type == pygame.VIDEORESIZE:  # Detect window resize
            win_dimensions = event.w,event.h
            data.update_sizes(win_dimensions)

    if keys[pygame.K_ESCAPE]:
        run=False
    if keys[pygame.K_LEFT] or keys[move_keys[1]]:
        data.coo.y -= data.game.vel
    if keys[pygame.K_RIGHT]  or keys[move_keys[3]]:
        data.coo.y += data.game.vel
    if keys[pygame.K_UP] or keys[move_keys[0]]:
        data.coo.x -= data.game.vel
    if keys[pygame.K_DOWN] or (keys[move_keys[2]] and not keys[pygame.K_LCTRL]):
        data.coo.x += data.game.vel
    if keys[pygame.K_PAGEUP] and data.x_tileset>0:
        data.add_x_tileset(-data.game.vel)
    if keys[pygame.K_PAGEDOWN]:
        data.add_x_tileset(data.game.vel)

    if keys[pygame.K_KP0] or keys[pygame.K_0]:
        data.selected_tile_layer=0
    if keys[pygame.K_KP1] or keys[pygame.K_1]:
        data.selected_tile_layer=1
    if keys[pygame.K_KP2] or keys[pygame.K_2]:
        data.selected_tile_layer=2
    if keys[pygame.K_KP3] or keys[pygame.K_3]:
        data.selected_tile_layer=3
    
    if first_press(pygame.K_KP4):
        data.selected_map_tile[1]-=1
    if first_press(pygame.K_KP5):
        data.selected_map_tile[0]+=1
    if first_press(pygame.K_KP6):
        data.selected_map_tile[1]+=1
    if first_press(pygame.K_KP8):
        data.selected_map_tile[0]-=1

    if first_press(pygame.K_r):
        data.reduce_map()
    
    if first_press(pygame.K_s) and keys[pygame.K_LCTRL]:
        if keys[pygame.K_LSHIFT]:
            data.save_map(input("Enter the name of the file to save (without .json): ")+".json")
        else:
            data.save_map()
    
    if first_press(pygame.K_o):
        if keys[pygame.K_LCTRL]:
            data.load_map(file_selection_menu(data.game.win))#input("Enter the name of the file to open (without .json): ")+".json")
        else:
            data.load_map()

    if first_press(pygame.K_DELETE):
        data.remove_layer(all=True)
        
    if first_press(pygame.K_KP_MINUS) or first_press(pygame.K_MINUS):
        data.remove_layer()

    if first_press(pygame.K_e):
        data.export_map()

    if first_press(pygame.K_c) and keys[pygame.K_LCTRL]:
        clipboard=data.map[data.selected_map_tile[0]][data.selected_map_tile[1]].copy()

    if first_press(pygame.K_v) and keys[pygame.K_LCTRL]:
        if keys[pygame.K_LSHIFT]:
            data.map_set_tile(custom_tile=clipboard,replace=True)
        else:
            data.map_set_tile(custom_tile=clipboard)
    
    if first_press(pygame.K_p):
        print(data.map[data.selected_map_tile[0]][data.selected_map_tile[1]])
        
    ############################################################################################################
    #                                           Left click                                                     #
    ############################################################################################################
    if pygame.mouse.get_pressed()[0]==1:
        if mouse0_released:
            mouse0_released=False
            mouse0_last_pos=(pygame.mouse.get_pos(),move_coo.get())

            #Click on the map
            if pygame.mouse.get_pos()[0]<data.game.map_width:
                mouse_on_map=True
                overed_tile_pos=[pygame.mouse.get_pos()[1]//data.game.tile_size_p1+data.coo.x,pygame.mouse.get_pos()[0]//data.game.tile_size_p1+data.coo.y]
                if keys[pygame.K_LCTRL]:
                    data.remove_layer(overed_tile_pos,all=True)
                else:
                    if data.selected_map_tile!=overed_tile_pos:
                        data.selected_map_tile=overed_tile_pos
                    else:
                        data.map_set_tile()

            #Click on a layer
            elif pygame.mouse.get_pos()[1]<data.game.tile_size_p1:
                data.selected_tile_layer=pygame.mouse.get_pos()[0]//data.game.tile_size_p1-data.game.ntiles_map_width-1

            #Click on a button
            elif pygame.mouse.get_pos()[1]<data.game.tile_size_p1*2:
                data.buttons[(pygame.mouse.get_pos()[0]//data.game.tile_size_p1-data.game.ntiles_map_width)].lead(data)
            
            #Click on the tileset
            else:
                if pygame.mouse.get_pos()[0]//data.game.tile_size_p1-data.game.ntiles_map_width-1>=0 and pygame.mouse.get_pos()[1]>2*data.game.tile_size_p1:
                    overed_tile_pos=[pygame.mouse.get_pos()[1]//data.game.tile_size_p1+data.x_tileset-2,pygame.mouse.get_pos()[0]//data.game.tile_size_p1-data.game.ntiles_map_width-1]
                    if data.selected_tileset_tile!=overed_tile_pos:
                        data.selected_tileset_tile=overed_tile_pos
                    else:
                        data.map_set_tile()
        else:
            if mouse_on_map:
                move_coo.redef(mouse0_last_pos[1][0]-(pygame.mouse.get_pos()[1]-mouse0_last_pos[0][1])//data.game.tile_size_p1,mouse0_last_pos[1][1]-(pygame.mouse.get_pos()[0]-mouse0_last_pos[0][0])//data.game.tile_size_p1)
 
    else:
        if not mouse0_released:
            mouse_on_map=False
            data.coo.redef(data.coo.x+move_coo.x,data.coo.y+move_coo.y)
            move_coo.redef(0,0)
        mouse0_released=True
    
    ############################################################################################################
    #                                           Right click                                                    #
    ############################################################################################################
    if pygame.mouse.get_pressed()[2]==1:
        if mouse2_released:
            mouse2_released=False
            #Click on the map
            if pygame.mouse.get_pos()[0]<data.game.map_width:
                coo=[pygame.mouse.get_pos()[1]//data.game.tile_size_p1+data.coo.x,pygame.mouse.get_pos()[0]//data.game.tile_size_p1+data.coo.y]
                if keys[pygame.K_LCTRL]:
                    data.remove_layer(coo,all=True)
                else:
                    data.remove_layer(coo)
            #Click on a layer
            elif pygame.mouse.get_pos()[1]<data.game.tile_size_p1:
                data.remove_layer(layer=pygame.mouse.get_pos()[0]//data.game.tile_size_p1-data.game.ntiles_map_width-1)

            #Click on the tileset
            else:
                if pygame.mouse.get_pos()[0]//data.game.tile_size_p1-data.game.ntiles_map_width-1>=0 and pygame.mouse.get_pos()[1]>2*data.game.tile_size_p1:
                    data.selected_tileset_tile=[pygame.mouse.get_pos()[1]//data.game.tile_size_p1+data.x_tileset-2,pygame.mouse.get_pos()[0]//data.game.tile_size_p1-data.game.ntiles_map_width-1]
                    data.map_set_tile(False)
    else:
        mouse2_released=True
    

    ############################################################################################################
    #                                               Display                                                    #
    ############################################################################################################
    temp_x=data.coo.x+move_coo.x
    temp_y=data.coo.y+move_coo.y

    #Highlight selected map tile
    if 0<=data.selected_map_tile[0]-temp_x<data.game.ntiles_height and 0<=data.selected_map_tile[1]-temp_y<data.game.ntiles_map_width:
        pygame.draw.rect(data.game.win,(0,0,0),((data.selected_map_tile[1]-temp_y)*data.game.tile_size_p1-1,(data.selected_map_tile[0]-temp_x)*data.game.tile_size_p1-1, data.game.tile_size_p2, data.game.tile_size_p2))
        pygame.draw.rect(data.game.win,(255,255,255),((data.selected_map_tile[1]-temp_y)*data.game.tile_size_p1,(data.selected_map_tile[0]-temp_x)*data.game.tile_size_p1, data.game.tile_size, data.game.tile_size))
        
    #Highlight selected layer tile
    pygame.draw.rect(data.game.win,(0,0,0),((data.selected_tile_layer+data.game.ntiles_map_width+1)*data.game.tile_size_p1-1,0, data.game.tile_size_p2, data.game.tile_size_p1))
    pygame.draw.rect(data.game.win,(255,255,255),((data.selected_tile_layer+data.game.ntiles_map_width+1)*data.game.tile_size_p1,0, data.game.tile_size, data.game.tile_size))
    
    #Highlight selected tileset tile
    if 0<=data.selected_tileset_tile[0]-data.x_tileset<data.game.ntiles_height:
        pygame.draw.rect(data.game.win,(0,0,0),((data.selected_tileset_tile[1]+data.game.ntiles_map_width+1)*data.game.tile_size_p1-1,(data.selected_tileset_tile[0]-data.x_tileset+2)*data.game.tile_size_p1-1, data.game.tile_size_p2, data.game.tile_size_p2))
        pygame.draw.rect(data.game.win,(255,255,255),((data.selected_tileset_tile[1]+data.game.ntiles_map_width+1)*data.game.tile_size_p1,(data.selected_tileset_tile[0]-data.x_tileset+2)*data.game.tile_size_p1, data.game.tile_size, data.game.tile_size))

    #Display selected map tile coordinates
    data.game.win.blit(data.game.font.render(str(data.selected_map_tile), 1, (0,0,0)), (data.game.ntiles_map_width*data.game.tile_size_p1-3, 8))

    fill_tile = pygame.Surface((data.game.default_tile_size, data.game.default_tile_size), pygame.SRCALPHA)
    fill_tile.fill((255, 255, 255, 0))

    #Display map
    for i in range(data.game.ntiles_height):
        for j in range(data.game.ntiles_map_width):
            if 0<=temp_x+i<len(data.map) and 0<=temp_y+j<len(data.map[temp_x+i]):
                for k in range(0,len(data.map[temp_x+i][temp_y+j])):
                    if data.map[temp_x+i][temp_y+j][k][2]=="":
                        tile=fill_tile
                    else:
                        tile=data.tilesets[data.map[temp_x+i][temp_y+j][k][2]].subsurface(pygame.Rect(
                            data.map[temp_x+i][temp_y+j][k][1]*data.game.default_tile_size,
                            data.map[temp_x+i][temp_y+j][k][0]*data.game.default_tile_size,
                            data.game.default_tile_size,
                            data.game.default_tile_size
                        ))
                    data.game.win.blit(
                        pygame.transform.scale(
                            tile,
                            (   
                                data.game.tile_size,
                                data.game.tile_size
                            )
                        ),
                        (
                            j*data.game.tile_size_p1,
                            i*data.game.tile_size_p1
                        )
                    )
            else:
                data.game.win.blit(data.game.hatched_tile, (j * data.game.tile_size_p1, i * data.game.tile_size_p1))
            if i==0:
                data.game.win.blit(data.game.font.render(str(j+temp_y), 1, (0,0,0)), (j*data.game.tile_size_p1+10, 0))
        data.game.win.blit(data.game.font.render(str(i+temp_x), 1, (0,0,0)), (0, i*data.game.tile_size_p1+10))
    
    #Display tileset
    for j in range(2,data.game.ntiles_height):
        for t in data.sets:
            if data.x_tileset+j-2<t[2]:
                ts=[data.tilesets[t[0]],t[1]]
                break
        if data.x_tileset+j-2<t[2]:

            for i in range(data.game.ntiles_map_width+1,data.game.ntiles_map_width+1+data.game.ntiles_tileset_width):
                data.game.win.blit(
                    pygame.transform.scale(
                        ts[0].subsurface(pygame.Rect((
                            i-data.game.ntiles_map_width-1)*data.game.default_tile_size,
                            (data.x_tileset+j-2-ts[1])*data.game.default_tile_size,
                            data.game.default_tile_size,
                            data.game.default_tile_size
                        )),
                        (
                            data.game.tile_size,
                            data.game.tile_size
                        )
                    ),
                    (
                        i*data.game.tile_size_p1,
                        j*data.game.tile_size_p1
                    )
                )

    #Display selected tile layers
    if 0<=data.selected_map_tile[0]<len(data.map) and 0<=data.selected_map_tile[1]<len(data.map[data.selected_map_tile[0]]):
        for i in range(len(data.map[data.selected_map_tile[0]][data.selected_map_tile[1]])):
            if data.map[data.selected_map_tile[0]][data.selected_map_tile[1]][i][2]=="":
                tile=fill_tile
            else:
                tile=data.tilesets[data.map[data.selected_map_tile[0]][data.selected_map_tile[1]][i][2]].subsurface(pygame.Rect(
                    (data.map[data.selected_map_tile[0]][data.selected_map_tile[1]][i][1])*data.game.default_tile_size,
                    (data.map[data.selected_map_tile[0]][data.selected_map_tile[1]][i][0])*data.game.default_tile_size,
                    data.game.default_tile_size,
                    data.game.default_tile_size
                ))
            data.game.win.blit(
                pygame.transform.scale(
                    tile,
                    (data.game.tile_size, data.game.tile_size)
                ),
                (
                    (data.game.ntiles_map_width+i+1)*data.game.tile_size_p1,
                    0
                )
            )
    
    #Display buttons
    for i in range(len(data.buttons)):
        data.game.win.blit(
            data.buttons[i].surface,
            (
                (data.game.ntiles_map_width+i)*data.game.tile_size_p1,
                data.game.tile_size_p1
            ),
            (
                0,
                0,
                data.game.tile_size,
                data.game.tile_size
            )
        )
    
    pygame.display.update()
    data.save_map(temp_map)
pygame.quit()