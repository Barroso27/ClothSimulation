#version 430

layout(std430, binding = 1) buffer clothBuffer {
    vec4 pos[]; // 1D array of positions
};

layout(std430, binding = 4) buffer normalsBuffer {
    vec4 normals[]; // 1D array of normals
};

in vec4 position;

out vec3 normal;
out int v_index;

void main() {

	int index = int(position.y);
	normal = normals[index].xyz;
	// normals[index] = vec4(0.0);
	v_index = index;
	gl_Position = pos[index];
}