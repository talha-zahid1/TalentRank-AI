from elasticsearch import Elasticsearch
from schemas.appschema import *
setting=Settings()
es = Elasticsearch(
    setting.Elastic_endpoint,
    api_key=setting.Elastic_apiKey
)
es.indices.create(index="resumes", ignore=400)


def add_into_es(doc):
    es.index(
        index="resumes",
        document=doc,
        id=f"{doc.get("file_id")}_{doc.get("job_id")}",
    )


def del_frm_es(file_id):
    es.delete_by_query(
        index="resumes",
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
    res = es.search(index="resumes", body=query)
    result = []
    for hit in res["hits"]["hits"]:
        result.append(hit["_source"])
    return result
