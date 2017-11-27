uniform vec4 light_position;
uniform vec4 light_direction;
uniform float light_radius;

varying vec4 out_Color;
varying vec4 position;
varying vec4 out_Normal;

void main()
{
	vec4 pq = light_position - position;

	if( dot(light_direction,out_Normal) < 0.0  && length(cross(pq.xyz,light_direction.xyz)) / length(light_direction.xyz) < light_radius)
	{
		gl_FragColor = out_Color*1.2;
	}
	else
	{
		gl_FragColor = out_Color;
	}

	//gl_FragColor = out_Normal;
}
