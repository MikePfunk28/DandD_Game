const canvas = document.createElement('canvas');
document.body.appendChild(canvas);
const gl = canvas.getContext('webgl');

// Shader sources
const vertexShaderSource = `
    attribute vec4 position;
    uniform mat4 matrix;
    void main() {
        gl_Position = matrix * position;
    }
`;
const fragmentShaderSource = `
    void main() {
        gl_FragColor = vec4(0.0, 1.0, 0.0, 1.0);
    }
`;

// Shader compilation omitted for brevity
// Setup buffers, compile shaders, set up uniform matrix, etc.

// Animation loop
function animate() {
    // Update matrix for rotation
    // Render using WebGL API
    requestAnimationFrame(animate);
}
animate();
