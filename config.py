# config.py

# --- DATA SOURCES ---
EMISSIONS_DATA_SOURCE = "https://www.gov.uk/government/publications/greenhouse-gas-reporting-conversion-factors-2024"
SOURCE_NAME = "UK Gov (DEFRA) GHG Reporting Factors 2024"

# --- EMISSION FACTORS (kg CO2e / tonne-km) ---
# Source: UK Gov / DEFRA 2024
CO2_FACTORS = {
    "Iron Ore": 0.00253,   # Bulk carrier 200,000+ dwt
    "Soybean": 0.00304,    # Bulk carrier 100k-199k dwt
    "Crude Oil": 0.00320,  # Large Tanker (VLCC Estimate)
    "Coffee": 0.01265,     # Container ship 8000+ TEU
    "Beef": 0.01306        # Refrigerated cargo (Reefer)
}

# --- VESSEL MAPPING ---
PRODUCT_VESSEL_MAPPING = {
    "Iron Ore": "Bulk Carrier (200k+ dwt)",
    "Soybean": "Bulk Carrier (100k-199k dwt)",
    "Crude Oil": "Large Tanker (VLCC)",
    "Coffee": "Container Ship (8k+ TEU)",
    "Beef": "Refrigerated Cargo (Reefer)"
}

# --- COLORS (TROPICAL THEME) ---
# Darker, earthy tones that show up well on beige backgrounds
PRODUCT_COLORS = {
    "Iron Ore": "#D35400",   # Burnt Orange
    "Crude Oil": "#2E4053",  # Dark Slate
    "Beef": "#C0392B",       # Deep Red
    "Soybean": "#27AE60",    # Jungle Green
    "Coffee": "#6E2C00"      # Dark Brown
}

# --- MAP STYLES ---
MAP_STYLES = {
    "Tropical": {
        "landcolor": "#F9F7E8",     # Very Light Beige
        "countrycolor": "#A5D6A7",  # Pale Green Borders
        "oceancolor": "#E0F7FA",    # Light Cyan/Teal
        "bgcolor": "#E0F7FA"        # Light Cyan/Teal
    }
}

# --- GEOGRAPHIC DATA ---
ORIGINS = {
    "Tubarão Port (Vitoria)": [-40.24, -20.29],
    "Ponta da Madeira (São Luís)": [-44.38, -2.57],
    "Santos Port (São Paulo)": [-46.33, -24.00],
    "Paranaguá Port": [-48.50, -25.50],
    "Rio Grande Port": [-52.09, -32.03],
    "Port of Rio de Janeiro": [-43.18, -22.89],
    "Port of Açu (Rio)": [-40.99, -21.82]
}

PRODUCT_ORIGINS = {
    "Iron Ore": ["Tubarão Port (Vitoria)", "Ponta da Madeira (São Luís)"],
    "Crude Oil": ["Port of Açu (Rio)", "Port of Rio de Janeiro", "Santos Port (São Paulo)"],
    "Beef": ["Paranaguá Port", "Santos Port (São Paulo)", "Rio Grande Port"],
    "Soybean": ["Paranaguá Port", "Santos Port (São Paulo)", "Rio Grande Port", "Ponta da Madeira (São Luís)"],
    "Coffee": ["Santos Port (São Paulo)", "Port of Rio de Janeiro"]
}

DESTINATIONS = {
    "China (Qingdao Port)": [120.33, 36.06],
    "Malaysia (Teluk Rubiah)": [100.65, 4.19],
    "Oman (Sohar Port)": [56.63, 24.50],
    "Japan (Kimitsu/Tokyo)": [139.75, 35.61],
    "Bahrain (Khalifa Bin Salman)": [50.71, 26.20],
    "Spain (Algeciras/Valencia)": [-5.43, 36.14],
    "Thailand (Laem Chabang)": [100.90, 13.08],
    "Iran (Bandar Abbas)": [56.08, 27.13],
    "Netherlands (Rotterdam)": [4.40, 51.90],
    "China (Shanghai Port)": [121.47, 31.23],
    "USA (Houston - Oil)": [-95.36, 29.76],
    "Singapore Port": [103.84, 1.26],
    "Spain (Cartagena/Algeciras)": [-0.98, 37.60],
    "UAE (Jebel Ali)": [55.02, 25.00],
    "Philippines (Manila)": [120.96, 14.58],
    "Saudi Arabia (Jeddah)": [39.16, 21.48],
    "USA (New York/NJ - Gen)": [-74.00, 40.71],
    "Germany (Hamburg)": [9.97, 53.53],
    "Belgium (Antwerp)": [4.40, 51.22],
    "Italy (Genoa)": [8.92, 44.40]
}

PRODUCTS = ["Iron Ore", "Crude Oil", "Beef", "Soybean", "Coffee"]

EXPORT_VOLUMES = {
    "Iron Ore": { "China (Qingdao Port)": 279_000_000_000, "Malaysia (Teluk Rubiah)": 20_600_000_000, "Oman (Sohar Port)": 12_300_000_000, "Japan (Kimitsu/Tokyo)": 11_900_000_000, "Bahrain (Khalifa Bin Salman)": 10_200_000_000 },
    "Crude Oil": { "China (Shanghai Port)": 40_800_000_000, "USA (Houston - Oil)": 14_800_000_000, "Singapore Port": 10_000_000_000, "Spain (Cartagena/Algeciras)": 9_700_000_000, "Netherlands (Rotterdam)": 6_600_000_000 },
    "Beef": { "China (Shanghai Port)": 2_100_000_000, "UAE (Jebel Ali)": 601_000_000, "Philippines (Manila)": 579_000_000, "Japan (Kimitsu/Tokyo)": 530_000_000, "Saudi Arabia (Jeddah)": 428_000_000 },
    "Soybean": { "China (Qingdao Port)": 72_300_000_000, "Spain (Algeciras/Valencia)": 4_100_000_000, "Thailand (Laem Chabang)": 3_400_000_000, "Iran (Bandar Abbas)": 1_800_000_000, "Netherlands (Rotterdam)": 1_000_000_000 },
    "Coffee": { "USA (New York/NJ - Gen)": 467_000_000, "Germany (Hamburg)": 445_000_000, "Belgium (Antwerp)": 259_000_000, "Italy (Genoa)": 233_000_000, "Japan (Kimitsu/Tokyo)": 135_000_000 }
}

AVAILABLE_RESTRICTIONS = [
    'suez', 'panama', 'northwest', 'northeast', 'bering',
    'gibraltar', 'babelmandeb', 'malacca', 'sunda', 'ormuz'
]