from elasticsearch import Elasticsearch
from schemas.appschema import *

setting = Settings()
es = Elasticsearch(
    setting.Elastic_endpoint,
    api_key=setting.Elastic_apiKey
)

INDEX_NAME = "resumes"
_index_ready = False


def ensure_index():
    global _index_ready
    if _index_ready:
        return True
    try:
        es.indices.create(index=INDEX_NAME, ignore=400)
        _index_ready = True
        return True
    except Exception as e:
        print(f"Elasticsearch index create failed: {e}")
        return False


# startup pe try karo, fail ho to app crash na ho
ensure_index()


def add_into_es(doc):
    ensure_index()
    es.index(
        index=INDEX_NAME,
        document=doc,
        id=f"{doc.get('file_id')}_{doc.get('job_id')}",
    )


def del_frm_es(file_id):
    es.delete_by_query(
        index=INDEX_NAME,
        body={"query": {"term": {"file_id": file_id}}},
        refresh=True,
        wait_for_completion=True,
    )
    return True


def get_documents(job_id: int):
    query = {
        "query": {"term": {"job_id": job_id}},
        "sort": [{"matched_percentage": {"order": "desc"}}],
    }
    res = es.search(index=INDEX_NAME, body=query)
    result = []
    for hit in res["hits"]["hits"]:
        result.append(hit["_source"])
    return result