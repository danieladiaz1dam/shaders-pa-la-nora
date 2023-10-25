#version 330

// red shader

uniform sampler2D source;
in vec2 outTexCoords;
in vec3 outColor;

float intensityFactor = 2.;

void main()
{
    vec3 color = vec3(texture(source, outTexCoords).rgb);

    gl_FragColor = vec4(color * outColor, 1.f);
}