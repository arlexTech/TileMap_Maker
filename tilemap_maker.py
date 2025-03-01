import pygame
import time
import json
import os


#Parameters
tilesets_folder = "pokemon_tilesets"
ntiles_width=58 #width=ntiles_width*33 by default so 58*33=1914
ntiles_height=32 #height=ntiles_height*33 by default so 32*33=1056

#Controls
move_keys=[
                pygame.K_z,
    pygame.K_q, pygame.K_s,  pygame.K_d
]




pygame.init()
pygame.display.set_caption("Map Editor")

vel = 1

space_between_tiles = 1 #1
tile_size = 32 #32
total_size1 = tile_size + space_between_tiles
total_size2 = total_size1 + space_between_tiles

ntiles_tileset_width=8
ntiles_map_width=ntiles_width-ntiles_tileset_width


tileset_width=total_size1*ntiles_tileset_width
map_width=total_size1*ntiles_map_width
print("Map width:",map_width)
print("Tileset width:",tileset_width)

height=ntiles_height*total_size1
width=map_width+tileset_width+total_size1
print("Width:",width)

win = pygame.display.set_mode((width,height),pygame.RESIZABLE)
myfont = pygame.font.SysFont("monospace", 50)
bestfont = pygame.font.SysFont("monospace", 10)

#sets=[("Mansion interior",0,29),("Boat",29,89)]
#tilesets = {}
#for s in sets:
#    tilesets[s[0]]=pygame.image.load("Tilesets/"+s[0]+".PNG").convert_alpha()

# Get all PNG files in the folder
png_files = sorted([f for f in os.listdir(tilesets_folder) if f.endswith(".PNG")])
print("Loaded tilesets: ",png_files)
sets = []
tilesets = {}

start_tile = 0  # First tile index starts at 0

for png in png_files:
    name = os.path.splitext(png)[0]  # Remove .PNG extension
    image = pygame.image.load(os.path.join(tilesets_folder, png)).convert_alpha()
    
    # Get the height in tiles
    height_in_tiles = image.get_height() // tile_size
    
    # Add entry to sets
    sets.append((name, start_tile, start_tile + height_in_tiles))

    # Store in tilesets dictionary
    tilesets[name] = image

    # Update start_tile for the next tileset
    start_tile += height_in_tiles

##############################
# Génération des cosmétiques #
##############################

# Hached tile
default= [[-1,0,sets[0][0]]]

hatched_tile = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
hatched_tile.fill((230, 230, 230))

step = 10 
line_color = (240, 240, 240)

for offset in range(-tile_size, tile_size, step):
    pygame.draw.line(hatched_tile, line_color, (offset, 0), (offset + tile_size, tile_size), 1)



# Buttons
color = (50, 50, 50)
bg_color = (200, 200, 200)
index_color = (30, 30, 120)
index_bg_color = (230, 230, 230)
font = pygame.font.Font(None, tile_size)  # Adjust font size based on tile size
class Button:
    def __init__(self,surface,dest=0,display_dest=False):
        self.surface = surface
        self.dest=dest
        self.display_dest=display_dest

    def def_dest(self,dest):
        self.dest=dest
        if self.display_dest:
            self.surface.fill(bg_color)
            text_surface = font.render(str(dest), True, color)
            text_rect = text_surface.get_rect(center=(tile_size // 2, tile_size // 2))
            self.surface.blit(text_surface, text_rect)

    def lead(self,data):
        print("Lead to ",self.dest)
        data.goto_tileset(self.dest)



buttons = [Button(pygame.Surface((tile_size, tile_size), pygame.SRCALPHA), 0) for _ in range(8)]


# Fill backgrounds
for buts in buttons:
    buts.surface.fill(bg_color)

buttons[0].def_dest(0)
buttons[7].def_dest(-1)

for i in range(min(4,len(sets))):
    b=buttons[i+2]
    b.display_dest=True
    b.def_dest(i+1)
    
# Draw up arrow (▲)
pygame.draw.polygon(buttons[1].surface, color, [
    (tile_size // 2, tile_size // 4),  # Top point
    (tile_size // 4, tile_size * 3 // 4),  # Bottom left
    (tile_size * 3 // 4, tile_size * 3 // 4)  # Bottom right
])

# Draw down arrow (▼)
pygame.draw.polygon(buttons[6].surface, color, [
    (tile_size // 2, tile_size * 3 // 4),  # Bottom point
    (tile_size // 4, tile_size // 4),  # Top left
    (tile_size * 3 // 4, tile_size // 4)  # Top right
])

# First arrow (⏫) - Double Up Arrow with better alignment
pygame.draw.polygon(buttons[0].surface, color, [
    (tile_size // 2, tile_size // 6),  # Top point (higher)
    (tile_size // 4, tile_size // 2),  # Middle left
    (tile_size * 3 // 4, tile_size // 2)  # Middle right
])
pygame.draw.polygon(buttons[0].surface, color, [
    (tile_size // 2, tile_size * 5 // 12),  # Lower point (moved up slightly)
    (tile_size // 4, tile_size * 3 // 4),  # Bottom left
    (tile_size * 3 // 4, tile_size * 3 // 4)  # Bottom right
])

# Last arrow (⏬) - Double Down Arrow with better alignment
pygame.draw.polygon(buttons[7].surface, color, [
    (tile_size // 2, tile_size * 5 // 6),  # Bottom point (lower)
    (tile_size // 4, tile_size // 2),  # Middle left
    (tile_size * 3 // 4, tile_size // 2)  # Middle right
])
pygame.draw.polygon(buttons[7].surface, color, [
    (tile_size // 2, tile_size * 7 // 12),  # Upper point (moved down slightly)
    (tile_size // 4, tile_size // 4),  # Top left
    (tile_size * 3 // 4, tile_size // 4)  # Top right
])


class Coo:
    def __init__(self,x=0,y=0):
        self.x=x
        self.y=y
    
    def redef(self,x,y):
        self.x=x
        self.y=y

    def redef_from_list(self,c):
        self.x=c[0]
        self.y=c[1]

    def redef_from_coo(self,o):
        self.x=o.x
        self.y=o.y
    
    def get(self):
        return [self.x,self.y]

class Data:
    def __init__(self, buttons, x=0, y=0, selected_map_tile=[0,0], selected_tileset_tile=[0,0], selected_tile_layer=0, x_tileset=0):
        self.buttons = buttons
        self.coo = Coo(x,y)
        self.selected_map_tile = selected_map_tile
        self.selected_tile_layer = selected_tile_layer
        self.selected_tileset_tile = selected_tileset_tile
        self.x_tileset = x_tileset
        self.tileset_index = 0
        self.load_map()

    def load_map(self,filename="temp.json"):
        if not os.path.exists(filename):
            print(f"{filename} not found. Creating a new one...")
            with open(filename, "w") as f:
                json.dump([[]], f, indent=4)
        with open(filename,"r") as f:
            self.map=json.loads(f.read())

    def save_map(self,filename="temp.json"):
        with open(filename,"w+") as f:
            f.write(json.dumps(self.map))

    def reduce_map(self):
        shrink=True
        while shrink and len(self.map)>1:
            for j in self.map[0]:
                if j!=default:
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
                    if j!=default:
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
                if j[0]!=default:
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
                    if j[i]!=default:
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
            self.map.insert(0,[default.copy() for _ in range(len(self.map[0]))])
            coo[0]+=1
            self.coo.x+=1
            self.selected_map_tile[0]+=1
        while coo[1]<0:
            for l in self.map:
                l.insert(0,default.copy())
            coo[1]+=1
            self.coo.y+=1
            self.selected_map_tile[1]+=1
        while len(self.map)<=coo[0]:
            self.map.append([default.copy() for _ in range(len(self.map[0]))])
        for l in self.map:
            while len(l)<=coo[1]:
                l.append(default.copy())

    def remove_layer(self,coo=False,layer=-1,all=False):
        if not coo:
            coo=self.selected_map_tile
        if 0<=coo[0]<len(self.map) and 0<=coo[1]<len(self.map[coo[0]]):
            if all or len(self.map[coo[0]][coo[1]])==1:
                self.map[coo[0]][coo[1]]=default.copy()
                self.reduce_map()
            else:
                if len(self.map[coo[0]][coo[1]])>layer:
                    del self.map[coo[0]][coo[1]][layer]
    
    def wich_tile(self):
        for t in sets:
            if self.selected_tileset_tile[0]<t[2]:
                return [self.selected_tileset_tile[0]-t[1],self.selected_tileset_tile[1],t[0]]
        
    def map_set_tile(self,use_layer=False):
        self.map_is_large_enough()
        if use_layer:
            layer=len(self.map[self.selected_map_tile[0]][self.selected_map_tile[1]])
        else:
            layer=self.selected_tile_layer
        if self.map[self.selected_map_tile[0]][self.selected_map_tile[1]][0]==default[0]:
            del self.map[self.selected_map_tile[0]][self.selected_map_tile[1]][0]
        if len(self.map[self.selected_map_tile[0]][self.selected_map_tile[1]])>layer:
            self.map[self.selected_map_tile[0]][self.selected_map_tile[1]][layer]=self.wich_tile()
        else:
            self.map[self.selected_map_tile[0]][self.selected_map_tile[1]].append(self.wich_tile())
        self.reduce_map()

    def update_buttons(self):
        self.tileset_index=self.index_of_tileset()
        self.buttons[1].def_dest(max(0,self.tileset_index-1))
        self.buttons[6].def_dest(min(len(sets)-1,self.tileset_index+1))
        
        if 0==self.tileset_index:
            dests=[2,3,4,5]
        elif 1==self.tileset_index:
            dests=[3,4,5,6]

        elif len(sets)-1==self.tileset_index:
            dests=[self.tileset_index-5,self.tileset_index-4,self.tileset_index-3,self.tileset_index-2]
        elif len(sets)-2==self.tileset_index:
            dests=[self.tileset_index-6,self.tileset_index-5,self.tileset_index-4,self.tileset_index-3]

        else:
            dests=[self.tileset_index-2,self.tileset_index-1,self.tileset_index+1,self.tileset_index+2]
        
        for i in range(min(4,len(sets)-1)):
            self.buttons[i+2].def_dest(dests[i])

    def goto_tileset(self,x):
        self.x_tileset=sets[x][1]
        self.update_buttons()

    def index_of_tileset(self):
        for i,t in enumerate(sets):
            if t[2]>self.x_tileset:
                return i
        return len(sets)-2

    def add_x_tileset(self,x):
        self.x_tileset+=x
        self.update_buttons()
        
    def export_map(self):
        print("Exporting map")
        map_surface = pygame.Surface((len(self.map[0])*tile_size,len(self.map)*tile_size), pygame.SRCALPHA)
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                for k in range(len(self.map[i][j])):
                    map_surface.blit(tilesets[self.map[i][j][k][2]], (j*tile_size, i*tile_size),(self.map[i][j][k][1]*tile_size,self.map[i][j][k][0]*tile_size,tile_size,tile_size))
        pygame.image.save(map_surface, "map.png")
        print("Map exported")

data=Data(buttons)
data.update_buttons()
tileset_index_display=pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)

mouse0_last_pos=(pygame.mouse.get_pos(),data.coo.get(),data.coo.get())
key_released=True
mouse0_released=True
mouse2_released=True
move_coo=Coo()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEWHEEL:  # Detect scrolling
            if pygame.mouse.get_pos()[0]<map_width:
                data.coo.x -= event.y
                data.coo.y += event.x
            else:
                data.add_x_tileset(-event.y)
    
    win.fill((255,255,255))
    keys = pygame.key.get_pressed()
    if all(not key for key in keys):
        key_released=True
    if keys[pygame.K_ESCAPE]:
        run=False
    if keys[pygame.K_LEFT] or keys[move_keys[1]]:
        data.coo.y -= vel
    if keys[pygame.K_RIGHT]  or keys[move_keys[3]]:
        data.coo.y += vel
    if keys[pygame.K_UP] or keys[move_keys[0]]:
        data.coo.x -= vel
    if keys[pygame.K_DOWN] or (keys[move_keys[2]] and not keys[pygame.K_LCTRL]):
        if keys[pygame.K_LCTRL]:
            key_released=False
        data.coo.x += vel
    if keys[pygame.K_PAGEUP] and data.x_tileset>0:
        data.add_x_tileset(-vel)
    if keys[pygame.K_PAGEDOWN]:
        data.add_x_tileset(vel)

    if keys[pygame.K_KP0] or keys[pygame.K_0]:
        data.selected_tile_layer=0
    if keys[pygame.K_KP1] or keys[pygame.K_2]:
        data.selected_tile_layer=1
    if keys[pygame.K_KP2] or keys[pygame.K_3]:
        data.selected_tile_layer=2
    if keys[pygame.K_KP3] or keys[pygame.K_4]:
        data.selected_tile_layer=3
    if key_released and keys[pygame.K_KP4] and data.selected_map_tile[1]>0:
        key_released=False
        data.selected_map_tile[1]-=1
    if key_released and keys[pygame.K_KP5]:
        key_released=False
        data.selected_map_tile[0]+=1
    if key_released and keys[pygame.K_KP6]:
        key_released=False
        data.selected_map_tile[1]+=1
    if key_released and keys[pygame.K_KP8] and data.selected_map_tile[0]>0:
        key_released=False
        data.selected_map_tile[0]-=1

    if key_released and keys[pygame.K_r]:
        key_released=False
        data.reduce_map()
    
    if key_released and keys[pygame.K_LCTRL] and keys[pygame.K_s]:
        key_released=False
        data.save_map("map.json")
        print('Saved')
    
    if key_released and keys[pygame.K_o]:
        key_released=False
        print('Loading')
        data.load_map("map.json")
        print('Loaded')

    if key_released and keys[pygame.K_DELETE]:
        key_released=False
        data.remove_layer(all=True)
        
    if key_released and (keys[pygame.K_KP_MINUS] or keys[pygame.K_MINUS]):
        key_released=False
        data.remove_layer()

    if key_released and keys[pygame.K_e]:
        key_released=False
        data.export_map()
        

    if pygame.mouse.get_pressed()[0]==1:
        if mouse0_released:
            mouse0_released=False
            mouse0_last_pos=(pygame.mouse.get_pos(),move_coo.get(),data.coo.get())

            #Click on the map
            if pygame.mouse.get_pos()[0]<map_width:
                overed_tile_pos=[pygame.mouse.get_pos()[1]//total_size1+data.coo.x,pygame.mouse.get_pos()[0]//total_size1+data.coo.y]
                if keys[pygame.K_LCTRL]:
                    data.remove_layer(overed_tile_pos,all=True)
                else:
                    if data.selected_map_tile!=overed_tile_pos:
                        data.selected_map_tile=overed_tile_pos
                    else:
                        data.map_set_tile()
                #try:print("Selected tile: ",data.map[data.selected_map_tile[0]][data.selected_map_tile[1]])
                #except:print("Selected tile: Out of bounds")

            #Click on a layer
            elif pygame.mouse.get_pos()[1]<total_size1:
                data.selected_tile_layer=pygame.mouse.get_pos()[0]//total_size1-ntiles_map_width-1

            #Click on a button
            elif pygame.mouse.get_pos()[1]<total_size1*2:
                data.buttons[(pygame.mouse.get_pos()[0]//total_size1-ntiles_map_width-1)].lead(data)
            
            #Click on the tileset
            else:
                if pygame.mouse.get_pos()[0]//total_size1-ntiles_map_width-1>=0 and pygame.mouse.get_pos()[1]>2*total_size1:
                    overed_tile_pos=[pygame.mouse.get_pos()[1]//total_size1+data.x_tileset-2,pygame.mouse.get_pos()[0]//total_size1-ntiles_map_width-1]
                    if data.selected_tileset_tile!=overed_tile_pos:
                        data.selected_tileset_tile=overed_tile_pos
                    else:
                        data.map_set_tile(True)
        else:
            move_coo.redef(mouse0_last_pos[1][0]-(pygame.mouse.get_pos()[1]-mouse0_last_pos[0][1])//total_size1,mouse0_last_pos[1][1]-(pygame.mouse.get_pos()[0]-mouse0_last_pos[0][0])//total_size1)

    else:
        if not mouse0_released:
            data.coo.redef(data.coo.x+move_coo.x,data.coo.y+move_coo.y)
            move_coo.redef(0,0)
        mouse0_released=True
    
    if pygame.mouse.get_pressed()[2]==1:
        if mouse2_released:
            mouse2_released=False
            #Click on the map
            if pygame.mouse.get_pos()[0]<map_width:
                coo=[pygame.mouse.get_pos()[1]//total_size1+data.coo.x,pygame.mouse.get_pos()[0]//total_size1+data.coo.y]
                if keys[pygame.K_LCTRL]:
                    data.remove_layer(coo)
                else:
                    data.remove_layer(coo,all=True)
            #Click on a layer
            elif pygame.mouse.get_pos()[1]<total_size1:
                data.remove_layer(layer=pygame.mouse.get_pos()[0]//total_size1-ntiles_map_width-1)
    else:
        mouse2_released=True
    
    temp_x=data.coo.x+move_coo.x
    temp_y=data.coo.y+move_coo.y

    #Highlight selected map tile
    if 0<=data.selected_map_tile[0]-temp_x<ntiles_height and 0<=data.selected_map_tile[1]-temp_y<ntiles_map_width:
        pygame.draw.rect(win,(0,0,0),((data.selected_map_tile[1]-temp_y)*total_size1-1,(data.selected_map_tile[0]-temp_x)*total_size1-1, total_size2, total_size2))
        pygame.draw.rect(win,(255,255,255),((data.selected_map_tile[1]-temp_y)*total_size1,(data.selected_map_tile[0]-temp_x)*total_size1, tile_size, tile_size))
        
    #Highlight selected layer tile
    pygame.draw.rect(win,(0,0,0),((data.selected_tile_layer+ntiles_map_width+1)*total_size1-1,0, total_size2, total_size1))
    pygame.draw.rect(win,(255,255,255),((data.selected_tile_layer+ntiles_map_width+1)*total_size1,0, tile_size, tile_size))
    
    #Highlight selected tileset tile
    if 0<=data.selected_tileset_tile[0]-data.x_tileset<ntiles_height:
        pygame.draw.rect(win,(0,0,0),((data.selected_tileset_tile[1]+ntiles_map_width+1)*total_size1-1,(data.selected_tileset_tile[0]-data.x_tileset+2)*total_size1-1, total_size2, total_size2))
        pygame.draw.rect(win,(255,255,255),((data.selected_tileset_tile[1]+ntiles_map_width+1)*total_size1,(data.selected_tileset_tile[0]-data.x_tileset+2)*total_size1, tile_size, tile_size))

    #Display selected map tile coordinates
    win.blit(bestfont.render(str(data.selected_map_tile), 1, (0,0,0)), (ntiles_map_width*total_size1-3, 8))

    #Display the displayed tileset's index
    tileset_index_display.fill((index_bg_color))
    text_surface = font.render(str(data.tileset_index), True, index_color)
    text_rect = text_surface.get_rect(center=(tile_size // 2, tile_size // 2))
    tileset_index_display.blit(text_surface, text_rect)
    win.blit(tileset_index_display, (ntiles_map_width*total_size1, total_size1))


    #Display map
    for i in range(ntiles_height):
        for j in range(ntiles_map_width):
            if 0<=temp_x+i<len(data.map) and 0<=temp_y+j<len(data.map[temp_x+i]):
                for k in range(0,len(data.map[temp_x+i][temp_y+j])):
                    win.blit(tilesets[data.map[temp_x+i][temp_y+j][k][2]], (j*total_size1, i*total_size1),(data.map[temp_x+i][temp_y+j][k][1]*tile_size,data.map[temp_x+i][temp_y+j][k][0]*tile_size,tile_size,tile_size))
            else:
                win.blit(hatched_tile, (j * total_size1, i * total_size1))
            if i==0:
                win.blit(bestfont.render(str(j+temp_y), 1, (0,0,0)), (j*total_size1+10, 0))
        win.blit(bestfont.render(str(i+temp_x), 1, (0,0,0)), (0, i*total_size1+10))
    
    #Display tileset
    for j in range(2,ntiles_height):
        for t in sets:
            if data.x_tileset+j-2<t[2]:
                ts=[tilesets[t[0]],t[1]]
                break
        for i in range(ntiles_map_width+1,ntiles_map_width+1+ntiles_tileset_width):
            win.blit(ts[0], (i*total_size1, j*total_size1),((i-ntiles_map_width-1)*tile_size,(data.x_tileset+j-2-ts[1])*tile_size,tile_size,tile_size))

    #Display selected tile layers
    if 0<=data.selected_map_tile[0]<len(data.map) and 0<=data.selected_map_tile[1]<len(data.map[data.selected_map_tile[0]]):
        for i in range(len(data.map[data.selected_map_tile[0]][data.selected_map_tile[1]])):
            win.blit(tilesets[data.map[data.selected_map_tile[0]][data.selected_map_tile[1]][i][2]], ((ntiles_map_width+i+1)*total_size1, 0),((data.map[data.selected_map_tile[0]][data.selected_map_tile[1]][i][1])*tile_size,(data.map[data.selected_map_tile[0]][data.selected_map_tile[1]][i][0])*tile_size,tile_size,tile_size))
    
    #Display buttons
    for i in range(8):
        win.blit(data.buttons[i].surface, ((ntiles_map_width+1+i)*total_size1, total_size1),(0,0,tile_size,tile_size))
    
    pygame.display.update()
    data.save_map()
    time.sleep(0.01)
pygame.quit()