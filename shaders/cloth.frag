#version 430

//uniform
// uniform vec4 diffuse;
uniform vec4 l_dir; // world space
uniform mat4 m_view;
uniform sampler2D tex;
uniform vec4 diffuse;
uniform mat3 m_normal;

// // input
in vec3 n;
in vec2 text_c;

// output
out vec4 color;

void main() {

	// compute light direction in camera space
	vec3 l = normalize(vec3(m_view * -l_dir));
	vec3 nn = normalize(m_normal * normalize(n));
	float i = max(0.0, dot(l,nn));

	color = max(0.25, i) * diffuse * texture(tex, text_c);
}