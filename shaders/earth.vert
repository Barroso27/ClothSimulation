#version 330

uniform	mat4 m_pvm;
uniform	mat4 m_viewModel;
uniform	mat4 m_view;
uniform	mat3 m_normal;
uniform float timer;

uniform	vec4 l_dir;	   // global space

in vec4 position;	// local space
in vec3 normal;		// local space
in vec2 texCoord0;	

// the data to be sent to the fragment shader

out vec4 eye;
out vec3 n;
out vec3 ld;
out vec2 texCoord;

void main () {
	texCoord = texCoord0;
	n = normalize(m_normal * normal);
	
	// A esfera visual precisa coincidir com a esfera de colisão do cloth.comp
	// Como a translação XML já posiciona a esfera em (5, -5, 5),
	// e o cloth.comp calcula: animated_z = sphere_z + sin(timer * speed) * amplitude
	// onde sphere_z = 5.0, o offset que precisamos adicionar é apenas sin(timer * speed) * amplitude
	
	// Parâmetros da animação (devem coincidir com cloth.comp)
	const float oscillation_speed = 0.0003;
	const float oscillation_amplitude = 10.0; // Amplitude: vai de -10 a +10
	
	// Calcula o offset da animação (movimento perpendicular ao pano - eixo Z)
	float offset_z = sin(timer * oscillation_speed) * oscillation_amplitude;
	
	// Aplica o offset à posição local (antes da transformação m_pvm que inclui a translação)
	vec4 animated_position = position;
	animated_position.z += offset_z;
	
	eye = -(m_viewModel * animated_position);
	ld = normalize(vec3(m_view * -l_dir));

	gl_Position = m_pvm * animated_position;	
}