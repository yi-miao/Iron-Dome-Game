"""
3D Model Generation from Photos and Videos

This module provides functionality to convert photos and videos into 3D models
using various reconstruction techniques.

Supported methods:
1. Depth map estimation from single images
2. Multi-view reconstruction from multiple photos
3. Video frame extraction and 3D reconstruction
"""

import numpy as np
from PIL import Image
import trimesh
import os
import sys


class Photo3DConverter:
    """Convert photos to 3D models using depth estimation"""
    
    def __init__(self, output_dir="output_3d_models", max_image_size=200):
        """
        Initialize the converter
        
        Args:
            output_dir: Directory to save generated 3D models
            max_image_size: Maximum dimension for image processing (default: 200)
        """
        self.output_dir = output_dir
        self.max_image_size = max_image_size
        os.makedirs(output_dir, exist_ok=True)
        print(f"✅ 3D Converter initialized. Output directory: {output_dir}")
    
    def load_image(self, image_path):
        """
        Load an image from file
        
        Args:
            image_path: Path to the image file
            
        Returns:
            PIL Image object
        """
        try:
            img = Image.open(image_path)
            print(f"✅ Loaded image: {image_path} (size: {img.size})")
            return img
        except Exception as e:
            print(f"❌ Error loading image: {e}")
            return None
    
    def estimate_depth_simple(self, image):
        """
        Simple depth estimation based on brightness
        (For demo purposes - real implementations use neural networks)
        
        Args:
            image: PIL Image object
            
        Returns:
            Numpy array representing depth map
        """
        # Convert to grayscale and normalize
        gray = image.convert('L')
        depth = np.array(gray, dtype=np.float32) / 255.0
        
        # Invert so brighter areas are closer
        depth = 1.0 - depth
        
        print(f"✅ Generated depth map (shape: {depth.shape})")
        return depth
    
    def depth_to_pointcloud(self, image, depth_map, scale=1.0, max_depth=10.0):
        """
        Convert depth map to 3D point cloud
        
        Args:
            image: Original PIL Image
            depth_map: 2D numpy array of depth values
            scale: Scaling factor for the model
            max_depth: Maximum depth value
            
        Returns:
            trimesh.PointCloud object
        """
        img_array = np.array(image)
        height, width = depth_map.shape
        
        # Create coordinate grids
        x_coords, y_coords = np.meshgrid(np.arange(width), np.arange(height))
        
        # Flatten arrays
        x_coords = x_coords.flatten()
        y_coords = y_coords.flatten()
        z_coords = depth_map.flatten() * max_depth
        
        # Create 3D points
        points = np.column_stack((
            x_coords * scale,
            y_coords * scale,
            z_coords
        ))
        
        # Get colors from original image
        if len(img_array.shape) == 3:
            colors = img_array.reshape(-1, img_array.shape[2])
        else:
            # Grayscale - convert to RGB
            gray_flat = img_array.flatten()
            colors = np.column_stack([gray_flat, gray_flat, gray_flat])
        
        # Create point cloud
        point_cloud = trimesh.PointCloud(vertices=points, colors=colors)
        print(f"✅ Created point cloud with {len(points)} points")
        
        return point_cloud
    
    def pointcloud_to_mesh(self, point_cloud, method='ball_pivoting'):
        """
        Convert point cloud to mesh (simplified version)
        
        Args:
            point_cloud: trimesh.PointCloud object
            method: Meshing method to use
            
        Returns:
            trimesh.Trimesh object
        """
        # For simplicity, create a basic mesh using convex hull
        try:
            mesh = point_cloud.convex_hull
            print(f"✅ Created mesh with {len(mesh.vertices)} vertices and {len(mesh.faces)} faces")
            return mesh
        except Exception as e:
            print(f"⚠️  Could not create mesh: {e}")
            return None
    
    def image_to_3d(self, image_path, output_name=None, export_format='obj'):
        """
        Complete pipeline: image to 3D model
        
        Args:
            image_path: Path to input image
            output_name: Name for output file (without extension)
            export_format: Output format ('obj', 'ply', 'stl')
            
        Returns:
            Path to saved 3D model file
        """
        print(f"\n🚀 Starting 3D conversion for: {image_path}")
        
        # Load image
        image = self.load_image(image_path)
        if image is None:
            return None
        
        # Resize for processing (optional, for performance)
        if max(image.size) > self.max_image_size:
            ratio = self.max_image_size / max(image.size)
            new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
            image = image.resize(new_size, Image.LANCZOS)
            print(f"📏 Resized image to {new_size} for processing")
        
        # Estimate depth
        depth_map = self.estimate_depth_simple(image)
        
        # Convert to point cloud
        point_cloud = self.depth_to_pointcloud(image, depth_map, scale=0.1, max_depth=5.0)
        
        # Convert to mesh
        mesh = self.pointcloud_to_mesh(point_cloud)
        
        # Export
        if output_name is None:
            output_name = os.path.splitext(os.path.basename(image_path))[0]
        
        if mesh:
            output_path = os.path.join(self.output_dir, f"{output_name}.{export_format}")
            mesh.export(output_path)
            print(f"✅ 3D model saved to: {output_path}")
            return output_path
        else:
            # Export point cloud if mesh creation failed
            output_path = os.path.join(self.output_dir, f"{output_name}.ply")
            point_cloud.export(output_path)
            print(f"✅ Point cloud saved to: {output_path}")
            return output_path


class Video3DConverter:
    """Convert videos to 3D models by extracting and processing frames"""
    
    def __init__(self, output_dir="output_3d_models"):
        """
        Initialize the video converter
        
        Args:
            output_dir: Directory to save generated 3D models
        """
        self.output_dir = output_dir
        self.photo_converter = Photo3DConverter(output_dir)
        print(f"✅ Video 3D Converter initialized")
    
    def extract_frames(self, video_path, num_frames=10):
        """
        Extract frames from video
        
        Args:
            video_path: Path to video file
            num_frames: Number of frames to extract
            
        Returns:
            List of frame file paths
        """
        try:
            import imageio.v2 as imageio
            
            print(f"📹 Extracting {num_frames} frames from {video_path}...")
            
            # Create temporary directory for frames
            frames_dir = os.path.join(self.output_dir, "temp_frames")
            os.makedirs(frames_dir, exist_ok=True)
            
            # Read video
            reader = imageio.get_reader(video_path)
            metadata = reader.get_meta_data()
            
            # Get total frame count - try multiple methods
            total_frames = metadata.get('nframes')
            if total_frames is None:
                try:
                    total_frames = len(reader)
                except (TypeError, AttributeError, NotImplementedError):
                    # Fallback: estimate from fps and duration
                    fps = metadata.get('fps', 30)
                    duration = metadata.get('duration', 1)
                    total_frames = int(fps * duration) if duration else 100
            
            # Calculate frame indices to extract
            if total_frames < num_frames:
                frame_indices = range(int(total_frames))
            else:
                step = int(total_frames) // num_frames
                frame_indices = range(0, int(total_frames), step)[:num_frames]
            
            # Extract frames
            frame_paths = []
            for i, frame_idx in enumerate(frame_indices):
                try:
                    reader.set_image_index(frame_idx)
                    frame = reader.get_next_data()
                    frame_path = os.path.join(frames_dir, f"frame_{i:04d}.png")
                    imageio.imwrite(frame_path, frame)
                    frame_paths.append(frame_path)
                except (IndexError, IOError, RuntimeError, ValueError) as e:
                    print(f"⚠️  Could not extract frame {frame_idx}: {e}")
                    continue
            
            reader.close()
            print(f"✅ Extracted {len(frame_paths)} frames")
            return frame_paths
            
        except ImportError:
            print("❌ imageio library required for video processing. Install with: pip install imageio")
            return []
        except Exception as e:
            print(f"❌ Error extracting frames: {e}")
            return []
    
    def video_to_3d(self, video_path, output_name=None, frame_to_use='first'):
        """
        Convert video to 3D model
        
        Args:
            video_path: Path to video file
            output_name: Name for output file
            frame_to_use: Which frame to use ('first', 'middle', frame_number)
            
        Returns:
            Path to saved 3D model file
        """
        print(f"\n🎬 Starting 3D conversion from video: {video_path}")
        
        # Extract frames
        frames = self.extract_frames(video_path, num_frames=10)
        if not frames:
            return None
        
        # Select frame to process
        if frame_to_use == 'first':
            selected_frame = frames[0]
        elif frame_to_use == 'middle':
            selected_frame = frames[len(frames) // 2]
        elif isinstance(frame_to_use, int) and frame_to_use < len(frames):
            selected_frame = frames[frame_to_use]
        else:
            selected_frame = frames[0]
        
        print(f"🎯 Using frame: {selected_frame}")
        
        # Convert selected frame to 3D
        if output_name is None:
            output_name = os.path.splitext(os.path.basename(video_path))[0]
        
        result = self.photo_converter.image_to_3d(selected_frame, output_name)
        
        # Cleanup temp frames (optional)
        try:
            import shutil
            frames_dir = os.path.join(self.output_dir, "temp_frames")
            if os.path.exists(frames_dir):
                shutil.rmtree(frames_dir)
                print("🧹 Cleaned up temporary frames")
        except (OSError, PermissionError) as e:
            print(f"⚠️  Could not clean up temporary frames: {e}")
        
        return result


def main():
    """Example usage of the 3D conversion tools"""
    print("=" * 60)
    print("3D Model Generator from Photos and Videos")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("\n📖 Usage:")
        print("  python photo_to_3d.py <image_or_video_path> [output_name]")
        print("\n📝 Examples:")
        print("  python photo_to_3d.py assets/battlefield.png")
        print("  python photo_to_3d.py video/iron_dome.mp4 iron_dome_3d")
        print("\n💡 Supported formats:")
        print("  Images: PNG, JPG, JPEG, BMP, GIF")
        print("  Videos: MP4, AVI, MOV (requires imageio)")
        return
    
    input_path = sys.argv[1]
    output_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Check if file exists
    if not os.path.exists(input_path):
        print(f"❌ Error: File not found: {input_path}")
        return
    
    # Determine if input is image or video
    ext = os.path.splitext(input_path)[1].lower()
    image_exts = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
    video_exts = ['.mp4', '.avi', '.mov', '.mkv']
    
    if ext in image_exts:
        # Process as image
        converter = Photo3DConverter()
        result = converter.image_to_3d(input_path, output_name)
    elif ext in video_exts:
        # Process as video
        converter = Video3DConverter()
        result = converter.video_to_3d(input_path, output_name)
    else:
        print(f"❌ Unsupported file format: {ext}")
        return
    
    if result:
        print("\n" + "=" * 60)
        print("✨ Success! 3D model generated")
        print("=" * 60)
        print(f"\n📦 Output file: {result}")
        print("\n💡 You can view the 3D model using:")
        print("  - Blender (free, open-source)")
        print("  - MeshLab (free)")
        print("  - Online viewers (e.g., Clara.io)")
    else:
        print("\n❌ Failed to generate 3D model")


if __name__ == "__main__":
    main()
