import os
import math

class ClothGenerator:

    def __init__(self, height=5.0, width=5.0, divisions_h=25, divisions_v=25, vert_stuck=[]):
        self.height = height
        self.width = width
        self.divisions_h = divisions_h
        self.divisions_v = divisions_v
        self.vert_stuck = vert_stuck
        
        # Estruturas de dados
        self.vertices = []
        self.text_coords = []
        self.normals = []
        self.faces_front = []
        self.faces_back = []
        
        # Resultados das adjacências
        self.adj_list = []      # Buffer de 9 vizinhos
        self.adj_2_list = []    # Buffer de 4 vizinhos (bending)

        # Passo da grelha
        self.step_h = self.width / (self.divisions_h - 1) if self.divisions_h > 1 else 0
        self.step_v = self.height / (self.divisions_v - 1) if self.divisions_v > 1 else 0

    def generate_mesh_data(self):
        """ Gera vértices, UVs e faces """
        print(f"1. A gerar malha {self.divisions_h}x{self.divisions_v}...")

        # 1. Vértices e UVs
        for z in range(self.divisions_h):
            for x in range(self.divisions_v):
                # Posição
                px = x * self.step_h
                py = 0.0
                pz = z * self.step_v
                self.vertices.append([px, py, pz])

                # UVs
                u = z / (self.divisions_h - 1) if self.divisions_h > 1 else 0
                v = x / (self.divisions_v - 1) if self.divisions_v > 1 else 0
                self.text_coords.append([u, v])

        self.normals = [[0, 1, 0], [0, -1, 0]]

        # 2. Faces (Triângulos para o OBJ)
        for z in range(self.divisions_h - 1):
            for x in range(self.divisions_v - 1):
                v1 = z * self.divisions_v + x
                v2 = z * self.divisions_v + x + 1
                v3 = (z + 1) * self.divisions_v + x
                v4 = (z + 1) * self.divisions_v + x + 1

                # Frente
                self.faces_front.append([v1, v3, v2])
                self.faces_front.append([v2, v3, v4])
                # Trás
                self.faces_back.append([v1, v2, v3])
                self.faces_back.append([v2, v4, v3])

    def calculate_adjacencies(self):
        """ Calcula as distâncias de repouso para as molas """
        print("2. A calcular adjacências...")
        
        dist_h = self.step_h
        dist_v = self.step_v
        hipotenuse = math.sqrt(dist_h**2 + dist_v**2)

        for j in range(self.divisions_v):     # j = Z (linhas)
            for i in range(self.divisions_h): # i = X (colunas)
                
                indices_9 = [] # Structural + Shear
                indices_4 = [] # Bending

                # --- Lógica Bending (4 vizinhos - Salto de 2) ---
                # Vizinho Esquerda (-2)
                if i - 2 >= 0:
                    indices_4.append(2 * dist_h)
                else:
                    indices_4.append(-1)

                # Vizinho Direita (+2)
                if i + 2 < self.divisions_h:
                    indices_4.append(2 * dist_h)
                else:
                    indices_4.append(-1)

                # Vizinho Cima (-2)
                if j - 2 >= 0:
                    indices_4.append(2 * dist_v)
                else:
                    indices_4.append(-1)

                # Vizinho Baixo (+2)
                if j + 2 < self.divisions_v:
                    indices_4.append(2 * dist_v)
                else:
                    indices_4.append(-1)

                # --- Lógica Structural/Shear (9 vizinhos - Janela 3x3) ---
                # Linha de Cima (j-1)
                for x in range(-1, 2):
                    if i + x >= 0 and i + x < self.divisions_h and j - 1 >= 0:
                        dist = hipotenuse if x != 0 else dist_v
                        indices_9.append(dist)
                    else:
                        indices_9.append(-1)

                # Linha do Meio (j)
                for x in range(-1, 2):
                    if i + x >= 0 and i + x < self.divisions_h:
                        if x != 0:
                            indices_9.append(dist_h)
                        else:
                             # O próprio vértice (distância 0 ou placeholder)
                            indices_9.append(0.0) 
                    else:
                        indices_9.append(-1)

                # Linha de Baixo (j+1)
                for x in range(-1, 2):
                    if i + x >= 0 and i + x < self.divisions_h and j + 1 < self.divisions_v:
                        dist = hipotenuse if x != 0 else dist_v
                        indices_9.append(dist)
                    else:
                        indices_9.append(-1)

                self.adj_list.append(indices_9)
                self.adj_2_list.append(indices_4)

    def write_files(self, obj_path='../objects/cloth.obj'):
        """ Escreve os ficheiros OBJ e buffers TXT """
        print(f"3. A escrever ficheiros em {os.path.dirname(obj_path)} e ../buffers/ ...")

        # Criar pastas se não existirem
        os.makedirs(os.path.dirname(obj_path), exist_ok=True)
        os.makedirs('../buffers', exist_ok=True)

        # --- OBJ FILE ---
        with open(obj_path, 'w') as f:
            for index, v in enumerate(self.vertices):
                f.write(f"v {v[0]:.4f} {index} {v[2]:.4f}\n")
            
            for tex in self.text_coords:
                f.write(f"vt {tex[0]:.4f} {tex[1]:.4f}\n")
            
            for norm in self.normals:
                f.write(f"vn {norm[0]} {norm[1]} {norm[2]}\n")
            
            for face in self.faces_front:
                f.write(f"f {face[0]+1}/{face[0]+1}/1 {face[1]+1}/{face[1]+1}/1 {face[2]+1}/{face[2]+1}/1\n")
            
            for face in self.faces_back:
                f.write(f"f {face[0]+1}/{face[0]+1}/2 {face[1]+1}/{face[1]+1}/2 {face[2]+1}/{face[2]+1}/2\n")

        # --- BUFFERS TXT ---
        
        # 1. Posições (x y z w)
        with open('../buffers/cloth_buffer_info.txt', 'w') as f:
            for v in self.vertices:
                # w=1.0 (massa inversa padrão)
                f.write(f"{v[0]:.4f} {v[1]:.4f} {v[2]:.4f} 1.0\n")

        # 2. Adjacências (Distâncias apenas)
        with open('../buffers/cloth_adj_info.txt', 'w') as f:
            for neighbors in self.adj_list:
                for dist in neighbors:
                    f.write(f"{dist:.4f}\n")

        with open('../buffers/cloth_adj_2_info.txt', 'w') as f:
            for neighbors in self.adj_2_list:
                for dist in neighbors:
                    f.write(f"{dist:.4f}\n")

        # 3. Normais
        with open('../buffers/cloth_normals_info.txt', 'w') as f:
            for _ in self.vertices:
                f.write("0.0 1.0 0.0 0.0\n")

        # 4. Texturas
        with open('../buffers/cloth_texture_coords_info.txt', 'w') as f:
            for tex in self.text_coords:
                f.write(f"{tex[0]:.4f} {tex[1]:.4f}\n")

        # 5. Forças e Velocidades (Zero)
        with open('../buffers/cloth_forces_buffer.txt', 'w') as f:
            for _ in self.vertices:
                f.write("0.0 0.0 0.0 0.0\n")
        
        with open('../buffers/cloth_velocities_buffer.txt', 'w') as f:
            for _ in self.vertices:
                f.write("0.0 0.0 0.0 0.0\n")
        
        # 6. Vértices Presos
        with open('../buffers/cloth_stuck_vert.txt', 'w') as f:
            f.write(f"{len(self.vert_stuck)}\n")
            for ind in self.vert_stuck:
                f.write(f"{ind}\n")

    def run(self, output_path='../objects/cloth.obj'):
        self.generate_mesh_data()
        self.calculate_adjacencies()
        self.write_files(output_path)
        print("Concluído.")

if __name__ == "__main__":
    divisions_h = 25
    divisions_v = 25
    height = 10.0
    width = 10.0
    
    stuck_verts = [0, divisions_h - 1]
    
    generator = ClothGenerator(height, width, divisions_h, divisions_v, stuck_verts)
    generator.run()