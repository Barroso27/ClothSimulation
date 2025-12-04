# Script para gerar uma grelha (grid.obj) para Simulação de Tecidos
# Gera posições (v), texturas (vt) e normais (vn)

filename = "grid.obj"
resolution = 60  # 60x60 quadrados (podes aumentar para mais detalhe, ex: 100)
size = 4.0       # Tamanho total da grelha no mundo

def generate_grid():
    print(f"A gerar {filename} com resolução {resolution}x{resolution}...")
    
    with open(filename, 'w') as f:
        f.write("# Grid gerada para Cloth Simulation\n")
        f.write(f"# Resolution: {resolution}x{resolution}\n")
        f.write("o ClothGrid\n")
        
        # DEFINIR O NOME DO MATERIAL (Isto ajuda no XML)
        f.write("mtllib materials.mlib\n")
        f.write("usemtl ClothMat\n\n") 

        # 1. VERTICES (v) - Centrado no (0,0,0) no plano XZ
        # Começa em -size/2 e vai até +size/2
        step = size / resolution
        start = -size / 2.0
        
        for z in range(resolution + 1):
            for x in range(resolution + 1):
                px = start + (x * step)
                pz = start + (z * step)
                # Plano XZ (y=0)
                f.write(f"v {px:.4f} 0.0000 {pz:.4f}\n")

        # 2. TEXTURE COORDS (vt) - De 0 a 1
        uv_step = 1.0 / resolution
        for z in range(resolution + 1):
            for x in range(resolution + 1):
                u = x * uv_step
                v = 1.0 - (z * uv_step) # Inverter V se a textura aparecer de cabeça para baixo
                f.write(f"vt {u:.4f} {v:.4f}\n")

        # 3. NORMALS (vn) - A apontar para cima (Y positivo)
        f.write("\nvn 0.0000 1.0000 0.0000\n\n")

        # 4. FACES (f)
        # Formato: f v/vt/vn v/vt/vn v/vt/vn
        for z in range(resolution):
            for x in range(resolution):
                # Indices no OBJ começam em 1
                # Calcular indices dos 4 cantos do quadrado (quad)
                top_left = (z * (resolution + 1)) + x + 1
                top_right = top_left + 1
                bottom_left = ((z + 1) * (resolution + 1)) + x + 1
                bottom_right = bottom_left + 1
                
                # Triângulo 1
                f.write(f"f {top_left}/{top_left}/1 {bottom_left}/{bottom_left}/1 {top_right}/{top_right}/1\n")
                # Triângulo 2
                f.write(f"f {top_right}/{top_right}/1 {bottom_left}/{bottom_left}/1 {bottom_right}/{bottom_right}/1\n")

    print("Concluído! O ficheiro 'grid.obj' foi criado.")

if __name__ == "__main__":
    generate_grid()