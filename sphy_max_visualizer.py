from ursina import *
from math import degrees
import pandas as pd
import json
import hashlib

# ====================== DATASET LOADING ======================
print("Loading Parquet dataset...")
df = pd.read_parquet("sphy_dataset.parquet")
print(f"S(Φ):OK {len(df)} frames loaded.")

# ====================== URSINA ENGINE ======================
app = Ursina(title="SPHY - SHA256 Validation Viewer", borderless=False)
window.color = color.black

# Enable interactive mouse controls (zoom, rotate, pan)
EditorCamera()

state = {"current_frame": 0}

# Pivot for geometric orientation
pivot = Entity()
pivot.rotation_x = 68

mesh_model = Mesh(mode="line", thickness=1.4)
Entity(parent=pivot, model=mesh_model, unlit=True)

# UI Elements
ui_title = Text("SPHY - REAL-TIME VALIDATOR", position=(-0.85, 0.45), scale=1.3, color=color.yellow)
ui_frame = Text("", position=(-0.85, 0.38), scale=1.1, color=color.white)
ui_status = Text("", position=(-0.85, 0.32), scale=1.0, color=color.green)

def load_frame(frame_idx):
    row = df.iloc[frame_idx]
    
    vertices = json.loads(row['vertices'])
    colors_raw = json.loads(row['colors'])
    
    # SHA256 Integrity Validation
    frame_data = {
        "frame": int(row['frame']),
        "t": float(row['t']),
        "g_flex": float(row['g_flex']),
        "vertices": vertices,
        "colors": colors_raw
    }
    # Re-generating hash to audit data immutability
    frame_json = json.dumps(frame_data, sort_keys=True).encode('utf-8')
    calculated_sha = hashlib.sha256(frame_json).hexdigest()
    
    # Verification check
    is_valid = calculated_sha == row['sha256']
    
    # Update Mesh Data
    mesh_model.vertices = [Vec3(*v) for v in vertices]
    mesh_model.colors = [color.rgba(0, int(100 + c[0]*155), int(200 + c[0]*55), 180) for c in colors_raw]
    mesh_model.generate()
    
    # Update HUD
    ui_frame.text = f"Frame: {frame_idx}/{len(df)-1} | t = {row['t']:.3f} | g = {row['g_flex']:.3f}"
    ui_status.text = "S(Φ):OK SHA256 Valid" if is_valid else "S(Φ):Error INVALID SHA256!"
    ui_status.color = color.green if is_valid else color.red

def update():
    # Automatic Frame Progression
    state["current_frame"] = (state["current_frame"] + 1) % len(df)
    load_frame(state["current_frame"])

# Initial Load
load_frame(0)

app.run()
