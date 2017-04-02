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
  
  if (y < height/2) {
    if (x < width/2) {
      gl_FragColor = vec4( 0.8, 1, 0, 1 );
    } else {
      gl_FragColor = vec4( 0.8, 1, 1, 1 );
    }
  } else {
    if (x < width/2) {
      gl_FragColor = vec4( 1, .8, 1, 1 );
    } else {
      gl_FragColor = vec4( 0.8, .8, 1, 1 );
    }
  }
}
