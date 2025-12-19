# 3D Model Generation from Photos and Videos

This guide explains how to use the photo-to-3D conversion tools included in this repository.

## Overview

The `photo_to_3d.py` script provides functionality to convert photos and videos into 3D models using depth estimation techniques. This is useful for:

- Creating 3D assets from existing images
- Visualizing scenes in 3D
- Generating models for game development
- Educational purposes in computer vision

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Required Libraries

- **numpy**: Numerical computing
- **Pillow (PIL)**: Image processing
- **trimesh**: 3D mesh processing and export
- **imageio**: Video frame extraction (optional, for video support)
- **imageio-ffmpeg**: FFmpeg plugin for imageio (optional, for video support)

## Usage

### Basic Usage

Convert a photo to a 3D model:

```bash
python photo_to_3d.py <image_path>
```

Example:
```bash
python photo_to_3d.py assets/battlefield.png
```

### Custom Output Name

Specify a custom name for the output file:

```bash
python photo_to_3d.py <image_path> <output_name>
```

Example:
```bash
python photo_to_3d.py assets/battlefield.png battlefield_3d
```

### Video to 3D

Convert a video frame to a 3D model:

```bash
python photo_to_3d.py video/iron_dome.mp4 iron_dome_3d
```

## How It Works

### 1. Depth Map Estimation

The script uses a simple brightness-based depth estimation technique:
- Brighter areas are considered closer
- Darker areas are considered farther away

**Note**: This is a simplified approach for demonstration. Production systems use advanced techniques like:
- Neural networks (e.g., MiDaS, DPT)
- Multi-view stereo
- Structure from Motion (SfM)
- Photogrammetry

### 2. Point Cloud Generation

The depth map is converted into a 3D point cloud:
- Each pixel becomes a 3D point
- X, Y coordinates from pixel position
- Z coordinate from depth value
- Colors preserved from original image

### 3. Mesh Creation

The point cloud is converted to a mesh using convex hull algorithm:
- Creates triangular faces connecting points
- Produces a watertight mesh
- Exports to standard 3D formats

### 4. Export Formats

Supported output formats:
- **OBJ**: Wavefront OBJ (with colors)
- **PLY**: Stanford PLY (point cloud or mesh)
- **STL**: Stereolithography (for 3D printing)

## Python API

You can also use the converters programmatically:

### Photo to 3D

```python
from photo_to_3d import Photo3DConverter

# Initialize converter
converter = Photo3DConverter(output_dir="my_3d_models")

# Convert image to 3D
model_path = converter.image_to_3d(
    image_path="assets/battlefield.png",
    output_name="battlefield_model",
    export_format="obj"
)

print(f"3D model saved to: {model_path}")
```

### Video to 3D

```python
from photo_to_3d import Video3DConverter

# Initialize converter
converter = Video3DConverter(output_dir="my_3d_models")

# Convert video to 3D (uses first frame by default)
model_path = converter.video_to_3d(
    video_path="video/iron_dome.mp4",
    output_name="iron_dome_3d",
    frame_to_use='middle'  # Options: 'first', 'middle', or frame number
)

print(f"3D model saved to: {model_path}")
```

### Advanced Usage: Custom Depth Maps

```python
from photo_to_3d import Photo3DConverter
from PIL import Image
import numpy as np

converter = Photo3DConverter()

# Load image
image = converter.load_image("myimage.png")

# Create custom depth map (e.g., from a neural network)
depth_map = np.random.rand(image.height, image.width)  # Your custom depth

# Convert to point cloud
point_cloud = converter.depth_to_pointcloud(image, depth_map)

# Convert to mesh
mesh = converter.pointcloud_to_mesh(point_cloud)

# Export
mesh.export("output_3d_models/custom_model.obj")
```

## Viewing 3D Models

Once generated, you can view your 3D models using:

### Free Software
- **Blender**: Professional 3D software (https://www.blender.org/)
- **MeshLab**: 3D mesh viewer and editor (https://www.meshlab.net/)
- **3D Viewer**: Built into Windows 10/11

### Online Viewers
- Clara.io (https://clara.io/)
- Sketchfab (https://sketchfab.com/)
- Three.js examples (https://threejs.org/)

## Advanced Techniques

For production-quality 3D reconstruction, consider these state-of-the-art tools:

### 1. MiDaS (Monocular Depth Estimation)
```bash
pip install timm
# Use pretrained MiDaS models for depth estimation
```

### 2. COLMAP (Structure from Motion)
Multi-view 3D reconstruction from photo collections
- Website: https://colmap.github.io/

### 3. Meshroom (Photogrammetry)
Free, open-source photogrammetry software
- Website: https://alicevision.org/

### 4. PyTorch3D
Facebook's 3D deep learning library
```bash
pip install pytorch3d
```

### 5. NeRF (Neural Radiance Fields)
Novel view synthesis and 3D reconstruction
- Instant-NGP: https://github.com/NVlabs/instant-ngp
- Nerfstudio: https://github.com/nerfstudio-project/nerfstudio

## Limitations

The current implementation has the following limitations:

1. **Simple Depth Estimation**: Uses brightness-based heuristic rather than learned models
2. **Single Image**: Doesn't use multiple views for better reconstruction
3. **No Texture Mapping**: Colors are per-vertex rather than UV-mapped textures
4. **Basic Meshing**: Uses convex hull which may not preserve all details

## Improvements

To improve the quality of 3D models:

1. **Use Neural Networks**: Integrate MiDaS or DPT for better depth estimation
2. **Multi-View Reconstruction**: Use multiple photos for more accurate models
3. **Better Meshing**: Implement Poisson surface reconstruction or Ball-Pivoting
4. **Texture Mapping**: Add proper UV mapping for textures
5. **Post-Processing**: Add smoothing, hole filling, and mesh optimization

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### Video conversion fails
Make sure imageio and ffmpeg are installed:
```bash
pip install imageio imageio-ffmpeg
```

### Output model looks incorrect
- Try different images with better contrast
- Adjust the `scale` and `max_depth` parameters
- Use images with clear depth cues (perspective, shadows)

## Contributing

To add new depth estimation methods:

1. Subclass `Photo3DConverter`
2. Override `estimate_depth_simple()` with your method
3. Add new dependencies to `requirements.txt`

Example:
```python
class AdvancedPhoto3DConverter(Photo3DConverter):
    def estimate_depth_simple(self, image):
        # Your advanced depth estimation here
        # e.g., using MiDaS, DPT, or other neural networks
        return depth_map
```

## License

This implementation is provided under the same MIT License as the main project.

## References

- Trimesh documentation: https://trimsh.org/
- Depth estimation papers: https://paperswithcode.com/task/monocular-depth-estimation
- 3D reconstruction overview: https://en.wikipedia.org/wiki/3D_reconstruction
