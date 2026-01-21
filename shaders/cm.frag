#version 460

uniform samplerCube tex_cm;
uniform float eta = 0.9 ;

in vec3 n, incident;

out vec4 color;

void main() {

    vec3 ii = normalize(incident); 
    vec3 nn = normalize(n);

    vec3 r = reflect(ii, nn);

    vec3 trefrRed = refract(ii, nn, eta);
    vec3 trefrGreen = refract(ii, nn, eta + 0.01);
    vec3 trefrBlue = refract(ii, nn, eta + 0.02);

    vec3 refl = texture(tex_cm, r).rgb;
    vec3 refr;
    
    refr.r = texture(tex_cm, trefrRed).r;
    refr.g = texture(tex_cm, trefrGreen).g;
    refr.b = texture(tex_cm, trefrBlue).b;

    float R = 1.0 - eta * eta * (1.0 - dot(nn, -ii) * dot(nn, -ii));

    color = vec4(mix(refl, refr, R), 1); 
}
