#version 330

// red shader

uniform sampler2D source;
in vec2 outTexCoords;
in vec3 customColor;

float intensityFactor = 2.;

void main()
{
    vec3 color = vec3(texture(source, outTexCoords).rgb);

    gl_FragColor = vec4(color * vec3(1.0f, 0.f, 0.f), 1.f);
}