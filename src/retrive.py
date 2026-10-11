from os import environ
from db import runSql
from embeddings import embedQuery
from seed import titleFromPath

def retrive(query, limit=10):
    if not query or not query.strip():
        return []

    rows = runSql("""
        SELECT id, path, modality, embedding <=> %(query)s AS distance
        FROM documents
        WHERE embedding <=> %(query)s < %(maxDistance)s
        ORDER BY distance
        LIMIT %(limit)s
    """, {
        "query": embedQuery(query),
        "maxDistance": float(environ["SEARCH_MAX_DISTANCE"]),
        "limit": limit,
    })

    return [
        {
            "id": row_id,
            "file": path,
            "modality": modality,
            "title": titleFromPath(path),
            "distance": distance,
        }
        for row_id, path, modality, distance in rows
    ]
