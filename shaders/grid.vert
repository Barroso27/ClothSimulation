#version 330

uniform mat4 m_pvm;
uniform mat4 m_viewModel;
uniform mat3 m_normal;

in vec4 position;
in vec3 normal;
in vec4 tangent;
in vec2 texCoord0;

out vec3 fragPos;
out vec2 texCoord;
out mat3 TBN;

void main() {
    texCoord = texCoord0;
    
    // Transform position to view space
    vec4 viewPos = m_viewModel * position;
    fragPos = viewPos.xyz;
    
    // Calculate TBN matrix for normal mapping
    vec3 T = normalize(m_normal * tangent.xyz);
    vec3 N = normalize(m_normal * normal);
    // Re-orthogonalize T with respect to N
    T = normalize(T - dot(T, N) * N);
    // Calculate bitangent
    vec3 B = cross(N, T) * tangent.w;
    
    TBN = mat3(T, B, N);
    
    gl_Position = m_pvm * position;
}