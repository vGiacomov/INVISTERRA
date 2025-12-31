import streamlit as st


def render():
    # CSS dla obramowań expanderów i formuł
    st.markdown("""
    <style>
        /* Obramowanie dla WSZYSTKICH expanderów (zwinięte i rozwinięte) */
        div[data-testid="stExpander"] {
            border: 2px solid #999 !important;
            border-radius: 8px !important;
            margin-bottom: 0.8rem !important;
            background-color: #ffffff !important;
        }

        /* Nagłówek expandera */
        div[data-testid="stExpander"] summary {
            background-color: #f5f5f5 !important;
            padding: 0.8rem !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
        }

        /* Treść expandera po rozwinięciu */
        div[data-testid="stExpander"] > div[role="region"] {
            padding: 0 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1>Spectral Indices Reference</h1>
        <p style="font-size: 1.1rem; opacity: 0.8;">
            Understanding satellite-derived indices for Earth observation
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Vegetation Indices
    st.markdown("## 🌿 Vegetation Indices")

    indices_vegetation = [
        {
            "name": "NDVI - Normalized Difference Vegetation Index",
            "formula": "(NIR - Red) / (NIR + Red) = (B8 - B4) / (B8 + B4)",
            "range": "-1 to +1",
            "description": "Measures vegetation health and density. Values above 0.2 indicate vegetation presence, higher values indicate healthier, denser vegetation.",
            "use_cases": "Agriculture monitoring, forest health assessment, biomass estimation"
        },
        {
            "name": "EVI - Enhanced Vegetation Index",
            "formula": "2.5 × ((NIR - Red) / (NIR + 6×Red - 7.5×Blue + 1))",
            "range": "-1 to +1",
            "description": "Improved version of NDVI that reduces atmospheric and soil background effects. More sensitive in high biomass regions.",
            "use_cases": "Dense vegetation monitoring, tropical forest analysis"
        },
        {
            "name": "SAVI - Soil Adjusted Vegetation Index",
            "formula": "((NIR - Red) / (NIR + Red + L)) × (1 + L), where L=0.5",
            "range": "-1 to +1",
            "description": "Minimizes soil brightness influences when vegetation cover is low.",
            "use_cases": "Sparse vegetation areas, early crop growth stages"
        },
        {
            "name": "GNDVI - Green Normalized Difference Vegetation Index",
            "formula": "(NIR - Green) / (NIR + Green) = (B8 - B3) / (B8 + B3)",
            "range": "-1 to +1",
            "description": "More sensitive to chlorophyll concentration than NDVI. Better for mid to late-season crop assessment.",
            "use_cases": "Chlorophyll content estimation, nitrogen stress detection"
        },
        {
            "name": "NDRE - Normalized Difference Red Edge",
            "formula": "(NIR - RedEdge) / (NIR + RedEdge) = (B8 - B5) / (B8 + B5)",
            "range": "-1 to +1",
            "description": "Sensitive to chlorophyll content variations. Less sensitive to atmospheric effects.",
            "use_cases": "Precision agriculture, crop health monitoring, fertilizer optimization"
        }
    ]

    for idx in indices_vegetation:
        with st.expander(f"**{idx['name']}**"):
            st.markdown(f"""
            <div style="padding: 1rem;">
                <div style="background-color: #2c3e50; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;">
                    <strong style="color: #ecf0f1;">Formula:</strong><br>
                    <span style="font-size: 1.15rem; color: #ffffff; font-family: 'Courier New', monospace;">{idx['formula']}</span>
                </div>
                <p><strong>Value Range:</strong> {idx['range']}</p>
                <p><strong>Description:</strong> {idx['description']}</p>
                <p style="margin-bottom: 0;"><strong>Use Cases:</strong> {idx['use_cases']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Water Indices
    st.markdown("## 💧 Water Indices")

    indices_water = [
        {
            "name": "NDWI - Normalized Difference Water Index",
            "formula": "(Green - NIR) / (Green + NIR) = (B3 - B8) / (B3 + B8)",
            "range": "-1 to +1",
            "description": "Detects water bodies and measures water content in vegetation. Positive values indicate water presence.",
            "use_cases": "Water body mapping, flood monitoring, irrigation assessment"
        },
        {
            "name": "MNDWI - Modified Normalized Difference Water Index",
            "formula": "(Green - SWIR) / (Green + SWIR) = (B3 - B11) / (B3 + B11)",
            "range": "-1 to +1",
            "description": "Better separates water from built-up areas compared to NDWI. Suppresses urban noise.",
            "use_cases": "Urban water body detection, coastal monitoring"
        },
        {
            "name": "NDMI - Normalized Difference Moisture Index",
            "formula": "(NIR - SWIR1) / (NIR + SWIR1) = (B8 - B11) / (B8 + B11)",
            "range": "-1 to +1",
            "description": "Sensitive to moisture content in vegetation and soil. High values indicate high moisture content.",
            "use_cases": "Drought monitoring, irrigation management, fire risk assessment"
        }
    ]

    for idx in indices_water:
        with st.expander(f"**{idx['name']}**"):
            st.markdown(f"""
            <div style="padding: 1rem;">
                <div style="background-color: #2c3e50; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;">
                    <strong style="color: #ecf0f1;">Formula:</strong><br>
                    <span style="font-size: 1.15rem; color: #ffffff; font-family: 'Courier New', monospace;">{idx['formula']}</span>
                </div>
                <p><strong>Value Range:</strong> {idx['range']}</p>
                <p><strong>Description:</strong> {idx['description']}</p>
                <p style="margin-bottom: 0;"><strong>Use Cases:</strong> {idx['use_cases']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Urban and Soil Indices
    st.markdown("## 🏙️ Urban & Soil Indices")

    indices_urban = [
        {
            "name": "NDBI - Normalized Difference Built-up Index",
            "formula": "(SWIR - NIR) / (SWIR + NIR) = (B11 - B8) / (B11 + B8)",
            "range": "-1 to +1",
            "description": "Identifies built-up and urban areas. Positive values indicate urban/built-up land.",
            "use_cases": "Urban expansion monitoring, city planning, land use classification"
        },
        {
            "name": "BSI - Bare Soil Index",
            "formula": "((SWIR + Red) - (NIR + Blue)) / ((SWIR + Red) + (NIR + Blue))",
            "range": "-1 to +1",
            "description": "Detects bare soil and sparse vegetation areas.",
            "use_cases": "Soil erosion assessment, construction site monitoring"
        },
        {
            "name": "UI - Urban Index",
            "formula": "(SWIR2 - NIR) / (SWIR2 + NIR) = (B12 - B8) / (B12 + B8)",
            "range": "-1 to +1",
            "description": "Alternative urban detection index. Higher values indicate urban areas.",
            "use_cases": "Urban area extraction, impervious surface mapping"
        }
    ]

    for idx in indices_urban:
        with st.expander(f"**{idx['name']}**"):
            st.markdown(f"""
            <div style="padding: 1rem;">
                <div style="background-color: #2c3e50; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;">
                    <strong style="color: #ecf0f1;">Formula:</strong><br>
                    <span style="font-size: 1.15rem; color: #ffffff; font-family: 'Courier New', monospace;">{idx['formula']}</span>
                </div>
                <p><strong>Value Range:</strong> {idx['range']}</p>
                <p><strong>Description:</strong> {idx['description']}</p>
                <p style="margin-bottom: 0;"><strong>Use Cases:</strong> {idx['use_cases']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Fire and Burn Indices
    st.markdown("## 🔥 Fire & Burn Indices")

    indices_fire = [
        {
            "name": "NBR - Normalized Burn Ratio",
            "formula": "(NIR - SWIR) / (NIR + SWIR) = (B8 - B12) / (B8 + B12)",
            "range": "-1 to +1",
            "description": "Identifies burned areas and assesses burn severity. Healthy vegetation has high NBR values.",
            "use_cases": "Post-fire damage assessment, burn severity mapping"
        },
        {
            "name": "BAIS2 - Burned Area Index for Sentinel-2",
            "formula": "(1 - ((B6 × B7 × B8A) / B4)^0.5) × ((B12 - B8A) / (B12 + B8A)^0.5 + 1)",
            "range": "Variable",
            "description": "Specifically designed for Sentinel-2 to detect burned areas with high accuracy.",
            "use_cases": "Rapid fire damage mapping, burned area detection"
        },
        {
            "name": "NBR2 - Normalized Burn Ratio 2",
            "formula": "(SWIR1 - SWIR2) / (SWIR1 + SWIR2) = (B11 - B12) / (B11 + B12)",
            "range": "-1 to +1",
            "description": "Alternative burn index using two SWIR bands. Useful for water content in burned areas.",
            "use_cases": "Burn severity assessment, post-fire recovery monitoring"
        }
    ]

    for idx in indices_fire:
        with st.expander(f"**{idx['name']}**"):
            st.markdown(f"""
            <div style="padding: 1rem;">
                <div style="background-color: #2c3e50; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;">
                    <strong style="color: #ecf0f1;">Formula:</strong><br>
                    <span style="font-size: 1.15rem; color: #ffffff; font-family: 'Courier New', monospace;">{idx['formula']}</span>
                </div>
                <p><strong>Value Range:</strong> {idx['range']}</p>
                <p><strong>Description:</strong> {idx['description']}</p>
                <p style="margin-bottom: 0;"><strong>Use Cases:</strong> {idx['use_cases']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Snow and Ice Indices
    st.markdown("## ❄️ Snow & Ice Indices")

    indices_snow = [
        {
            "name": "NDSI - Normalized Difference Snow Index",
            "formula": "(Green - SWIR1) / (Green + SWIR1) = (B3 - B11) / (B3 + B11)",
            "range": "-1 to +1",
            "description": "Identifies snow and ice cover. Values > 0.4 typically indicate snow presence.",
            "use_cases": "Snow cover mapping, glacier monitoring, avalanche risk assessment"
        },
        {
            "name": "S2WI - Sentinel-2 Water and Ice Index",
            "formula": "(NIR - SWIR2) / (NIR + SWIR2) = (B8 - B12) / (B8 + B12)",
            "range": "-1 to +1",
            "description": "Distinguishes between water, ice, and snow. Positive values indicate water/ice.",
            "use_cases": "Cryosphere monitoring, lake ice detection"
        }
    ]

    for idx in indices_snow:
        with st.expander(f"**{idx['name']}**"):
            st.markdown(f"""
            <div style="padding: 1rem;">
                <div style="background-color: #2c3e50; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;">
                    <strong style="color: #ecf0f1;">Formula:</strong><br>
                    <span style="font-size: 1.15rem; color: #ffffff; font-family: 'Courier New', monospace;">{idx['formula']}</span>
                </div>
                <p><strong>Value Range:</strong> {idx['range']}</p>
                <p><strong>Description:</strong> {idx['description']}</p>
                <p style="margin-bottom: 0;"><strong>Use Cases:</strong> {idx['use_cases']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Sentinel-2 Band Reference
    st.markdown("## 🛰️ Sentinel-2 Band Reference")

    st.markdown("""
    <div style="display: flex; justify-content: center; margin: 2rem 0;">
        <table style="border-collapse: collapse; width: 90%; max-width: 1200px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <thead>
                <tr style="background-color: #2c3e50; color: #ffffff;">
                    <th style="border: 1px solid #ddd; padding: 12px; text-align: left;">Band</th>
                    <th style="border: 1px solid #ddd; padding: 12px; text-align: left;">Name</th>
                    <th style="border: 1px solid #ddd; padding: 12px; text-align: center;">Wavelength (nm)</th>
                    <th style="border: 1px solid #ddd; padding: 12px; text-align: center;">Resolution (m)</th>
                    <th style="border: 1px solid #ddd; padding: 12px; text-align: left;">Common Use</th>
                </tr>
            </thead>
            <tbody>
                <tr style="background-color: #f9f9f9;">
                    <td style="border: 1px solid #ddd; padding: 10px; font-weight: 600;">B1</td>
                    <td style="border: 1px solid #ddd; padding: 10px;">Coastal aerosol</td>
                    <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">443</td>
                    <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">60</td>
                    <td style="border: 1px solid #ddd; padding: 10px;">Atmospheric correction</td>
                </tr>
                <tr style="background-color: #ffffff;">
                    <td style="border: 1px solid #ddd; padding: 10px; font-weight: 600;">B2</td>
                    <td style="border: 1px solid #ddd; padding: 10px;">Blue</td>
                    <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">490</td>
                    <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">10</td>
                    <td style="border: 1px solid #ddd; padding: 10px;">True color composites</td>
                </tr>
                <tr style="background-color: #f9f9f9;">
                    <td style="border: 1px solid #ddd; padding: 10px; font-weight: 600;">B3</td>
                    <td style="border: 1px solid #ddd; padding: 10px;">Green</td>
                    <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">560</td>
                    <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">10</td>
                    <td style="border: 1px solid #ddd; padding: 10px;">True color composites</td>
                </tr>
                <tr style="background-color: #ffffff;">
                    <td style="border: 1px solid #ddd; padding: 10px; font-weight: 600;">B4</td>
                    <td style="border: 1px solid #ddd; padding: 10px;">Red</td>
                    <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">665</td>
                    <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">10</td>
                    <td style="border: 1px solid #ddd; padding: 10px;">Vegetation, true color</td>
                </tr>
                <tr style="background-color: #f9f9f9;">
                    <td style="border: 1px solid #ddd; padding: 10px; font-weight: 600;">B5</td>
                    <td style="border: 1px solid #ddd; padding: 10px;">Red Edge 1</td>
                    <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">705</td>
                    <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">20</td>
                    <td style="border: 1px solid #ddd; padding: 10px;">Vegetation classification</td>
                </tr>
                <tr style="background-color: #ffffff;">
                    <td style="border: 1px solid #ddd; padding: 10px; font-weight: 600;">B6</td>
                    <td style="border: 1px solid #ddd; padding: 10px;">Red Edge 2</td>
                    <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">740</td>
                    <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">20</td>
                    <td style="border: 1px solid #ddd; padding: 10px;">Vegetation classification</td>
                </tr>
                <tr style="background-color: #f9f9f9;">
                    <td style="border: 1px solid #ddd; padding: 10px; font-weight: 600;">B7</td>
                    <td style="border: 1px solid #ddd; padding: 10px;">Red Edge 3</td>
                    <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">783</td>
                    <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">20</td>
                    <td style="border: 1px solid #ddd; padding: 10px;">Vegetation classification</td>
                </tr>
                <tr style="background-color: #ffffff;">
                    <td style="border: 1px solid #ddd; padding: 10px; font-weight: 600;">B8</td>
                    <td style="border: 1px solid #ddd; padding: 10px;">NIR</td>
                    <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">842</td>
                    <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">10</td>
                    <td style="border: 1px solid #ddd; padding: 10px;">Vegetation indices</td>
                </tr>
                <tr style="background-color: #f9f9f9;">
                    <td style="border: 1px solid #ddd; padding: 10px; font-weight: 600;">B8A</td>
                    <td style="border: 1px solid #ddd; padding: 10px;">NIR narrow</td>
                    <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">865</td>
                    <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">20</td>
                    <td style="border: 1px solid #ddd; padding: 10px;">Vegetation analysis</td>
                </tr>
                <tr style="background-color: #ffffff;">
                    <td style="border: 1px solid #ddd; padding: 10px; font-weight: 600;">B9</td>
                    <td style="border: 1px solid #ddd; padding: 10px;">Water vapor</td>
                    <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">945</td>
                    <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">60</td>
                    <td style="border: 1px solid #ddd; padding: 10px;">Atmospheric correction</td>
                </tr>
                <tr style="background-color: #f9f9f9;">
                    <td style="border: 1px solid #ddd; padding: 10px; font-weight: 600;">B10</td>
                    <td style="border: 1px solid #ddd; padding: 10px;">SWIR - Cirrus</td>
                    <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">1375</td>
                    <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">60</td>
                    <td style="border: 1px solid #ddd; padding: 10px;">Cloud detection</td>
                </tr>
                <tr style="background-color: #ffffff;">
                    <td style="border: 1px solid #ddd; padding: 10px; font-weight: 600;">B11</td>
                    <td style="border: 1px solid #ddd; padding: 10px;">SWIR 1</td>
                    <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">1610</td>
                    <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">20</td>
                    <td style="border: 1px solid #ddd; padding: 10px;">Moisture, snow/ice</td>
                </tr>
                <tr style="background-color: #f9f9f9;">
                    <td style="border: 1px solid #ddd; padding: 10px; font-weight: 600;">B12</td>
                    <td style="border: 1px solid #ddd; padding: 10px;">SWIR 2</td>
                    <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">2190</td>
                    <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">20</td>
                    <td style="border: 1px solid #ddd; padding: 10px;">Moisture, geology</td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

