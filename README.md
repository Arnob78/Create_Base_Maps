# Create Base Maps

This project contains a Python script to create a base map from a shapefile and overlay it with a basemap from a tile server. The script is designed to be easily customizable for different shapefiles and map styles.

## Setup

To run this project, you will need to have Conda installed.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Arnob78/Create_Base_Maps.git
    cd Create_Base_Maps
    ```

2.  **Create the Conda environment:**
    Use the `environment.yml` file to create the Conda environment with all the necessary dependencies.
    ```bash
    conda env create -f environment.yml
    ```

3.  **Activate the environment:**
    ```bash
    conda activate BASE_MAP_CREATION
    ```

## Usage

To generate the base map, run the `create_base_map.py` script:
```bash
python create_base_map.py
```

The output map will be saved in the `output_base_maps` directory.

## Customization

You can customize the script in `create_base_map.py` to:
*   Use a different shapefile by changing the `shapefile_path` variable.
*   Change the output directory by modifying the `output_dir` variable.
*   Adjust the map's appearance, such as colors, fonts, and basemap provider.
