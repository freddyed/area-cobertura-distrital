# Mobile Coverage Analysis in Peruvian Districts

This repository contains a Python script that processes mobile coverage maps and intersects them with district maps of Peru to obtain the coverage area (km²) per district, linked to its UBIGEO code.

## 📌 Features

*   📍 Geospatial Processing: Uses `geopandas` to read and manipulate shapefiles (.shp).
*   🌎 Coordinate System Transformation: Converts geometries from geographic coordinates (EPSG:4326) to a projected system (EPSG:32718) to ensure accurate area calculations.
*   📡 Mobile Coverage Analysis: Supports multiple mobile technologies: 2G, 3G, 4G, and 5G.
*   🏢 Telecom Operators: Processes coverage data for the four main operators in Peru.
*   📊 District-Level Intersection: Intersects mobile coverage layers with district boundaries to calculate the covered area per district.
*   📂 Excel Report Generation: Exports the results to an Excel file (.xlsx) with structured data for further analysis.

## 🛠 Requirements

Make sure you have the following dependencies installed:

```bash
pip install geopandas pandas
```

## 🚀 Usage

*   Set the `base_dir` variable to the directory containing the .shp files for mobile coverage.
*   Ensure the district shapefile (DISTRITOS.shp) is available in the specified path.
*   Run the script to process the data and generate an Excel file with the results.

## 📁 Output

The script generates an Excel file `area-cubierta-total.xlsx`, containing the following columns:

*   `UBIGEO` – Unique district identifier.
*   `DEPARTAMEN` – Name of the department.
*   `PROVINCIA` – Name of the province.
*   `DISTRITO` – Name of the district.
*   `area_km2-{technology}-{coverage_type}` – Covered area (km²) for each technology and coverage type.

## 🤝 Contributions

Feel free to contribute by submitting a Pull Request or opening an Issue with suggestions or improvements.

## 📜 License

This project is open-source and available under the MIT License.
