from ursina import *
import pandas as pd
import json
import numpy as np

# ====================== CONFIGURAÇÃO SPHY-LORENZ ======================
print("Carregando integrador geométrico (Parquet)...")
df = pd.read_parquet("sphy_dataset.parquet")

app = Ursina(title="SPHY - Lorenz Chaos Integrator", borderless=False)
window.color = color.black
EditorCamera()

# Parâmetros de Lorenz
sigma, rho, beta = 10.0, 28.0, 8.0 / 3.0
lorenz_pos = Vec3(0.1, 0.1, 0.1)
points = [] 
max_points = 800 # Rastro um pouco mais longo para ver a convergência

# Malha SPHY (O Campo Guia)
mesh_model = Mesh(mode="line", thickness=1)
grid_entity = Entity(model=mesh_model, color=color.rgba(0, 255, 255, 40), unlit=True)

# A Borboleta e o Rastro
butterfly = Entity(model='sphere', scale=0.15, color=color.yellow)
# Inicializamos com dois pontos iguais para evitar o erro de Primitive do Panda3D
trail_renderer = Entity(model=Mesh(vertices=[lorenz_pos, lorenz_pos], mode='line', thickness=2), color=color.yellow)

state = {"frame": 0}

def update():
    global lorenz_pos
    dt = time.dt * 0.8
    
    # 1. ACESSAR O CAMPO GEOMÉTRICO AUDITADO
    row = df.iloc[state["frame"]]
    vertices_raw = json.loads(row['vertices'])
    g_mod = float(row['g_flex']) 
    
    # 2. INTEGRAÇÃO LORENZ MODULADA PELA SPHY
    # A gravidade (g_mod) atua como a viscosidade do espaço-tempo no caos
    dx = (sigma * (lorenz_pos.y - lorenz_pos.x)) * dt
    dy = (lorenz_pos.x * (rho - lorenz_pos.z) - lorenz_pos.y) * dt
    dz = (lorenz_pos.x * lorenz_pos.y - beta * lorenz_pos.z) * dt
    
    # A trajetória é ancorada no valor real do dataset
    lorenz_pos += Vec3(dx, dy, dz) * g_mod 
    butterfly.position = lorenz_pos * 0.3 # Ajuste de escala visual
    
    # 3. ATUALIZAR RASTRO (Segurança de Primitiva)
    points.append(Vec3(butterfly.position))
    if len(points) > max_points: 
        points.pop(0)
    
    if len(points) > 1:
        trail_renderer.model.vertices = points
        trail_renderer.model.generate()
    
    # 4. ATUALIZAR CAMPO SPHY
    mesh_model.vertices = [Vec3(*v) for v in vertices_raw]
    mesh_model.generate()
    
    # Ciclo de frames do Parquet
    state["frame"] = (state["frame"] + 1) % len(df)

app.run()
