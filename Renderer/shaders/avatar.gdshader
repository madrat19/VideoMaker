shader_type canvas_item;
render_mode blend_mix;

uniform float radius = 4.0;

uniform sampler2D mask;

void fragment() {
    vec4 color = texture(TEXTURE,UV);
    vec2 pixel_size = TEXTURE_PIXEL_SIZE;
    vec4 shader = texture(mask, UV).rgba;
    COLOR.rgb = color.rgb;
    shader += texture(mask, UV + vec2(0.0, -radius) * pixel_size);
    shader += texture(mask, UV + vec2(0.0, -radius/2.0) * pixel_size);
    shader += texture(mask, UV + vec2(0.0, radius) * pixel_size);
    shader += texture(mask, UV + vec2(0.0, radius/2.0) * pixel_size);
    shader += texture(mask, UV + vec2(-radius, 0.0) * pixel_size);
    shader += texture(mask, UV + vec2(-radius/2.0, 0.0) * pixel_size);
    shader += texture(mask, UV + vec2(radius, 0.0) * pixel_size);
    shader += texture(mask, UV + vec2(radius/2.0, 0.0) * pixel_size);
    shader /= 5.0;
    color.a = shader.a;

    COLOR = color;
}