# Configuration constants for the Global Logistics Planner

# Authentic CO2 Multiplier (IMO 2020 Study)
CO2_FACTORS = {
    "Iron Ore": 0.0025,
    "Crude Oil": 0.0032,
    "Beef": 0.0085,
    "Soybean": 0.0043,
    "Coffee": 0.0075
}

# STRICT COLOR PALETTE (Technical/High-Contrast)
PRODUCT_COLORS = {
    "Iron Ore": "#ff4b4b",   # Radar Red
    "Crude Oil": "#94a3b8",  # Steel Grey
    "Beef": "#f59e0b",       # Amber Warning
    "Soybean": "#10b981",    # Matrix Green
    "Coffee": "#d97706"      # Bronze
}

# Ports
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

# Top Destinations
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
    "Iron Ore": {
        "China (Qingdao Port)": 279_000_000_000,
        "Malaysia (Teluk Rubiah)": 20_600_000_000,
        "Oman (Sohar Port)": 12_300_000_000,
        "Japan (Kimitsu/Tokyo)": 11_900_000_000,
        "Bahrain (Khalifa Bin Salman)": 10_200_000_000
    },
    "Crude Oil": {
        "China (Shanghai Port)": 40_800_000_000,
        "USA (Houston - Oil)": 14_800_000_000,
        "Singapore Port": 10_000_000_000,
        "Spain (Cartagena/Algeciras)": 9_700_000_000,
        "Netherlands (Rotterdam)": 6_600_000_000
    },
    "Beef": {
        "China (Shanghai Port)": 2_100_000_000,
        "UAE (Jebel Ali)": 601_000_000,
        "Philippines (Manila)": 579_000_000,
        "Japan (Kimitsu/Tokyo)": 530_000_000,
        "Saudi Arabia (Jeddah)": 428_000_000
    },
    "Soybean": {
        "China (Qingdao Port)": 72_300_000_000,
        "Spain (Algeciras/Valencia)": 4_100_000_000,
        "Thailand (Laem Chabang)": 3_400_000_000,
        "Iran (Bandar Abbas)": 1_800_000_000,
        "Netherlands (Rotterdam)": 1_000_000_000
    },
    "Coffee": {
        "USA (New York/NJ - Gen)": 467_000_000,
        "Germany (Hamburg)": 445_000_000,
        "Belgium (Antwerp)": 259_000_000,
        "Italy (Genoa)": 233_000_000,
        "Japan (Kimitsu/Tokyo)": 135_000_000
    }
}

MAP_STYLES = {
    "Dark": {
        "landcolor": "#0f172a",
        "countrycolor": "#1e293b",
        "oceancolor": "#020617",
        "bgcolor": "#020617"
    }
}

AVAILABLE_RESTRICTIONS = [
    'suez', 'panama', 'northwest', 'northeast', 'bering',
    'gibraltar', 'babalmandab', 'malacca', 'sunda', 'ormuz'
]