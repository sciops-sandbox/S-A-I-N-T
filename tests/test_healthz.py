def test_healthz():
    import importlib
    rag_api = importlib.import_module('rag_api')
    app = rag_api.app
    c = app.test_client()
    r = c.get('/healthz')
    assert r.status_code == 200
    assert 'status' in r.get_json()
