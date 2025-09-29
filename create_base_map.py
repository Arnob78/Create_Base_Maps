import geopandas as gpd
import matplotlib.pyplot as plt
import os
import contextily as ctx
from pyproj import Transformer
import numpy as np
from matplotlib.patches import Patch

def create_base_map(shapefile_path, output_dir):
    """
    Creates a base map from a shapefile and saves it as a PNG image.

    Args:
        shapefile_path (str): The path to the input shapefile.
        output_dir (str): The directory to save the output PNG file.
    """
    # Read the shapefile
    gdf = gpd.read_file(shapefile_path)

    # Get the shapefile name without extension for the title
    shapefile_name = os.path.splitext(os.path.basename(shapefile_path))[0]
    # Create a nice title by replacing underscores with spaces and capitalizing
    map_title = shapefile_name.replace('_', ' ').title()

    # Set initial CRS and reproject
    gdf_wm = gdf.set_crs(epsg=4326).to_crs(epsg=3857)

    # Create a plot
    fig, ax = plt.subplots(1, 1, figsize=(15, 15))

    # Plot the shapefile with THICKER BLACK BOUNDARY
    gdf_wm.plot(ax=ax, alpha=0.5, edgecolor='black', facecolor='saddlebrown', linewidth=3)  # CHANGED: edgecolor to 'black' and linewidth to 3

    # Get the bounding box of the reprojected data
    west, south, east, north = gdf_wm.total_bounds

    # Calculate the range
    x_range = east - west
    y_range = north - south

    # Add 20% padding
    x_padding = x_range * 0.2
    y_padding = y_range * 0.2

    # Set the new limits
    ax.set_xlim(west - x_padding, east + x_padding)
    ax.set_ylim(south - y_padding, north + y_padding)

    # Add basemap to the plot
    ctx.add_basemap(ax, crs=gdf_wm.crs.to_string(), source=ctx.providers.OpenStreetMap.HOT)

    # Create a transformer to convert from Web Mercator to WGS84
    transformer = Transformer.from_crs("epsg:3857", "epsg:4326", always_xy=True)

    # Calculate tick positions in Web Mercator
    x_ticks = np.linspace(west - x_padding, east + x_padding, 6)
    y_ticks = np.linspace(south - y_padding, north + y_padding, 6)

    # Convert tick positions to lat/lon for labels
    x_tick_lons, _ = transformer.transform(x_ticks, [south] * len(x_ticks))
    _, y_tick_lats = transformer.transform([west] * len(y_ticks), y_ticks)

    # Set ticks and labels
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    ax.set_xticklabels([f'{lon:.2f}°E' for lon in x_tick_lons])
    ax.set_yticklabels([f'{lat:.2f}°N' for lat in y_tick_lats])

    # Increase font size for tick labels
    ax.tick_params(axis='both', which='major', labelsize=16)

    # Add gridlines (AFTER setting ticks)
    ax.grid(True, linestyle='--', alpha=0.8, linewidth=1.5)

    # Create custom legend
    legend_elements = [Patch(facecolor='saddlebrown', alpha=0.5, edgecolor='black', 
                            label='Study Area')]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=14, frameon=True)

    # Custom scale bar with "15 KM" text on top - MOVED DOWN ABOUT 3 POINTS
    scalebar_length = 15000  # 15 km in meters
    scalebar_x_start = east + x_padding - scalebar_length - 5000  # Right side with padding
    scalebar_y = south - y_padding + y_range * 0.05  # MOVED DOWN (decreased from 0.20 to 0.15)
    
    # Draw the scale bar line
    ax.plot([scalebar_x_start, scalebar_x_start + scalebar_length], 
            [scalebar_y, scalebar_y], 
            color='black', linewidth=6, solid_capstyle='butt')
    
    # Add "15 KM" text
    ax.text(scalebar_x_start + scalebar_length / 2, scalebar_y + 500, 
            '15 KM', ha='center', va='bottom', fontsize=14, fontweight='bold')

    # Add end markers
    ax.plot([scalebar_x_start, scalebar_x_start], 
            [scalebar_y - 300, scalebar_y + 300], 
            color='black', linewidth=2)
    ax.plot([scalebar_x_start + scalebar_length, scalebar_x_start + scalebar_length], 
            [scalebar_y - 300, scalebar_y + 300], 
            color='black', linewidth=2)

    # Add a SHORTER and THICKER north arrow
    x, y, arrow_length = 0.95, 0.95, 0.05  # SHORTER arrow (decreased from 0.1 to 0.05)
    ax.annotate('N', xy=(x, y), xytext=(x, y - arrow_length),
                arrowprops=dict(facecolor='black', width=8, headwidth=20, headlength=15),  # THICKER
                ha='center', va='center', fontsize=20,
                xycoords=ax.transAxes)

    # Set title and axis labels - USING DYNAMIC TITLE FROM FILENAME
    ax.set_title(map_title, fontsize=26)
    ax.set_xlabel("Longitude", fontsize=20)
    ax.set_ylabel("Latitude", fontsize=20)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Save the plot as a PNG file
    output_path = os.path.join(output_dir, f"{shapefile_name}_basemap.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0.5, transparent=True)
    print(f"Base map saved to: {output_path}")

    plt.show()

if __name__ == "__main__":
    # Prompt user for shapefile path
    print("Please enter the path to your shapefile/GeoJSON file:")
    shapefile_path = input().strip()
    
    # Remove quotes if user entered them
    shapefile_path = shapefile_path.strip('"\'')
    
    # Check if file exists
    if not os.path.exists(shapefile_path):
        print(f"Error: File not found at {shapefile_path}")
        exit(1)
    
    # Define the output directory
    output_dir = r"C:\Users\NagaiLab\Gemini_conversation\Create_Base_Maps\output_base_maps"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    print(f"Processing shapefile: {shapefile_path}")
    print(f"Output will be saved to: {output_dir}")
    
    # Create the base map
    create_base_map(shapefile_path, output_dir)