#version 330

const float PI = 3.14159265359;

uniform sampler2D texAlbedo;
uniform sampler2D texAo;
uniform sampler2D texHeight;
uniform sampler2D texMetalic;
uniform sampler2D texNormal;
uniform sampler2D texRoughness;

uniform vec4 l_dir;

in vec3 fragPos;
in vec2 texCoord;
in mat3 TBN;

out vec4 colorOut;

// Fresnel-Schlick approximation
vec3 fresnelSchlick(float cosTheta, vec3 F0) {
    return F0 + (1.0 - F0) * pow(1.0 - cosTheta, 5.0);
}

// GGX/Trowbridge-Reitz normal distribution
float distributionGGX(vec3 N, vec3 H, float roughness) {
    float a = roughness * roughness;
    float a2 = a * a;
    float NdotH = max(dot(N, H), 0.0);
    float NdotH2 = NdotH * NdotH;
    
    float nom = a2;
    float denom = (NdotH2 * (a2 - 1.0) + 1.0);
    denom = PI * denom * denom;
    
    return nom / denom;
}

// Schlick-GGX geometry function
float geometrySchlickGGX(float NdotV, float roughness) {
    float r = (roughness + 1.0);
    float k = (r * r) / 8.0;
    
    float nom = NdotV;
    float denom = NdotV * (1.0 - k) + k;
    
    return nom / denom;
}

// Smith's method for geometry obstruction
float geometrySmith(vec3 N, vec3 V, vec3 L, float roughness) {
    float NdotV = max(dot(N, V), 0.0);
    float NdotL = max(dot(N, L), 0.0);
    float ggx2 = geometrySchlickGGX(NdotV, roughness);
    float ggx1 = geometrySchlickGGX(NdotL, roughness);
    
    return ggx1 * ggx2;
}

void main() {
    // Sample textures
    vec3 albedo = texture(texAlbedo, texCoord).rgb;
    float ao = texture(texAo, texCoord).r;
    float metallic = texture(texMetalic, texCoord).r;
    float roughness = texture(texRoughness, texCoord).r;
    
    // Normal mapping
    vec3 normalMap = texture(texNormal, texCoord).rgb;
    normalMap = normalMap * 2.0 - 1.0; // Convert from [0,1] to [-1,1]
    vec3 N = normalize(TBN * normalMap);
    
    // Calculate lighting vectors
    vec3 V = normalize(-fragPos); // View direction
    vec3 L = normalize(-l_dir.xyz); // Light direction
    vec3 H = normalize(V + L); // Half vector
    
    // Calculate reflectance at normal incidence
    vec3 F0 = vec3(0.04);
    F0 = mix(F0, albedo, metallic);
    
    // Cook-Torrance BRDF
    float NDF = distributionGGX(N, H, roughness);
    float G = geometrySmith(N, V, L, roughness);
    vec3 F = fresnelSchlick(max(dot(H, V), 0.0), F0);
    
    vec3 numerator = NDF * G * F;
    float denominator = 4.0 * max(dot(N, V), 0.0) * max(dot(N, L), 0.0) + 0.0001;
    vec3 specular = numerator / denominator;
    
    // Energy conservation
    vec3 kS = F;
    vec3 kD = vec3(1.0) - kS;
    kD *= 1.0 - metallic;
    
    // Calculate radiance
    float NdotL = max(dot(N, L), 0.0);
    vec3 radiance = vec3(1.0); // Light color/intensity
    
    // Final lighting calculation
    vec3 Lo = (kD * albedo / PI + specular) * radiance * NdotL;
    
    // Ambient lighting
    vec3 ambient = vec3(0.03) * albedo * ao;
    vec3 color = ambient + Lo;
    
    // Tone mapping (simple Reinhard)
    color = color / (color + vec3(1.0));
    
    // Gamma correction
    color = pow(color, vec3(1.0/2.2));
    
    colorOut = vec4(color, 1.0);
}