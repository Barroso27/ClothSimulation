#version 460
uniform mat4  m_pvm;
uniform vec3 cam_pos; // Global space
uniform mat4 m_m;

in vec4 position; // Local space
in vec4 normal;

out vec3 n, incident;

void main(){

    n = normalize(vec3(inverse(transpose(m_m)) * normal));

    vec3 pos = vec3(m_m * position);
    incident = pos - cam_pos;

    gl_Position = m_pvm * position;
}