import streamlit as st
import rasterio
import geopandas as gpd
import numpy as np
import folium
from streamlit_folium import st_folium
from rasterstats import zonal_stats
import tempfile
import os
from matplotlib import pyplot as plt
from matplotlib.patches import FancyArrow, Rectangle
import io


def render():
    """Render the MAPS tab for raster and vector analysis"""

    # CSS dla białego dropdown (BEZPOŚREDNIO w MAPS)
    st.markdown("""
    <style>
        /* Wymuszenie białego dropdown menu */
        div[data-baseweb="popover"] {
            background-color: #ffffff !important;
        }

        div[data-baseweb="popover"] ul {
            background-color: #ffffff !important;
        }

        ul[role="listbox"] {
            background-color: #ffffff !important;
            border: 1px solid #ddd !important;
        }

        ul[role="listbox"] li {
            background-color: #ffffff !important;
            color: #000000 !important;
            padding: 0.5rem 1rem !important;
        }

        ul[role="listbox"] li:hover {
            background-color: #f0f0f0 !important;
        }

        ul[role="listbox"] li[aria-selected="true"] {
            background-color: #e8e8e8 !important;
            font-weight: 600 !important;
        }

        /* Selectbox - biały input */
        div[data-baseweb="select"] {
            background-color: #ffffff !important;
        }

        div[data-baseweb="select"] > div {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 1px solid #ddd !important;
        }

        div[data-baseweb="select"] input {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar configuration
    with st.sidebar:
        st.markdown("### 📁 File Manager")

        # Raster upload
        st.markdown("#### 🛰️ Raster Data")
        uploaded_bands = st.file_uploader(
            "Upload Sentinel-2 bands",
            type=['tif', 'tiff'],
            accept_multiple_files=True,
            help="Upload multiple TIFF files",
            key="raster_upload"
        )

        if uploaded_bands:
            st.success(f"✓ {len(uploaded_bands)} files loaded")
            with st.expander("📋 View files", expanded=False):
                for band in uploaded_bands:
                    st.text(f"• {band.name}")

        st.markdown("---")

        # Vector upload
        st.markdown("#### 📐 Vector Data")
        uploaded_vector = st.file_uploader(
            "Upload GeoJSON (optional)",
            type=['geojson', 'json'],
            help="For zonal statistics",
            key="vector_upload"
        )

        if uploaded_vector:
            st.success(f"✓ {uploaded_vector.name}")

        st.markdown("---")

        # Analysis settings
        st.markdown("### ⚙️ Analysis Settings")

        # Index selection - WSZYSTKIE INDEKSY
        index_type = st.selectbox(
            "Spectral Index",
            [
                "NDVI", "EVI", "SAVI", "GNDVI", "NDRE",  # Vegetation
                "NDWI", "MNDWI", "NDMI",  # Water
                "NDBI", "BSI", "UI",  # Urban
                "NBR", "BAIS2", "NBR2",  # Fire
                "NDSI", "S2WI"  # Snow
            ],
            help="Select spectral index to calculate"
        )

        # Colormap
        colormap_options = {
            'RdYlGn': 'RdYlGn',
            'RdBu': 'RdBu',
            'Spectral': 'Spectral',
            'viridis': 'viridis',
            'plasma': 'plasma',
            'inferno': 'inferno',
            'magma': 'magma',
            'coolwarm': 'coolwarm',
            'YlOrRd': 'YlOrRd',
            'PuOr': 'PuOr',
            'BrBG': 'BrBG',
            'Greys': 'Greys'
        }

        selected_colormap = st.selectbox(
            "Color Palette",
            list(colormap_options.keys()),
            index=0
        )

        # Reverse colormap
        reverse_cmap = st.checkbox("Reverse Palette", value=False)

        st.markdown("---")

        # MAP CUSTOMIZATION
        st.markdown("### 🗺️ Map Settings")

        # Custom title
        map_title = st.text_input(
            "Map Title",
            value=f"{index_type} Analysis",
            help="Enter custom title for your map"
        )

        # Show scale bar
        show_scale = st.checkbox("Show Scale Bar", value=True)

        # Show north arrow
        show_north = st.checkbox("Show North Arrow", value=True)

        # Show legend
        show_legend = st.checkbox("Show Legend", value=True)

        st.markdown("---")

        # Process button
        if uploaded_bands:
            if st.button("🚀 Run Analysis", use_container_width=True, type="primary"):
                st.session_state.run_analysis = True
                st.session_state.map_title = map_title
                st.session_state.show_scale = show_scale
                st.session_state.show_north = show_north
                st.session_state.show_legend = show_legend
        else:
            st.info("👆 Upload files first")

    # Main content area - FULL WIDTH
    if uploaded_bands and ('run_analysis' in st.session_state and st.session_state.run_analysis):
        # Get settings from session state
        map_title = st.session_state.get('map_title', f"{index_type} Analysis")
        show_scale = st.session_state.get('show_scale', True)
        show_north = st.session_state.get('show_north', True)
        show_legend = st.session_state.get('show_legend', True)

        process_raster_data(
            uploaded_bands, uploaded_vector, index_type,
            selected_colormap, reverse_cmap,
            map_title, show_scale, show_north, show_legend
        )
    elif uploaded_bands:
        st.info("👈 Click 'Run Analysis' in the sidebar to start processing")
    else:
        st.info("👈 Upload raster files using the sidebar to begin")

        # Quick guide
        with st.expander("📖 Quick Start Guide", expanded=True):
            st.markdown("""
            **Required bands for each index:**

            | Index | Required Bands | Category |
            |-------|----------------|----------|
            | **NDVI** | B4 (Red) + B8 (NIR) | 🌿 Vegetation |
            | **EVI** | B2 (Blue) + B4 (Red) + B8 (NIR) | 🌿 Vegetation |
            | **SAVI** | B4 (Red) + B8 (NIR) | 🌿 Vegetation |
            | **GNDVI** | B3 (Green) + B8 (NIR) | 🌿 Vegetation |
            | **NDRE** | B5 (Red Edge) + B8 (NIR) | 🌿 Vegetation |
            | **NDWI** | B3 (Green) + B8 (NIR) | 💧 Water |
            | **MNDWI** | B3 (Green) + B11 (SWIR1) | 💧 Water |
            | **NDMI** | B8 (NIR) + B11 (SWIR1) | 💧 Water |
            | **NDBI** | B8 (NIR) + B11 (SWIR1) | 🏙️ Urban |
            | **BSI** | B2 + B4 + B8 + B11 | 🏙️ Urban |
            | **UI** | B8 (NIR) + B12 (SWIR2) | 🏙️ Urban |
            | **NBR** | B8 (NIR) + B12 (SWIR2) | 🔥 Fire |
            | **NBR2** | B11 (SWIR1) + B12 (SWIR2) | 🔥 Fire |
            | **BAIS2** | B4 + B6 + B7 + B8A + B12 | 🔥 Fire |
            | **NDSI** | B3 (Green) + B11 (SWIR1) | ❄️ Snow |
            | **S2WI** | B8 (NIR) + B12 (SWIR2) | ❄️ Snow |

            **Steps:**
            1. 📁 Upload Sentinel-2 band files (.tif) in the sidebar
            2. 📐 Optionally upload vector data (.geojson)
            3. ⚙️ Select spectral index and color palette
            4. 🗺️ Customize map settings (title, scale, north arrow)
            5. 🚀 Click 'Run Analysis'
            6. 💾 Download results
            """)


def process_raster_data(uploaded_bands, uploaded_vector, index_type, colormap, reverse_cmap,
                        map_title, show_scale, show_north, show_legend):
    """Process raster data and calculate spectral indices"""

    try:
        # Save uploaded files temporarily
        temp_files = []
        band_data = {}

        with st.spinner("🔄 Loading raster data..."):
            for band_file in uploaded_bands:
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.tif')
                temp_file.write(band_file.read())
                temp_file.close()
                temp_files.append(temp_file.name)

                # Identify band from filename
                filename = band_file.name.upper()
                if 'B04' in filename or 'B4_' in filename or '_B4.' in filename:
                    band_data['B4'] = temp_file.name
                elif 'B03' in filename or 'B3_' in filename or '_B3.' in filename:
                    band_data['B3'] = temp_file.name
                elif 'B02' in filename or 'B2_' in filename or '_B2.' in filename:
                    band_data['B2'] = temp_file.name
                elif 'B05' in filename or 'B5_' in filename or '_B5.' in filename:
                    band_data['B5'] = temp_file.name
                elif 'B06' in filename or 'B6_' in filename or '_B6.' in filename:
                    band_data['B6'] = temp_file.name
                elif 'B07' in filename or 'B7_' in filename or '_B7.' in filename:
                    band_data['B7'] = temp_file.name
                elif 'B08' in filename or 'B8_' in filename or '_B8.' in filename:
                    band_data['B8'] = temp_file.name
                elif 'B8A' in filename or 'B08A' in filename:
                    band_data['B8A'] = temp_file.name
                elif 'B11' in filename:
                    band_data['B11'] = temp_file.name
                elif 'B12' in filename:
                    band_data['B12'] = temp_file.name

        st.success(f"✅ Loaded {len(band_data)} bands: {', '.join(band_data.keys())}")

        # Calculate spectral index
        index_result = calculate_spectral_index(band_data, index_type)

        if index_result is not None:
            index_array, profile = index_result

            st.success(f"✅ {index_type} calculated successfully!")

            # Display statistics
            display_statistics(index_array, index_type)

            # Create FULL-SCREEN visualization with custom settings
            fig = visualize_index(
                index_array, profile, index_type, colormap, reverse_cmap,
                map_title, show_scale, show_north, show_legend
            )

            # Process vector data if available
            if uploaded_vector:
                process_vector_analysis(uploaded_vector, index_array, profile, index_type)

            # Create interactive map
            create_interactive_map(index_array, profile, index_type, colormap, reverse_cmap)

            # Download section
            create_download_section(index_array, profile, index_type, fig)

        # Cleanup temporary files
        for temp_file in temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass

    except Exception as e:
        st.error(f"❌ Error processing data: {str(e)}")
        st.exception(e)


def calculate_spectral_index(band_data, index_type):
    """Calculate spectral index based on available bands"""

    index_formulas = {
        # Vegetation
        'NDVI': {'bands': ['B4', 'B8'], 'formula': lambda r, n: (n - r) / (n + r + 1e-10)},
        'EVI': {'bands': ['B2', 'B4', 'B8'],
                'formula': lambda b, r, n: 2.5 * ((n - r) / (n + 6 * r - 7.5 * b + 1 + 1e-10))},
        'SAVI': {'bands': ['B4', 'B8'],
                 'formula': lambda r, n: ((n - r) / (n + r + 0.5)) * 1.5},
        'GNDVI': {'bands': ['B3', 'B8'],
                  'formula': lambda g, n: (n - g) / (n + g + 1e-10)},
        'NDRE': {'bands': ['B5', 'B8'],
                 'formula': lambda re, n: (n - re) / (n + re + 1e-10)},

        # Water
        'NDWI': {'bands': ['B3', 'B8'], 'formula': lambda g, n: (g - n) / (g + n + 1e-10)},
        'MNDWI': {'bands': ['B3', 'B11'], 'formula': lambda g, s: (g - s) / (g + s + 1e-10)},
        'NDMI': {'bands': ['B8', 'B11'], 'formula': lambda n, s: (n - s) / (n + s + 1e-10)},

        # Urban
        'NDBI': {'bands': ['B8', 'B11'], 'formula': lambda n, s: (s - n) / (s + n + 1e-10)},
        'BSI': {'bands': ['B2', 'B4', 'B8', 'B11'],
                'formula': lambda b, r, n, s: ((s + r) - (n + b)) / ((s + r) + (n + b) + 1e-10)},
        'UI': {'bands': ['B8', 'B12'], 'formula': lambda n, s: (s - n) / (s + n + 1e-10)},

        # Fire
        'NBR': {'bands': ['B8', 'B12'], 'formula': lambda n, s: (n - s) / (n + s + 1e-10)},
        'NBR2': {'bands': ['B11', 'B12'], 'formula': lambda s1, s2: (s1 - s2) / (s1 + s2 + 1e-10)},
        'BAIS2': {'bands': ['B4', 'B6', 'B7', 'B8A', 'B12'],
                  'formula': lambda r, re2, re3, nir_n, swir2:
                  (1 - np.sqrt((re2 * re3 * nir_n) / (r + 1e-10))) *
                  ((swir2 - nir_n) / (np.sqrt(swir2 + nir_n) + 1) + 1)},

        # Snow
        'NDSI': {'bands': ['B3', 'B11'], 'formula': lambda g, s: (g - s) / (g + s + 1e-10)},
        'S2WI': {'bands': ['B8', 'B12'], 'formula': lambda n, s: (n - s) / (n + s + 1e-10)}
    }

    if index_type not in index_formulas:
        st.error(f"Index {index_type} not implemented")
        return None

    required_bands = index_formulas[index_type]['bands']
    formula = index_formulas[index_type]['formula']

    # Check if all required bands are available
    missing_bands = [b for b in required_bands if b not in band_data]
    if missing_bands:
        st.error(f"❌ Missing required bands for {index_type}: {', '.join(missing_bands)}")
        st.info(f"📋 Please upload: {', '.join(required_bands)}")
        return None

    # Read bands
    try:
        band_arrays = []
        profile = None

        for band_name in required_bands:
            with rasterio.open(band_data[band_name]) as src:
                band_array = src.read(1).astype(float)
                band_arrays.append(band_array)
                if profile is None:
                    profile = src.profile

        # Calculate index
        index_array = formula(*band_arrays)

        # Clip extreme values
        index_array = np.clip(index_array, -1, 1)

        return index_array, profile

    except Exception as e:
        st.error(f"Error calculating {index_type}: {str(e)}")
        st.exception(e)
        return None


def display_statistics(index_array, index_type):
    """Display statistical information about the index"""

    st.markdown("### 📈 Statistical Summary")

    valid_data = index_array[~np.isnan(index_array)]

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Mean", f"{np.mean(valid_data):.4f}")
    with col2:
        st.metric("Median", f"{np.median(valid_data):.4f}")
    with col3:
        st.metric("Std Dev", f"{np.std(valid_data):.4f}")
    with col4:
        st.metric("Min", f"{np.min(valid_data):.4f}")
    with col5:
        st.metric("Max", f"{np.max(valid_data):.4f}")

    st.markdown("---")


def visualize_index(index_array, profile, index_type, colormap, reverse_cmap,
                    map_title, show_scale, show_north, show_legend):
    st.markdown("### 🎨 Index Visualization")

    # FULL SCREEN: mapa wypełnia cały obszar
    fig = plt.figure(figsize=(20, 14), dpi=150, facecolor='white')

    # Main map takes THE ENTIRE FIGURE (100%)
    ax = fig.add_axes([0, 0, 1, 1])

    cmap = plt.cm.get_cmap(colormap)
    if reverse_cmap:
        cmap = cmap.reversed()

    # Plot with high quality interpolation - FULL EXTENT
    im = ax.imshow(index_array, cmap=cmap, vmin=-1, vmax=1, interpolation='bilinear', aspect='auto')

    ax.axis('off')
    ax.set_xlim(0, index_array.shape[1])
    ax.set_ylim(index_array.shape[0], 0)

    # LEGEND BOX - LEFT BOTTOM CORNER
    legend_left = 0.01
    legend_bottom = 0.01
    legend_width = 0.28
    legend_height = 0.20

    # White background box for entire legend
    legend_bg = Rectangle((legend_left, legend_bottom), legend_width, legend_height,
                          transform=fig.transFigure,
                          facecolor='white', alpha=1.0, edgecolor='black', linewidth=3, zorder=10)
    fig.patches.append(legend_bg)

    # TITLE inside legend box
    fig.text(legend_left + legend_width / 2, legend_bottom + legend_height - 0.02,
             map_title,
             ha='center', va='top', fontsize=20, fontweight='bold',
             transform=fig.transFigure, zorder=11)

    # HORIZONTAL COLORBAR in legend box
    if show_legend:
        cbar_left = legend_left + 0.025
        cbar_bottom = legend_bottom + 0.09
        cbar_width = legend_width - 0.05
        cbar_height = 0.04

        cbar_ax = fig.add_axes([cbar_left, cbar_bottom, cbar_width, cbar_height], zorder=12)

        gradient_data = np.linspace(-1, 1, 256).reshape(1, -1)
        gradient_x = np.linspace(-1, 1, 257)
        gradient_y = [0, 1]

        mesh = cbar_ax.pcolormesh(gradient_x, gradient_y, gradient_data,
                                  cmap=cmap, shading='auto', vmin=-1, vmax=1)

        cbar_ax.set_xlim(-1, 1)
        cbar_ax.set_ylim(0, 1)
        cbar_ax.set_yticks([])
        cbar_ax.set_xticks([-1, -0.5, 0, 0.5, 1])
        cbar_ax.set_xticklabels(['-1.0', '-0.5', '0.0', '0.5', '1.0'],
                                fontsize=11, fontweight='bold')
        cbar_ax.tick_params(axis='x', which='both', length=6, width=2, direction='out',
                            bottom=True, top=False, labelbottom=True, labeltop=False)

        for spine in cbar_ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(2.5)
            spine.set_visible(True)

        fig.text(cbar_left + cbar_width / 2, cbar_bottom + cbar_height + 0.012,
                 f'{index_type} Value',
                 ha='center', va='bottom', fontsize=13, fontweight='bold',
                 transform=fig.transFigure, zorder=13)

    # SCALE BAR
    if show_scale:
        if 'transform' in profile:
            pixel_size_x = abs(profile['transform'][0])
            pixel_size_y = abs(profile['transform'][4])
            pixel_size = (pixel_size_x + pixel_size_y) / 2

            scale_length_m = 1000

            scale_bar_left = legend_left + 0.025
            scale_bar_bottom = legend_bottom + 0.03
            scale_bar_width = legend_width - 0.05
            scale_bar_height = 0.025

            black_seg = Rectangle((scale_bar_left, scale_bar_bottom),
                                  scale_bar_width / 2, scale_bar_height,
                                  transform=fig.transFigure,
                                  facecolor='black', edgecolor='black', linewidth=2, zorder=12)
            fig.patches.append(black_seg)

            white_seg = Rectangle((scale_bar_left + scale_bar_width / 2, scale_bar_bottom),
                                  scale_bar_width / 2, scale_bar_height,
                                  transform=fig.transFigure,
                                  facecolor='white', edgecolor='black', linewidth=2, zorder=12)
            fig.patches.append(white_seg)

            label_y = scale_bar_bottom - 0.01
            fig.text(scale_bar_left, label_y, '0',
                     ha='left', va='top', fontsize=11, fontweight='bold',
                     transform=fig.transFigure, zorder=13)
            fig.text(scale_bar_left + scale_bar_width / 2, label_y, f'{scale_length_m / 2:.0f}m',
                     ha='center', va='top', fontsize=11, fontweight='bold',
                     transform=fig.transFigure, zorder=13)
            fig.text(scale_bar_left + scale_bar_width, label_y, f'{scale_length_m / 1000:.1f} km',
                     ha='right', va='top', fontsize=11, fontweight='bold',
                     transform=fig.transFigure, zorder=13)

    # NORTH ARROW
    if show_north:
        north_x = 0.945
        north_y = 0.92
        north_size = 0.045

        north_ax = fig.add_axes([north_x, north_y, north_size, north_size * 1.5])

        arrow = FancyArrow(0.5, 0.1, 0, 0.7, width=0.3,
                           head_width=0.5, head_length=0.15,
                           facecolor='black', edgecolor='white', linewidth=3)
        north_ax.add_patch(arrow)

        north_ax.text(0.5, 0.95, 'N', ha='center', va='center',
                      fontsize=26, fontweight='bold', color='black',
                      bbox=dict(boxstyle='circle,pad=0.3', facecolor='white',
                                alpha=1.0, edgecolor='black', linewidth=2.5))

        north_ax.set_xlim(0, 1)
        north_ax.set_ylim(0, 1)
        north_ax.axis('off')

    # METADATA
    metadata_left = 0.72
    metadata_bottom = 0.01
    metadata_width = 0.27
    metadata_height = 0.08

    metadata_bg = Rectangle((metadata_left, metadata_bottom), metadata_width, metadata_height,
                            transform=fig.transFigure,
                            facecolor='white', alpha=1.0, edgecolor='black', linewidth=2, zorder=10)
    fig.patches.append(metadata_bg)

    crs_info = str(profile.get('crs', 'N/A'))
    if len(crs_info) > 40:
        crs_info = crs_info[:40] + '...'

    metadata_text = f'Source: Sentinel-2\nCRS: {crs_info}\nResolution: {abs(profile["transform"][0]):.1f}m'
    fig.text(metadata_left + metadata_width / 2, metadata_bottom + metadata_height / 2,
             metadata_text,
             ha='center', va='center', fontsize=10, style='italic',
             transform=fig.transFigure, zorder=11)

    st.pyplot(fig, use_container_width=True)

    st.markdown("---")

    return fig


def process_vector_analysis(uploaded_vector, index_array, profile, index_type):
    """Perform zonal statistics with vector data"""

    st.markdown("### 📐 Zonal Statistics")

    try:
        # Zapisz vector jako tekst (GeoJSON to JSON)
        temp_vector = tempfile.NamedTemporaryFile(delete=False, suffix='.geojson', mode='w', encoding='utf-8')
        # Dekoduj bytes do string
        vector_content = uploaded_vector.getvalue().decode('utf-8')
        temp_vector.write(vector_content)
        temp_vector.close()

        # Save index raster temporarily
        temp_raster = tempfile.NamedTemporaryFile(delete=False, suffix='.tif')
        temp_raster.close()

        profile.update(dtype=rasterio.float32, count=1)

        with rasterio.open(temp_raster.name, 'w', **profile) as dst:
            dst.write(index_array.astype(np.float32), 1)

        # Read vector data
        gdf = gpd.read_file(io.BytesIO(uploaded_vector.getvalue()))

        # Calculate zonal statistics
        with st.spinner("Calculating zonal statistics..."):
            stats = zonal_stats(
                gdf,
                temp_raster.name,
                stats=['mean', 'min', 'max', 'std', 'count'],
                geojson_out=True
            )

        stats_gdf = gpd.GeoDataFrame.from_features(stats)

        st.success(f"✅ Calculated statistics for {len(stats_gdf)} features")

        st.dataframe(stats_gdf.drop('geometry', axis=1), use_container_width=True, height=300)

        csv = stats_gdf.drop('geometry', axis=1).to_csv(index=False)
        st.download_button(
            label="📥 Download Zonal Statistics CSV",
            data=csv,
            file_name=f"{index_type}_zonal_stats.csv",
            mime="text/csv"
        )

        st.markdown("---")

        # Cleanup
        os.unlink(temp_vector.name)
        os.unlink(temp_raster.name)

    except Exception as e:
        st.error(f"Error in zonal statistics: {str(e)}")
        st.exception(e)


def create_interactive_map(index_array, profile, index_type, colormap, reverse_cmap):
    """Create interactive Folium map"""

    st.markdown("### 🗺️ Interactive Map")

    try:
        bounds = rasterio.transform.array_bounds(
            profile['height'],
            profile['width'],
            profile['transform']
        )

        center_lat = (bounds[1] + bounds[3]) / 2
        center_lon = (bounds[0] + bounds[2]) / 2

        # Create base map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=13,
            tiles='OpenStreetMap',
            prefer_canvas=True
        )

        # Add multiple tile layers - USUŃ STAMEN (nie działa bez API key)
        # Dodaj tylko działające tile layers z atrybutami

        folium.TileLayer(
            tiles='CartoDB positron',
            name='Light',
            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
        ).add_to(m)

        folium.TileLayer(
            tiles='CartoDB dark_matter',
            name='Dark',
            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
        ).add_to(m)

        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Satellite',
            overlay=False,
            control=True
        ).add_to(m)

        folium.TileLayer(
            tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
            attr='Google',
            name='Google Satellite',
            overlay=False,
            control=True
        ).add_to(m)

        # Add bounds rectangle
        folium.Rectangle(
            bounds=[[bounds[1], bounds[0]], [bounds[3], bounds[2]]],
            color='#FF0000',
            weight=4,
            fill=True,
            fillColor='#FF0000',
            fillOpacity=0.1,
            popup=f'{index_type} Coverage Area'
        ).add_to(m)

        # Add center marker
        folium.Marker(
            [center_lat, center_lon],
            popup=folium.Popup(f'<b>{index_type} Analysis Center</b>', max_width=200),
            tooltip=f'{index_type}',
            icon=folium.Icon(color='red', icon='map', prefix='fa')
        ).add_to(m)

        # Add corner markers
        folium.CircleMarker(
            [bounds[1], bounds[0]],
            radius=5,
            color='blue',
            fill=True,
            popup='SW Corner'
        ).add_to(m)

        folium.CircleMarker(
            [bounds[3], bounds[2]],
            radius=5,
            color='blue',
            fill=True,
            popup='NE Corner'
        ).add_to(m)

        # Add layer control
        folium.LayerControl(position='topright').add_to(m)

        # Display map
        map_data = st_folium(
            m,
            width=1400,
            height=700,
            returned_objects=[]
        )

        st.markdown("---")

    except Exception as e:
        st.warning(f"Could not create interactive map: {str(e)}")


def create_download_section(index_array, profile, index_type, fig):
    """Create download section for results"""

    st.markdown("### 💾 Download Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        try:
            temp_output = tempfile.NamedTemporaryFile(delete=False, suffix='.tif')
            temp_output.close()

            profile.update(dtype=rasterio.float32, count=1, compress='lzw')

            with rasterio.open(temp_output.name, 'w', **profile) as dst:
                dst.write(index_array.astype(np.float32), 1)

            with open(temp_output.name, 'rb') as f:
                st.download_button(
                    label="📥 Download GeoTIFF",
                    data=f.read(),
                    file_name=f"{index_type}_result.tif",
                    mime="image/tiff",
                    use_container_width=True
                )

            os.unlink(temp_output.name)
        except Exception as e:
            st.error(f"Error: {str(e)}")

    with col2:
        try:
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=300, bbox_inches='tight', facecolor='white', pad_inches=0)
            buf.seek(0)

            st.download_button(
                label="📥 Download PNG (High Quality)",
                data=buf,
                file_name=f"{index_type}_visualization_HQ.png",
                mime="image/png",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error: {str(e)}")

    with col3:
        try:
            valid_data = index_array[~np.isnan(index_array)]
            stats_text = f"""
{index_type} STATISTICS REPORT
{'=' * 60}

BASIC STATISTICS:
  Mean:              {np.mean(valid_data):.6f}
  Median:            {np.median(valid_data):.6f}
  Standard Deviation:{np.std(valid_data):.6f}
  Minimum:           {np.min(valid_data):.6f}
  Maximum:           {np.max(valid_data):.6f}
  Range:             {np.max(valid_data) - np.min(valid_data):.6f}

PERCENTILES:
  25th percentile:   {np.percentile(valid_data, 25):.6f}
  50th percentile:   {np.percentile(valid_data, 50):.6f}
  75th percentile:   {np.percentile(valid_data, 75):.6f}
  90th percentile:   {np.percentile(valid_data, 90):.6f}
  95th percentile:   {np.percentile(valid_data, 95):.6f}

DATA INFO:
  Total valid pixels:{valid_data.size:,}
  Array shape:       {index_array.shape}
  Data type:         {index_array.dtype}

Generated by CASSANDRA - Spatial Analysis Tool
Author: Jakub Mielcarek 2025
"""

            st.download_button(
                label="📥 Download Report (TXT)",
                data=stats_text,
                file_name=f"{index_type}_report.txt",
                mime="text/plain",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error: {str(e)}")
