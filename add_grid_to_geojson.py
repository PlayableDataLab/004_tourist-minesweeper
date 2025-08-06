import json

# Load GeoJSON
with open("MALLORCA_airbnb2.geojson", "r", encoding="utf-8") as f:
    data = json.load(f)

features = data["features"]

# Collect unique X (left) and Y (top) values
x_vals = sorted(set(round(feat['properties']['left'], 5) for feat in features))
y_vals = sorted(set(round(feat['properties']['top'], 5) for feat in features), reverse=True)

# Map to grid indices
x_map = {x: i for i, x in enumerate(x_vals)}
y_map = {y: i for i, y in enumerate(y_vals)}

# Assign row/col to each feature
for feat in features:
    x = round(feat['properties']['left'], 5)
    y = round(feat['properties']['top'], 5)
    feat['properties']['col'] = x_map[x]
    feat['properties']['row'] = y_map[y]

# Save new GeoJSON
with open("MALLORCA_airbnb_grid2.geojson", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Done! File saved as MALLORCA_airbnb_grid2.geojson")
