"""
Example: Using the 3D Conversion API

This script demonstrates various ways to use the photo_to_3d module
programmatically in your Python projects.
"""

from photo_to_3d import Photo3DConverter, Video3DConverter
import os


def example_1_basic_image_conversion():
    """Example 1: Convert a single image to 3D"""
    print("\n" + "=" * 60)
    print("Example 1: Basic Image to 3D Conversion")
    print("=" * 60)
    
    # Initialize converter
    converter = Photo3DConverter(output_dir="examples_output")
    
    # Convert the battlefield image
    if os.path.exists("assets/battlefield.png"):
        result = converter.image_to_3d(
            image_path="assets/battlefield.png",
            output_name="battlefield_3d",
            export_format="obj"
        )
        print(f"✅ Example 1 complete! Model saved to: {result}")
    else:
        print("⚠️  assets/battlefield.png not found, skipping example 1")


def example_2_custom_parameters():
    """Example 2: Custom parameters for depth and scale"""
    print("\n" + "=" * 60)
    print("Example 2: Custom Depth Parameters")
    print("=" * 60)
    
    from PIL import Image
    
    converter = Photo3DConverter(output_dir="examples_output")
    
    if os.path.exists("assets/battlefield.png"):
        # Load image
        image = converter.load_image("assets/battlefield.png")
        
        # Resize for processing
        image = image.resize((150, 150))
        
        # Estimate depth
        depth_map = converter.estimate_depth_simple(image)
        
        # Convert with custom parameters
        point_cloud = converter.depth_to_pointcloud(
            image, 
            depth_map,
            scale=0.2,      # Larger scale
            max_depth=10.0  # Greater depth range
        )
        
        # Create mesh and export
        mesh = converter.pointcloud_to_mesh(point_cloud)
        if mesh:
            output_path = "examples_output/battlefield_custom.obj"
            mesh.export(output_path)
            print(f"✅ Example 2 complete! Model saved to: {output_path}")
    else:
        print("⚠️  assets/battlefield.png not found, skipping example 2")


def example_3_video_conversion():
    """Example 3: Convert video to 3D"""
    print("\n" + "=" * 60)
    print("Example 3: Video to 3D Conversion")
    print("=" * 60)
    
    # Initialize video converter
    converter = Video3DConverter(output_dir="examples_output")
    
    if os.path.exists("video/iron_dome.mp4"):
        # Convert using middle frame
        result = converter.video_to_3d(
            video_path="video/iron_dome.mp4",
            output_name="iron_dome_3d",
            frame_to_use='middle'
        )
        print(f"✅ Example 3 complete! Model saved to: {result}")
    else:
        print("⚠️  video/iron_dome.mp4 not found, skipping example 3")


def example_4_batch_processing():
    """Example 4: Batch process multiple images"""
    print("\n" + "=" * 60)
    print("Example 4: Batch Image Processing")
    print("=" * 60)
    
    converter = Photo3DConverter(output_dir="examples_output/batch")
    
    # Find all PNG files in assets
    if os.path.exists("assets"):
        image_files = [f for f in os.listdir("assets") if f.endswith('.png')]
        
        if image_files:
            print(f"Found {len(image_files)} images to process")
            
            for image_file in image_files:
                image_path = os.path.join("assets", image_file)
                output_name = os.path.splitext(image_file)[0] + "_3d"
                
                print(f"\nProcessing: {image_file}")
                converter.image_to_3d(
                    image_path=image_path,
                    output_name=output_name,
                    export_format="ply"
                )
            
            print(f"\n✅ Example 4 complete! Processed {len(image_files)} images")
        else:
            print("⚠️  No PNG files found in assets/")
    else:
        print("⚠️  assets/ directory not found")


def example_5_point_cloud_only():
    """Example 5: Export point cloud without mesh conversion"""
    print("\n" + "=" * 60)
    print("Example 5: Point Cloud Export")
    print("=" * 60)
    
    converter = Photo3DConverter(output_dir="examples_output")
    
    if os.path.exists("assets/battlefield.png"):
        # Load and process image
        image = converter.load_image("assets/battlefield.png")
        image = image.resize((100, 100))
        depth_map = converter.estimate_depth_simple(image)
        
        # Create point cloud
        point_cloud = converter.depth_to_pointcloud(
            image, 
            depth_map,
            scale=0.15,
            max_depth=8.0
        )
        
        # Export point cloud directly (no mesh)
        output_path = "examples_output/battlefield_pointcloud.ply"
        point_cloud.export(output_path)
        print(f"✅ Example 5 complete! Point cloud saved to: {output_path}")
    else:
        print("⚠️  assets/battlefield.png not found, skipping example 5")


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("3D Conversion API Examples")
    print("=" * 60)
    print("\nThis script demonstrates various ways to use the 3D conversion tools.")
    print("Check the 'examples_output' directory for generated 3D models.")
    
    try:
        # Run examples
        example_1_basic_image_conversion()
        example_2_custom_parameters()
        example_3_video_conversion()
        example_4_batch_processing()
        example_5_point_cloud_only()
        
        print("\n" + "=" * 60)
        print("All examples completed!")
        print("=" * 60)
        print("\n📁 Check the 'examples_output' directory for generated 3D models")
        print("💡 You can view them in Blender, MeshLab, or online viewers")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
