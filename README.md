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

**broccoli_norns-desktop:**
```bash
curl -fsSL -o /boot/config/plugins/dockerMan/templates-user/broccoli_norns-desktop.xml \
  https://raw.githubusercontent.com/julesdg6/Broccoli-Unraid-Wrappers/main/templates/broccoli_norns-desktop.xml
```

**broccoli_open-notebook:**
```bash
curl -fsSL -o /boot/config/plugins/dockerMan/templates-user/broccoli_open-notebook.xml \
  https://raw.githubusercontent.com/julesdg6/Broccoli-Unraid-Wrappers/main/templates/broccoli_open-notebook.xml
```

**broccoli_omniroute:**
```bash
curl -fsSL -o /boot/config/plugins/dockerMan/templates-user/broccoli_omniroute.xml \
  https://raw.githubusercontent.com/julesdg6/Broccoli-Unraid-Wrappers/main/templates/broccoli_omniroute.xml
```

**broccoli_stealth-browser-mcp:**
```bash
curl -fsSL -o /boot/config/plugins/dockerMan/templates-user/broccoli_stealth-browser-mcp.xml \
  https://raw.githubusercontent.com/julesdg6/Broccoli-Unraid-Wrappers/main/templates/broccoli_stealth-browser-mcp.xml
```

**broccoli_surrealdb:**
```bash
curl -fsSL -o /boot/config/plugins/dockerMan/templates-user/broccoli_surrealdb.xml \
  https://raw.githubusercontent.com/julesdg6/Broccoli-Unraid-Wrappers/main/templates/broccoli_surrealdb.xml
```

**broccoli_maestro-mcp:**
```bash
curl -fsSL -o /boot/config/plugins/dockerMan/templates-user/broccoli_maestro-mcp.xml \
  https://raw.githubusercontent.com/julesdg6/Broccoli-Unraid-Wrappers/main/templates/broccoli_maestro-mcp.xml
```

3. In the Unraid web UI, go to **Docker** → **Add Container**.
4. In the template dropdown, select the desired template, then review/save.
5. Before starting the container, set required values:

   **broccoli_omniroute:**
   - `OMNIROUTE_WS_BRIDGE_SECRET`: recommended for production — set to a strong random string (`openssl rand -hex 32`)
   - After the container starts, open the dashboard at `http://<unraid-ip>:20128` and point coding agents (Claude Code, Codex, Cursor, Cline…) to `http://<unraid-ip>:20128/v1`
   - Connect free providers via **Dashboard → Providers** (e.g. Kiro AI, OpenCode Free — no signup required)
   - Copy an API key from **Dashboard → Endpoints** and use it as the `Authorization: Bearer` token in your coding tool

   **broccoli_github-mcp-server:**
   - `GITHUB_PERSONAL_ACCESS_TOKEN`: optional but recommended for higher API limits and private repo access
   - After the container starts, point your MCP client to `http://<unraid-ip>:8082/mcp`

   **broccoli_mcp-google-map:**
   - `GOOGLE_MAPS_API_KEY`: your Google Maps API key from [Google Cloud Console](https://console.cloud.google.com)
   - Enable **Places API (New)** and **Routes API** in your Google Cloud project before use
   - After the container starts, point your MCP client to `http://<unraid-ip>:3020/mcp`

   **broccoli_norns-desktop:**
   - Uses image `schollz/norns:dust` from the upstream norns-desktop workflow (linux/amd64)
   - Ensure your Unraid host exposes `/dev/snd` to Docker and has an `audio` group available
   - Create `/mnt/user/appdata/broccoli_norns-desktop` for persistent norns `dust` data before starting the container
   - **If your server has no real sound card (most Unraid NAS/server builds):** you must supply a jackdrc file that uses the ALSA dummy driver, otherwise jackd will crash immediately with `signal 11`. Do this once on your Unraid host before starting the container:
     ```bash
     mkdir -p /mnt/user/appdata/broccoli_norns-desktop
     echo '/usr/bin/jackd -R -P 95 -d dummy -p 1024' > /mnt/user/appdata/broccoli_norns-desktop/jackdrc
     ```
     Then set the `Jackd Config Override` template field to `/mnt/user/appdata/broccoli_norns-desktop/jackdrc`.
   - **If your server does have a real sound card:** leave `Jackd Config Override` blank to use the container default, or point it to a jackdrc file with your ALSA device (e.g. `/usr/bin/jackd -R -P 95 -d alsa -P hw:0 -C hw:0`).
   - **Write permissions and first-run setup:** container startup creates `/home/we/dust/{code,data,audio,jackdrc}`, runs `chown -R we:we /home/we/dust`, and verifies those paths are writable by user `we` (UID/GID 1000) before launching norns. If this check fails, startup exits with a clear permission error so the volume ownership can be fixed on the Unraid host.
   - The template includes `--tty` in Extra Parameters so that the container's `tmuxp`-based startup can allocate a pseudo-terminal; without it the container exits immediately with `open terminal failed: not a terminal`
   - After the container starts:
     - maiden UI: `http://<unraid-ip>:5000`
     - norns screen: `http://<unraid-ip>:8889`
     - audio stream: `http://<unraid-ip>:8000/radio.mp3` (requires jackd to be running; with the dummy driver the stream encodes silence)

   **broccoli_open-notebook:**
   - Depends on `broccoli_surrealdb` (or another reachable SurrealDB instance) running with matching credentials
   - Uses upstream `lfnovo/open_notebook:v1-latest` and starts `open-notebook-mcp` in the same container
   - `OPEN_NOTEBOOK_ENCRYPTION_KEY`: a unique, cryptographically random secret (recommended 32+ characters)
   - Keep `OPEN_NOTEBOOK_ENCRYPTION_KEY` unchanged after first deploy; rotating or losing it makes saved provider credentials unreadable
   - `SURREAL_PASSWORD`: must match your SurrealDB service password (use a strong, unique password)
   - `SURREAL_URL`: use `ws://surrealdb:8000/rpc` only when both containers are on a user-defined Docker network with working container DNS; if not on a user-defined network (default bridge mode), use `ws://<unraid-ip>:8000/rpc`
   - MCP defaults: `OPEN_NOTEBOOK_URL=http://127.0.0.1:5055`, `OPEN_NOTEBOOK_MCP_PORT=5056`, MCP endpoint `http://<unraid-ip>:5056/mcp`
   - **Security warning:** set `OPEN_NOTEBOOK_PASSWORD` before exposing API/MCP ports beyond your trusted network. Leaving it empty while publishing these ports can allow unauthenticated notebook/API access.
   - Optional but useful advanced variables in the template: `API_URL`, `OPEN_NOTEBOOK_PASSWORD`, `OPEN_NOTEBOOK_EMBEDDING_BATCH_SIZE`, `SURREAL_COMMANDS_MAX_TASKS`, `CORS_ORIGINS`
   - Example key generation: `openssl rand -base64 32`

   **broccoli_stealth-browser-mcp:**
   - `STEALTH_BROWSER_MCP_AUTH_TOKEN`: optional but strongly recommended — set a random token (e.g. `openssl rand -hex 32`) so the HTTP endpoint requires auth; without it the MCP port is open to anyone on your network
   - The template references `ghcr.io/vibheksoni/stealth-browser-mcp:latest`; if the project maintainer has not yet published this image, build it locally — see the [stealth-browser-mcp connection quick start](#stealth-browser-mcp-agent-connection-quick-start) section below
   - After the container starts, point your MCP client to `http://<unraid-ip>:8000/mcp`

   **broccoli_maestro-mcp:**
   - No required configuration — the container starts immediately and the MCP endpoint is available at `http://<unraid-ip>:3001/mcp`
   - No authentication is built in; keep the MCP port within your trusted network or use a reverse proxy to add auth

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
   - `curl http://<unraid-ip>:5056/mcp`
   - login to UI and verify credentials/models are still present
6. If migrating from older env-based provider configs, use **Settings → API Keys → Migrate to Database**, then re-test/discover/register models.

### Troubleshooting and recovery

Health and startup checks:

```bash
docker logs --tail=200 broccoli_open-notebook
curl -sS http://<unraid-ip>:5055/health
curl -i http://<unraid-ip>:5056/mcp
docker exec broccoli_open-notebook sh -lc 'command -v curl || command -v wget || echo "No HTTP client in image"'
```

Expected startup log markers in `docker logs`:
- `[startup] Open Notebook supervisord starting (api, worker, frontend)...`
- `[startup] Open Notebook API healthy at http://127.0.0.1:5055`
- `[startup] Open Notebook MCP starting at http://0.0.0.0:5056/mcp ...`

Container-internal diagnostics:

```bash
docker exec broccoli_open-notebook sh -lc 'curl -sS http://127.0.0.1:5055/health'
docker exec broccoli_open-notebook sh -lc 'curl -sS http://127.0.0.1:5055/openapi.json | head -c 200'
docker exec broccoli_open-notebook sh -lc 'curl -i http://127.0.0.1:5056/mcp'
```

Common recovery actions:

- **No models available**: run the provider onboarding flow again in **Settings → API Keys**, then set defaults in **Settings → Models**.
- **Credential decrypt errors after update**: restore previous `OPEN_NOTEBOOK_ENCRYPTION_KEY` and restart.
- **Database auth/connection errors**: verify `SURREAL_URL`, `SURREAL_USER`, `SURREAL_PASSWORD`, and SurrealDB container health.
- **Slow/failing embeddings on local setups**: lower `OPEN_NOTEBOOK_EMBEDDING_BATCH_SIZE` (for example `8`) and restart.
- **MCP endpoint unreachable**: confirm Open Notebook API is healthy first (`curl http://<unraid-ip>:5055/health`), then verify MCP endpoint (`curl -i http://<unraid-ip>:5056/mcp`) and `OPEN_NOTEBOOK_URL`/`OPEN_NOTEBOOK_MCP_PORT` values.

### Hermes MCP configuration example

```yaml
open_notebook:
  enabled: true
  transport: streamable_http
  url: http://<host>:5056/mcp
```

Replace `<host>` with your Unraid server IP or hostname (for example `192.168.1.100`).
Hermes connects to the MCP endpoint without an extra auth block in this wrapper. If `OPEN_NOTEBOOK_PASSWORD` is set, the bundled MCP process uses it internally as the Authorization bearer value when calling the local Open Notebook API.

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

## `stealth-browser-mcp` agent connection quick start

- **MCP endpoint URL:** `http://<unraid-ip>:8000/mcp`
- **Transport:** Streamable HTTP MCP over `POST` requests
- **Authentication:** If `STEALTH_BROWSER_MCP_AUTH_TOKEN` is set, send the following header:

```http
Authorization: Bearer <your-token>
```
- **Recommended headers:**
  - `Content-Type: application/json`
  - `Accept: application/json, text/event-stream`

### Building the image

The template references `ghcr.io/vibheksoni/stealth-browser-mcp:latest`. If the project maintainer has not yet published this image to the GitHub Container Registry, build it yourself and tag it to match:

```bash
# On your Unraid host or another machine with Docker
git clone https://github.com/vibheksoni/stealth-browser-mcp.git
cd stealth-browser-mcp
docker build -t ghcr.io/vibheksoni/stealth-browser-mcp:latest .
```

If building on a machine other than your Unraid server, push or export the image and load it on Unraid:

```bash
# Export / import across machines
docker save ghcr.io/vibheksoni/stealth-browser-mcp:latest | gzip > stealth-browser-mcp.tar.gz
# On Unraid:
docker load < stealth-browser-mcp.tar.gz
```

### Validate the deployment

```bash
curl -i http://<unraid-ip>:8000/mcp
```

If `STEALTH_BROWSER_MCP_AUTH_TOKEN` is set, include the header:

```bash
curl -i -H "Authorization: Bearer <your-token>" http://<unraid-ip>:8000/mcp
```

### Example MCP client configurations

> These are generic examples. Field names can vary slightly by client.
> If `STEALTH_BROWSER_MCP_AUTH_TOKEN` is not set, omit the `headers` block.

**Streamable HTTP / HTTP-style config**
```json
{
  "name": "stealth-browser-local",
  "type": "http",
  "url": "http://<unraid-ip>:8000/mcp",
  "headers": {
    "Authorization": "Bearer <your-token>"
  }
}
```

**SSE-style config (clients that still label remote MCP as SSE)**
```json
{
  "name": "stealth-browser-local",
  "transport": "sse",
  "url": "http://<unraid-ip>:8000/mcp",
  "headers": {
    "Authorization": "Bearer <your-token>"
  }
}
```

**Clients that use command arrays or env-injected headers**
```json
{
  "mcpServers": {
    "stealth-browser-local": {
      "url": "http://<unraid-ip>:8000/mcp",
      "headers": {
        "Authorization": "Bearer <your-token>"
      }
    }
  }
}
```

## `maestro-mcp` agent connection quick start

- **MCP endpoint URL:** `http://<unraid-ip>:3001/mcp`
- **Transport:** Streamable HTTP MCP over `POST` requests
- **Authentication:** None required

### Validate the deployment

```bash
curl -sS http://<unraid-ip>:3001/health
```

Expected response (version number will reflect the installed release):

```json
{"status":"ok","server":"maestro-workflow-mcp","version":"<version>"}
```

### Example MCP client configurations

> These are generic examples. Field names can vary slightly by client.

**Streamable HTTP / HTTP-style config**
```json
{
  "name": "maestro-local",
  "type": "http",
  "url": "http://<unraid-ip>:3001/mcp"
}
```

**SSE-style config (clients that still label remote MCP as SSE)**
```json
{
  "name": "maestro-local",
  "transport": "sse",
  "url": "http://<unraid-ip>:3001/mcp"
}
```

**Clients that use command arrays**
```json
{
  "mcpServers": {
    "maestro-local": {
      "url": "http://<unraid-ip>:3001/mcp"
    }
  }
}
```

These templates are suitable starting points for Claude Desktop, Cursor, VS Code Copilot, Gemini CLI, OpenCode, and other MCP-compatible clients. After connecting, use any of the 25 commands (e.g. `/diagnose`, `/refine`, `/fortify`) in your AI coding agent.

## Included templates

<!-- TEMPLATES:START -->
This repository provides Unraid Docker templates and matching icons for self-hosted apps.

### `broccoli_github-mcp-server`
<img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="broccoli_github-mcp-server icon" width="64">

- Template: `templates/broccoli_github-mcp-server.xml`
- Container image: `ghcr.io/github/github-mcp-server:latest`
- GitHub MCP server for AI agents. Exposes a Streamable HTTP MCP endpoint at /mcp on port 8082 (GET /mcp returns 405 with Allow: POST when healthy).

### `broccoli_maestro-mcp`
<img src="https://github.com/sharpdeveye.png" alt="broccoli_maestro-mcp icon" width="64">

- Template: `templates/broccoli_maestro-mcp.xml`
- Container image: `node:20-alpine`
- Maestro MCP server for AI agent workflow optimization. Exposes a Streamable HTTP MCP endpoint at /mcp on port 3001. Provides 25 commands (diagnose, refine, fortify, streamline, and more), 10 tools, and 8 skill resources to help AI agents avoid common workflow anti-patterns with domain-specific guidance for prompt engineering, context management, tool orchestration, and agent architecture. Health check available at /health.

### `broccoli_mcp-google-map`
<img src="https://raw.githubusercontent.com/julesdg6/Broccoli-Unraid-Wrappers/main/icons/mcp-google-map.png" alt="broccoli_mcp-google-map icon" width="64">

- Template: `templates/broccoli_mcp-google-map.xml`
- Container image: `node:20-alpine`
- MCP server providing 18 Google Maps tools for AI agents — geocode, search, directions, weather, air quality, local rank tracking, and more. Exposes a Streamable HTTP MCP endpoint at /mcp for use with Claude Desktop, Cursor, VS Code, and other MCP clients. Requires a Google Maps API key with Places API (New) and Routes API enabled.

### `broccoli_norns-desktop`
<img src="https://raw.githubusercontent.com/julesdg6/Broccoli-Unraid-Wrappers/main/icons/norns-desktop.png" alt="broccoli_norns-desktop icon" width="64">

- Template: `templates/broccoli_norns-desktop.xml`
- Container image: `schollz/norns:dust`
- norns on Docker for browser-based testing. Exposes maiden on 5000, norns screen at 8889, and audio stream at 8000/radio.mp3. Requires /dev/snd and realtime container permissions for audio. On startup, the wrapper initializes `/home/we/dust` (`code`, `data`, `audio`, `jackdrc`), verifies write access for user `we` (UID/GID 1000), and fails with a clear message if permissions are incorrect. Servers without a real sound card must supply a jackdrc file using the dummy driver (see Jackd Config Override).

### `broccoli_omniroute`
<img src="https://raw.githubusercontent.com/julesdg6/Broccoli-Unraid-Wrappers/main/icons/omniroute.png" alt="broccoli_omniroute icon" width="64">

- Template: `templates/broccoli_omniroute.xml`
- Container image: `diegosouzapw/omniroute:latest`
- OmniRoute — free AI gateway that connects coding agents (Claude Code, Codex, Cursor, Cline, Copilot) to 236 providers including 50+ with a free tier, through one OpenAI-compatible endpoint. Provides RTK + Caveman token compression (15–95% savings), 17 routing strategies with auto-fallback, MCP server (87 tools), A2A protocol, and an interactive dashboard. Dashboard and API both run on port 20128 (API at /v1). Data is persisted in /app/data — map it to a host path so settings, provider credentials, and combos survive container restarts. Set OMNIROUTE_WS_BRIDGE_SECRET to a strong random string for production use.

### `broccoli_open-notebook`
<img src="https://raw.githubusercontent.com/julesdg6/Broccoli-Unraid-Wrappers/main/icons/open-notebook.png" alt="broccoli_open-notebook icon" width="64">

- Template: `templates/broccoli_open-notebook.xml`
- Container image: `lfnovo/open_notebook:v1-latest`
- Privacy-focused NotebookLM alternative. Uses upstream v1-latest image with separated SurrealDB and starts Open Notebook MCP in the same container. Exposes Web UI on 8502, API on 5055, and MCP Streamable HTTP on 5056 (/mcp). Persist /app/data and keep OPEN_NOTEBOOK_ENCRYPTION_KEY stable across upgrades so provider credentials and model settings survive updates.

### `broccoli_stealth-browser-mcp`
<img src="https://raw.githubusercontent.com/vibheksoni/stealth-browser-mcp/master/media/UndetectedStealthBrowser.png" alt="broccoli_stealth-browser-mcp icon" width="64">

- Template: `templates/broccoli_stealth-browser-mcp.xml`
- Container image: `ghcr.io/vibheksoni/stealth-browser-mcp:latest`
- Stealth browser MCP server for AI agents — bypasses Cloudflare, antibot systems, and social media blocks using nodriver + Chrome DevTools Protocol + FastMCP. Exposes a Streamable HTTP MCP endpoint at /mcp on port 8000. Provides 97 tools across 11 sections: browser management, element interaction, element extraction, network interception, CDP function execution, and more. Set STEALTH_BROWSER_MCP_AUTH_TOKEN to enable bearer token auth for the HTTP endpoint.

### `broccoli_surrealdb`
<img src="https://raw.githubusercontent.com/julesdg6/Broccoli-Unraid-Wrappers/main/icons/surrealdb.png" alt="broccoli_surrealdb icon" width="64">

- Template: `templates/broccoli_surrealdb.xml`
- Container image: `surrealdb/surrealdb:v2.6.5`
- SurrealDB database service for apps like Open Notebook. Pinned to v2.6.5 (SurrealDB 3.x is not yet compatible with Open Notebook). Runs `surreal start` and exposes port 8000 (HTTP + WebSocket RPC). Data is stored using the surrealkv engine at the path set by SURREAL_PATH (default: surrealkv:///data/surreal.db inside the container). Map /data to a persistent host path so data survives container restarts. Supported storage schemes: surrealkv:// (recommended), rocksdb://. The legacy file:// scheme is no longer supported — using it will prevent the container from starting. IMPORTANT: SurrealDB runs as a non-root user (UID 65532). Before starting the container for the first time, run on your Unraid host: mkdir -p /mnt/user/appdata/broccoli_surrealdb && chown -R 65532:65532 /mnt/user/appdata/broccoli_surrealdb

<!-- TEMPLATES:END -->

