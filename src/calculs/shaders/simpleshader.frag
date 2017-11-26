uniform vec4 light_position;
uniform vec4 light_direction;
uniform float light_radius;

varying vec4 out_Color;
varying vec4 position;

void main()
{
	vec4 pq = light_position - position;

	if(length(cross(pq.xyz,light_direction.xyz)) / length(light_direction.xyz) < light_radius)
	{
		gl_FragColor = out_Color*1.2;
	}
	else
	{
		gl_FragColor = out_Color;
	}
}
