import json

# Load your geojson file
with open('MALLORCA_final.geojson', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Calculate centroids and create list of features
features = []
for feat in data['features']:
    # Assume Polygon and flat grid
    coords = feat['geometry']['coordinates'][0]
    xs = [pt[0] for pt in coords]
    ys = [pt[1] for pt in coords]
    centroid = (sum(xs) / len(xs), sum(ys) / len(ys))
    feat['centroid'] = centroid
    features.append(feat)

# Sort features: top to bottom (y), then left to right (x)
features.sort(key=lambda f: (-f['centroid'][1], f['centroid'][0]))

# Figure out number of columns (by unique y values)
ys = sorted(set(round(f['centroid'][1], 6) for f in features), reverse=True)
y_to_row = {y: i for i, y in enumerate(ys)}

# For each row, assign columns
for feat in features:
    y = round(feat['centroid'][1], 6)
    row = y_to_row[y]
    # Find all cells in this row
    row_feats = [f for f in features if round(f['centroid'][1], 6) == y]
    xs = sorted([f['centroid'][0] for f in row_feats])
    x_to_col = {x: i for i, x in enumerate(xs)}
    col = x_to_col[feat['centroid'][0]]
    feat['properties']['row'] = row
    feat['properties']['col'] = col

# Remove centroids
for feat in features:
    feat.pop('centroid', None)

# Save to new GeoJSON
data['features'] = features
with open('MALLORCA_final_with_grid.geojson', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Done! Your file is now 'MALLORCA_final_with_grid.geojson'")
