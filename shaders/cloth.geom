#version 430
// #pragma optionNV unroll all

layout(triangles) in;
layout (triangle_strip, max_vertices=6) out;

uniform mat4 m_pvm;
uniform mat3 m_normal;

layout(std430, binding = 1) buffer clothBuffer {
	vec4 pos[]; // 1D array of positions
};

layout(std430, binding = 4) buffer normalsBuffer {
	vec4 normals[]; // 1D array of normals
};

layout(std430, binding = 5) buffer textureBuffer {
	vec2 texture_coords[]; // 1D array of texture coordinates
};

out vec3 n;
out vec2 text_c;

in int v_index[3];

void main() {

	// Calcula a normal da face a partir das arestas
	vec3 edge1 = pos[v_index[1]].xyz - pos[v_index[0]].xyz;
	vec3 edge2 = pos[v_index[2]].xyz - pos[v_index[0]].xyz;
	vec3 faceNormal = normalize(cross(edge1, edge2));

	// Usamos as normais já calculadas no buffer (do compute shader anterior)
	// ou usa a normal da face	
	vec3 n0 = normalize(normals[v_index[0]].xyz);
	vec3 n1 = normalize(normals[v_index[1]].xyz);
	vec3 n2 = normalize(normals[v_index[2]].xyz);
	
	// Se a normal do buffer estiver a zeros, usamos a normal da face
	if (length(normals[v_index[0]].xyz) < 0.001) n0 = faceNormal;
	if (length(normals[v_index[1]].xyz) < 0.001) n1 = faceNormal;
	if (length(normals[v_index[2]].xyz) < 0.001) n2 = faceNormal;

	// Face frontal
	n = n0;
	text_c = texture_coords[v_index[0]];
	gl_Position = m_pvm * pos[v_index[0]];
	EmitVertex();

	n = n1;
	text_c = texture_coords[v_index[1]];
	gl_Position = m_pvm * pos[v_index[1]];
	EmitVertex();

	n = n2;
	text_c = texture_coords[v_index[2]];
	gl_Position = m_pvm * pos[v_index[2]];
	EmitVertex();
	EndPrimitive();

	// Face traseira (normais invertidas)
	n = -n0;
	text_c = texture_coords[v_index[0]];
	gl_Position = m_pvm * pos[v_index[0]];
	EmitVertex();

	n = -n2;
	text_c = texture_coords[v_index[2]];
	gl_Position = m_pvm * pos[v_index[2]];
	EmitVertex();

	n = -n1;
	text_c = texture_coords[v_index[1]];
	gl_Position = m_pvm * pos[v_index[1]];
	EmitVertex();
	EndPrimitive();
}