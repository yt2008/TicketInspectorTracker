# TicketInspectorTracker

REST API for reporting and retrieving real-time ticket inspector sightings on public transport.

## Run

```bash
python -m ticket_inspector_tracker
```

Server listens on `127.0.0.1:8080`.

## Endpoints

- `POST /sightings`  
  JSON body:
  - `line` (required, string)
  - `stop` (required, string)
  - `direction` (optional, string)
  - `inspector_count` (optional, integer, default `1`)
- `GET /sightings`  
  Optional query parameter: `line` to filter by transport line.
