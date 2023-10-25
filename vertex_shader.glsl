#version 330

in layout(location = 0) vec3 position;

in layout(location = 1) vec3 color;
out vec3 customColor;

//in layout(location = 1) vec3 inColor;
//out vec3 outColor;

in layout(location = 2) vec2 inTexCoords;
out vec2 outTexCoords;

void main()
{
    gl_Position = vec4(position, 1.0f);

    //outColor = inColor;

    outTexCoords = inTexCoords;
    customColor = color;
}