def compose_queries(cache, office_tags):
    queries = []
    for key, value in cache.items():
        bbox = value.get("bbox")
        if not bbox or len(bbox) < 4:
            continue
        south, north, west, east = (
            float(bbox[0]),
            float(bbox[1]),
            float(bbox[2]),
            float(bbox[3]),
        )
        for tag in office_tags:
            q = f'[out:json][timeout:25];\nnode["office"="{tag}"]["website"]({south},{west},{north},{east});\nout body;'
            queries.append(q)
    return queries
