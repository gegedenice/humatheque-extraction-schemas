# humatheque-extraction-schemas

Pivot JSON Schemas of the VLM title-page extraction, and a small FastAPI service
that serves them. They describe the POST body of the downstream APIs
(alma-checker, sudoc-checker, idref-linker), which fetch them from here instead of
each exposing its own copy.

| Kind | File |
|------|------|
| `thesis` | [`schemas/thesis.schema.json`](schemas/thesis.schema.json) |
| `dissertation` | [`schemas/dissertation.schema.json`](schemas/dissertation.schema.json) (master's mémoires, HDR) |

## API

| Route | Returns |
|-------|---------|
| `GET /schemas` | Available kinds, titles and `$id` |
| `GET /schemas/{kind}` | The JSON Schema (`/schemas/{kind}.schema.json` also works) |
| `GET /health` | `{"ok": true}` |

A client fetching `{base}/{kind}.schema.json` works unchanged against either base:

- `https://<this-service>/schemas`
- `https://raw.githubusercontent.com/gegedenice/humatheque-extraction-schemas/main/schemas`
  (replace `main` with a tag to pin a version)

## Run

```bash
pip install -r requirements.txt
uvicorn app:app --port 8000
# or
docker build -t humatheque-extraction-schemas . && docker run -p 8000:8000 humatheque-extraction-schemas
```

Test: `pip install pytest httpx && pytest -q`.
