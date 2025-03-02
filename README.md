# TileMap Maker  

**TileMap Maker** is a simple tool for creating maps from tilesets and exporting them as PNG images. It allows you to design maps with multiple layers and easily manage tiles.  

## Features  
✅ Create maps from tilesets
✅ Support for multiple layers
✅ Export maps as PNG


## UI Layout  
- **Map** → On the left side of the screen, with coordinates displayed on top and left  
- **Layers** → Top right corner  
- **Tileset** → Below the layers section 

## Controls  

### General  
- **Esc** → Quit the application  
- **Ctrl + S** → Save map to `map.json`  
- **O** → Load `map.json`  
- **E** → Export map to `map.png`  

### Navigation  
- **ZQSD** or **drag and drop** → Move the map  
- **Mouse scroll on the map** → Move up/down  
- **Mouse scroll on the tileset** → Move up/down (or **Page Up/Down**)  
- **Ctrl + Mouse scroll** → Zoom in/out

### Layer Selection  
- **Left click or Keys 0, 1, 2, 3** (keyboard or keypad) → Select a layer  

### Tile Placement & Editing  
- **Left click or Keypad 8, 4, 5, 6** → Move the selected tile on the map (up, left, down, right)  
- **Delete** → Remove all layers of the selected tile  
- **Minus (-)** → Remove the top layer of the selected tile  

### Mouse Actions  
- **Left click on an unselected tile** → Select it  
- **Left click on a selected tile** → Place the selected tileset tile on the map  
- **Left click on a layer** → Select it  
- **Right click on a tile** →  Remove the top layer
- **Ctrl + Right click on a tile** → Delete it
- **Right click on a layer** → Delete it   

### Debbug
- **Space** → Reload to adapt to new window size

## Installation & Usage  
Clone the repository and run the tool:  
```sh
git clone https://github.com/arlexTech/TileMap_Maker.git
cd TileMap_Maker
python tilemap_maker.py
```
