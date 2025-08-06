import json

INPUT = 'MALLORCA_final2.geojson'
OUTPUT = 'MALLORCA_final2_with_grid.geojson'

# Load GeoJSON
with open(INPUT, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Calculate centroid for each feature
for feat in data['features']:
    coords = feat['geometry']['coordinates'][0]
    xs = [pt[0] for pt in coords]
    ys = [pt[1] for pt in coords]
    feat['centroid'] = (sum(xs) / len(xs), sum(ys) / len(ys))

# Sort by Y descending (top to bottom), then X ascending (left to right)
features = data['features']
features.sort(key=lambda f: (-f['centroid'][1], f['centroid'][0]))

# Determine unique rows by unique y (to handle "ragged" grids)
ys = sorted(set(round(f['centroid'][1], 6) for f in features), reverse=True)
y_to_row = {y: i for i, y in enumerate(ys)}

# Assign row and column for each cell
for feat in features:
    y = round(feat['centroid'][1], 6)
    row = y_to_row[y]
    row_feats = [f for f in features if round(f['centroid'][1], 6) == y]
    xs = sorted([f['centroid'][0] for f in row_feats])
    x_to_col = {x: i for i, x in enumerate(xs)}
    col = x_to_col[feat['centroid'][0]]
    feat['properties']['row'] = row
    feat['properties']['col'] = col

# Remove centroid property
for feat in features:
    feat.pop('centroid', None)

# Save to new file
data['features'] = features
with open(OUTPUT, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Done! Saved as {OUTPUT}")
