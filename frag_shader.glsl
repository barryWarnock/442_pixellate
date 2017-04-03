#version 120
//the d will be replaced at runtime
uniform vec3[%d] averages;//multidimentional arrays are not supported by the version of the GLSL I'm using
uniform int width;
uniform int height;
uniform int columns;
uniform int rows;

void main() {
  float x = gl_FragCoord.x;
  float y = gl_FragCoord.y;
  float chunkWidth  = width/columns;
  float chunkHeight = height/rows;
  int chunkX = int(x/chunkWidth);
  int chunkY = int(y/chunkHeight);
  vec3 colour = averages[(chunkX*rows )+chunkY];
  gl_FragColor = vec4(colour[0]/255.0, colour[1]/255.0, colour[2]/255.0, 1.0);
}
