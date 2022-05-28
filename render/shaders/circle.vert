#version 330 core

layout (location = 0) in vec2 aPos;

out vec3 FragPos;

uniform vec2 translate;
uniform mat2 rotate;
uniform mat4 view;

void main()
{
    gl_Position = view * vec4(translate + rotate * aPos, 0.0, 1.0);
}