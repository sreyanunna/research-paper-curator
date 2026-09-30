from opensearchpy import OpenSearch

client = OpenSearch(hosts=["http://opensearch:9200"])

# PUT /arxiv-papers  (create index with your mapping)
client.indices.create(index="arxiv-papers", body=INDEX_MAPPING)

# PUT /arxiv-papers/_doc/2609.20820v1  (upsert one paper)
client.index(index="arxiv-papers", id="2609.20820v1", body=paper_dict)

# GET /arxiv-papers/_search
resp = client.search(index="arxiv-papers", body={"query": {...}})
hits = resp["hits"]["hits"]