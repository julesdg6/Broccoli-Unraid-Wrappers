# Broccoli-Unraid-Wrappers

A collection of Unraid 7 Docker templates (wrappers) for self-hosted apps.

## Install a template on Unraid 7 with `curl`

1. SSH into your Unraid server.
2. Download a template into your user templates folder:

**broccoli_github-mcp-server:**
```bash
curl -fsSL -o /boot/config/plugins/dockerMan/templates-user/broccoli_github-mcp-server.xml \
  https://raw.githubusercontent.com/julesdg6/Broccoli-Unraid-Wrappers/main/templates/broccoli_github-mcp-server.xml
```

**broccoli_mcp-google-map:**
```bash
curl -fsSL -o /boot/config/plugins/dockerMan/templates-user/broccoli_mcp-google-map.xml \
  https://raw.githubusercontent.com/julesdg6/Broccoli-Unraid-Wrappers/main/templates/broccoli_mcp-google-map.xml
```

**broccoli_open-notebook:**
```bash
curl -fsSL -o /boot/config/plugins/dockerMan/templates-user/broccoli_open-notebook.xml \
  https://raw.githubusercontent.com/julesdg6/Broccoli-Unraid-Wrappers/main/templates/broccoli_open-notebook.xml
```

**broccoli_surrealdb:**
```bash
curl -fsSL -o /boot/config/plugins/dockerMan/templates-user/broccoli_surrealdb.xml \
  https://raw.githubusercontent.com/julesdg6/Broccoli-Unraid-Wrappers/main/templates/broccoli_surrealdb.xml
```

3. In the Unraid web UI, go to **Docker** → **Add Container**.
4. In the template dropdown, select the desired template, then review/save.
5. Before starting the container, set required values:

   **broccoli_github-mcp-server:**
   - `GITHUB_PERSONAL_ACCESS_TOKEN`: optional but recommended for higher API limits and private repo access
   - After the container starts, point your MCP client to `http://<unraid-ip>:8082/mcp`

   **broccoli_mcp-google-map:**
   - `GOOGLE_MAPS_API_KEY`: your Google Maps API key from [Google Cloud Console](https://console.cloud.google.com)
   - Enable **Places API (New)** and **Routes API** in your Google Cloud project before use
   - After the container starts, point your MCP client to `http://<unraid-ip>:3020/mcp`

   **broccoli_open-notebook:**
   - Depends on `broccoli_surrealdb` (or another reachable SurrealDB instance) running with matching credentials
   - Uses upstream `lfnovo/open_notebook:v1-latest` (recommended deployment path)
   - `OPEN_NOTEBOOK_ENCRYPTION_KEY`: a unique, cryptographically random secret (recommended 32+ characters)
   - Keep `OPEN_NOTEBOOK_ENCRYPTION_KEY` unchanged after first deploy; rotating or losing it makes saved provider credentials unreadable
   - `SURREAL_PASSWORD`: must match your SurrealDB service password (use a strong, unique password)
   - `SURREAL_URL`: use `ws://surrealdb:8000/rpc` only when both containers are on a user-defined Docker network with working container DNS; if not on a user-defined network (default bridge mode), use `ws://<unraid-ip>:8000/rpc`
   - Optional but useful advanced variables in the template: `API_URL`, `OPEN_NOTEBOOK_PASSWORD`, `OPEN_NOTEBOOK_EMBEDDING_BATCH_SIZE`, `SURREAL_COMMANDS_MAX_TASKS`, `CORS_ORIGINS`
   - Example key generation: `openssl rand -base64 32`

   **broccoli_surrealdb:**
   - `SURREAL_PASS`: required root password (must match `broccoli_open-notebook` `SURREAL_PASSWORD`)
   - `SURREAL_USER`: defaults to `root`
   - `SURREAL_PATH`: defaults to `surrealkv:///data/surreal.db` — data is written inside the container's `/data` directory which is mapped to `/mnt/user/appdata/broccoli_surrealdb` on the host. Change this only if you need a different storage path or engine (`rocksdb://` is also supported). **Do not use the `file://` scheme** — it is no longer supported and will cause the container to exit immediately.
   - **Before starting the container for the first time**, prepare the data directory on the Unraid host (SurrealDB runs as UID 65532 / `nonroot` and needs write access):
     ```bash
     mkdir -p /mnt/user/appdata/broccoli_surrealdb
     chown -R 65532:65532 /mnt/user/appdata/broccoli_surrealdb
     ```

## `broccoli_open-notebook` deployment, upgrade, and recovery guide

### Fresh installation (supported workflow, no direct DB/API edits)

1. Deploy and start `broccoli_surrealdb`.
2. Deploy and start `broccoli_open-notebook` with:
   - `/app/data` mapped to persistent storage
   - a fixed `OPEN_NOTEBOOK_ENCRYPTION_KEY`
   - `SURREAL_*` values matching your SurrealDB service
3. Open `http://<unraid-ip>:8502`.
4. In Open Notebook UI: **Settings → API Keys**:
   - **Add Credential**
   - **Test Connection**
   - **Discover Models**
   - **Register Models**
5. In **Settings → Models**, choose defaults for:
   - chat / language model
   - embedding model

If no providers/models are configured yet, this UI workflow is the supported bootstrap path.

### Provider onboarding quick paths

- **Cloud provider (OpenAI/Anthropic/Groq/etc.)**: add credential key in **Settings → API Keys**, then discover/register.
- **Local Ollama**: add an **Ollama** credential in **Settings → API Keys** (for dockerized Ollama usually `http://ollama:11434`, for host-based Ollama often `http://host.docker.internal:11434`), then discover/register.
- **OpenAI-compatible backends (LM Studio, vLLM, etc.)**: add **OpenAI-Compatible** credential with the provider base URL, then discover/register.

### Persistent configuration expectations

To make configuration survive container recreation, image updates, stack redeployments, and template reloads:

- Keep `/app/data` on persistent storage (`/mnt/user/appdata/broccoli_open-notebook` by default).
- Keep `OPEN_NOTEBOOK_ENCRYPTION_KEY` stable for the life of the deployment.
- Keep SurrealDB data persistent (`/mnt/user/appdata/broccoli_surrealdb` by default).
- Back up both Open Notebook and SurrealDB appdata before major changes.

### Backup and restore

Stop both containers before backup for a clean snapshot.

```bash
docker stop broccoli_open-notebook broccoli_surrealdb
tar -czf /mnt/user/backups/open-notebook-$(date +%F).tgz \
  /mnt/user/appdata/broccoli_open-notebook \
  /mnt/user/appdata/broccoli_surrealdb
docker start broccoli_surrealdb broccoli_open-notebook
```

Restore by stopping containers, extracting both folders back to the same paths, and starting containers again.

### Upgrade and migration procedure

1. Back up appdata for both containers.
2. Update template(s) from this repository.
3. Confirm Open Notebook uses `lfnovo/open_notebook:v1-latest`.
4. Recreate containers while preserving mapped appdata paths and existing `OPEN_NOTEBOOK_ENCRYPTION_KEY`.
5. Validate:
   - `curl http://<unraid-ip>:5055/health`
   - login to UI and verify credentials/models are still present
6. If migrating from older env-based provider configs, use **Settings → API Keys → Migrate to Database**, then re-test/discover/register models.

### Troubleshooting and recovery

Health and startup checks:

```bash
docker logs --tail=200 broccoli_open-notebook
curl -sS http://<unraid-ip>:5055/health
docker exec broccoli_open-notebook sh -lc 'command -v curl || command -v wget || echo "No HTTP client in image"'
```

Common recovery actions:

- **No models available**: run the provider onboarding flow again in **Settings → API Keys**, then set defaults in **Settings → Models**.
- **Credential decrypt errors after update**: restore previous `OPEN_NOTEBOOK_ENCRYPTION_KEY` and restart.
- **Database auth/connection errors**: verify `SURREAL_URL`, `SURREAL_USER`, `SURREAL_PASSWORD`, and SurrealDB container health.
- **Slow/failing embeddings on local setups**: lower `OPEN_NOTEBOOK_EMBEDDING_BATCH_SIZE` (for example `8`) and restart.

## `broccoli_surrealdb` deployment notes

### First-run: directory permissions

SurrealDB runs as a non-root user (`nonroot`, UID 65532) inside the container. The mapped host directory must be writable by that user **before** the container starts for the first time, or you will see:

```
ERROR: There was a problem with the datastore: IO error: Permission denied (os error 13)
```

Run the following commands on your Unraid host (via SSH or the Unraid terminal) **before** clicking Start in the Docker UI:

```bash
mkdir -p /mnt/user/appdata/broccoli_surrealdb
chown -R 65532:65532 /mnt/user/appdata/broccoli_surrealdb
```

If you are unsure of your host user setup or need a quick fix, the following is an alternative (less restrictive) option:

```bash
mkdir -p /mnt/user/appdata/broccoli_surrealdb
chmod -R 777 /mnt/user/appdata/broccoli_surrealdb
```

### Storage configuration

SurrealDB persists data at the path specified by `SURREAL_PATH`. The default is `surrealkv:///data/surreal.db`.

| Supported scheme | Notes |
|---|---|
| `surrealkv://` | Default. Recommended for most deployments. |
| `rocksdb://` | Alternative embedded engine. |
| ~~`file://`~~ | **Removed.** No longer supported; causes startup failure. |

The `/data` path inside the container is mapped to `/mnt/user/appdata/broccoli_surrealdb` on the host by default, so data persists across container restarts and upgrades.

If you need to move data, copy the host directory before changing `SURREAL_PATH`.

### Validation

After the container starts, verify the volume mount and check for a clean startup:

```bash
docker inspect broccoli_surrealdb --format '{{range .Mounts}}{{println .Source "->" .Destination}}{{end}}'
```

Expected output:

```
/mnt/user/appdata/broccoli_surrealdb -> /data
```

Then check the logs:

```bash
docker logs --tail=100 broccoli_surrealdb
```

The logs should show:

```
 INFO  surrealdb::node Starting kvs store at surrealkv:///data/surreal.db
 INFO  surrealdb::rpc WebSocket listening on 0.0.0.0:8000
```

The container is healthy once you see the listening line. If you see `IO error: Permission denied (os error 13)`, the data directory was not made writable before the container started — stop the container, run the `chmod` command from the [First-run section](#first-run-directory-permissions), and restart.

If you see the following error, your `SURREAL_PATH` still uses the unsupported scheme:

```
ERROR  The `file://` scheme is no longer supported; use `rocksdb://` or `surrealkv://` instead
```

**Fix:** Update `SURREAL_PATH` to `surrealkv:///data/surreal.db` and restart the container.

## Obtaining a Google Maps API Key

1. Create a Google Cloud project in the [Google Cloud Console](https://console.cloud.google.com/projectcreate).
2. Enable the required Google Maps Platform APIs in [API Library](https://console.cloud.google.com/apis/library):
   - [Places API (New)](https://console.cloud.google.com/apis/library/places-backend.googleapis.com)
   - [Routes API](https://console.cloud.google.com/apis/library/routes.googleapis.com)
3. Enable billing for the same project from [Billing](https://console.cloud.google.com/billing) (required by Google Maps Platform APIs).
4. Create an API key in [Credentials](https://console.cloud.google.com/apis/credentials).
5. Apply restrictions to the key:
   - Set **API restrictions** to only **Places API (New)** and **Routes API**.
   - Add an **application restriction** only if it matches your deployment model (for server-side Unraid containers, overly strict client restrictions can block requests).
6. In the Unraid template, paste the key into `GOOGLE_MAPS_API_KEY`.
7. Save the template and restart the `broccoli_mcp-google-map` container.

### Validation

After the container restarts, run a live tool call through the MCP endpoint:

```bash
curl -sS http://<unraid-ip>:3020/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "maps_geocode",
      "arguments": {
        "address": "1600 Amphitheatre Parkway, Mountain View, CA"
      }
    }
  }'
```

A successful response with geocoding data confirms the MCP server can authenticate and communicate with Google Maps services. If you see `REQUEST_DENIED` or an API key error, re-check API enablement, billing, and key restrictions.

## `github-mcp-server` agent connection quick start

- **MCP endpoint URL:** `http://<unraid-ip>:8082/mcp`
- **Transport:** Streamable HTTP MCP over `POST` requests
- **Authentication:** Send the following header:

```http
Authorization: Bearer <your-github-token>
```
- **Recommended headers:**
  - `Content-Type: application/json`
  - `Accept: application/json, text/event-stream`

### Validate the deployment

```bash
curl -i http://<unraid-ip>:8082/mcp
```

Expected health signal:
- `HTTP/1.1 405 Method Not Allowed`
- `Allow: POST`

This means the server is reachable and waiting for MCP `POST` requests on `/mcp`.

### OAuth and token configuration

- Default/recommended setup for this wrapper is a static bearer token header in your MCP client config.
- If your MCP client supports OAuth discovery for your deployment, follow that client's OAuth setup flow; otherwise keep using the static header shown above.


### Example MCP client configurations

> These are generic examples. Field names can vary slightly by client.

**Streamable HTTP / HTTP-style config**
```json
{
  "name": "github-local",
  "type": "http",
  "url": "http://<unraid-ip>:8082/mcp",
  "headers": {
    "Authorization": "Bearer <your-github-token>"
  }
}
```

**SSE-style config (clients that still label remote MCP as SSE)**
```json
{
  "name": "github-local",
  "transport": "sse",
  "url": "http://<unraid-ip>:8082/mcp",
  "headers": {
    "Authorization": "Bearer <your-github-token>"
  }
}
```

**Clients that use command arrays or env-injected headers**
```json
{
  "mcpServers": {
    "github-local": {
      "url": "http://<unraid-ip>:8082/mcp",
      "headers": {
        "Authorization": "Bearer <your-github-token>"
      }
    }
  }
}
```

These templates are suitable starting points for Claude Desktop, OpenCode, Hermes, Open WebUI, LibreChat, Continue, Cline, Roo Code, and custom MCP clients.

## Included templates

<!-- TEMPLATES:START -->
This repository provides Unraid Docker templates and matching icons for self-hosted apps.

### `broccoli_github-mcp-server`
<img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="broccoli_github-mcp-server icon" width="64">

- Template: `templates/broccoli_github-mcp-server.xml`
- Container image: `ghcr.io/github/github-mcp-server:latest`
- GitHub MCP server for AI agents. Exposes a Streamable HTTP MCP endpoint at /mcp on port 8082 (GET /mcp returns 405 with Allow: POST when healthy).

### `broccoli_mcp-google-map`
<img src="https://raw.githubusercontent.com/julesdg6/Broccoli-Unraid-Wrappers/main/icons/mcp-google-map.png" alt="broccoli_mcp-google-map icon" width="64">

- Template: `templates/broccoli_mcp-google-map.xml`
- Container image: `node:20-alpine`
- MCP server providing 18 Google Maps tools for AI agents — geocode, search, directions, weather, air quality, local rank tracking, and more. Exposes a Streamable HTTP MCP endpoint at /mcp for use with Claude Desktop, Cursor, VS Code, and other MCP clients. Requires a Google Maps API key with Places API (New) and Routes API enabled.

### `broccoli_open-notebook`
<img src="https://raw.githubusercontent.com/julesdg6/Broccoli-Unraid-Wrappers/main/icons/open-notebook.png" alt="broccoli_open-notebook icon" width="64">

- Template: `templates/broccoli_open-notebook.xml`
- Container image: `lfnovo/open_notebook:v1-latest`
- Privacy-focused NotebookLM alternative. Uses the current upstream v1-latest image with separated SurrealDB. Exposes Web UI on 8502 and API on 5055 (used by open-notebook-mcp clients). Persist /app/data and keep OPEN_NOTEBOOK_ENCRYPTION_KEY stable across upgrades so provider credentials and model settings survive updates.

### `broccoli_surrealdb`
<img src="https://raw.githubusercontent.com/julesdg6/Broccoli-Unraid-Wrappers/main/icons/surrealdb.png" alt="broccoli_surrealdb icon" width="64">

- Template: `templates/broccoli_surrealdb.xml`
- Container image: `surrealdb/surrealdb:v2.6.5`
- SurrealDB database service for apps like Open Notebook. Pinned to v2.6.5 (SurrealDB 3.x is not yet compatible with Open Notebook). Runs `surreal start` and exposes port 8000 (HTTP + WebSocket RPC). Data is stored using the surrealkv engine at the path set by SURREAL_PATH (default: surrealkv:///data/surreal.db inside the container). Map /data to a persistent host path so data survives container restarts. Supported storage schemes: surrealkv:// (recommended), rocksdb://. The legacy file:// scheme is no longer supported — using it will prevent the container from starting. IMPORTANT: SurrealDB runs as a non-root user (UID 65532). Before starting the container for the first time, run on your Unraid host: mkdir -p /mnt/user/appdata/broccoli_surrealdb && chown -R 65532:65532 /mnt/user/appdata/broccoli_surrealdb

<!-- TEMPLATES:END -->

