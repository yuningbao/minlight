// simple demo vertex shader
// attribute variables
// www.lighthouse3d.com

//uniform vec4 light_source_position;
varying vec4 out_Color;
varying vec4 position;

void main()
{
	vec4 p;
	p.xyz = gl_Vertex.xyz;
  p.w = 1.0;

  position = p;

  out_Color = gl_Color;
  gl_Position = gl_ModelViewProjectionMatrix*gl_Vertex;
	gl_ModelViewProjectionMatrix * p;
}
