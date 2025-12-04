#version 330

uniform float shininess = 128;

uniform sampler2D texEarth;
uniform sampler2D texContinents;
uniform sampler2D texLights;
uniform float timer;

in	vec4 eye;
in	vec3 n;
in	vec3 ld;
in vec2 texCoord;

out vec4 colorOut;

float snoise(vec4 v);

float perlin(vec4 p){
	float c = 0;
	float amp = 1.0;
	float freq = 1.0;

	for(int i = 0; i < 5; i++){
		c = c + snoise(freq * p) * amp;
		amp = amp * 0.5;
		freq = freq * 2.0;
	}
	c = c * 0.5 + 0.5;
	return c;
}

const float PI = 3.1415926535897932384626433832795;

void main() {

	vec4 eColor = texture(texEarth, texCoord+vec2(timer*0.00001, 0));
	float eCont = texture(texContinents, texCoord+vec2(timer*0.00001, 0)).r;
	vec4 lColor = texture(texLights, texCoord+vec2(timer*0.00001, 0));
	
	vec2 ce = vec2(texCoord.s * 2 * PI + timer* 0.0001, texCoord.t * PI - PI * 0.5);
	float theta = ce.s;
	float beta = ce.t;
	vec3 cm = vec3(cos(beta) * sin(theta), sin(beta), cos(beta) * cos(theta));

	// float eCloud = perlin(vec4(texCoord * 32 + vec2(timer*0.0001, 0), timer*0.0001, 0));
	float eCloud = perlin(vec4(cm * 4, timer * 0.0001));

	eCloud = smoothstep(0.4, 0.9, eCloud);
	eCloud = pow(eCloud, 0.95);

	// initialize
	// set the specular term to black
	vec4 spec = vec4(0.0);

	// normalize both input vectors
	vec3 nd = normalize(n);
	vec3 e = normalize(vec3(eye));

	float intensity = max(dot(nd,ld), 0.0);
	vec4 color;

	float f = smoothstep(0.0, 0.3, intensity);

	// if the vertex is lit compute the specular color
	if (intensity > 0.0) {
		// compute the half vector
		vec3 h = normalize(ld + e);	
		// compute the specular intensity
		float intSpec = max(dot(h,nd), 0.0);
		// compute the specular term into spec
		spec = vec4(1) * pow(intSpec,shininess);
		eColor = eColor * max(intensity, 0.25) * (1 - eCloud) + spec * eCont * (1 - eCloud) + eCloud;
	}else{
		lColor = (1-eCloud) * lColor;
		color = lColor;
	}
	color = mix(lColor, eColor, f);
	colorOut = color;
}