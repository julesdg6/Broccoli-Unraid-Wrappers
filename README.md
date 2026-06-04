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
   - `OPEN_NOTEBOOK_ENCRYPTION_KEY`: a unique, cryptographically random secret (recommended 32+ characters)
   - `SURREAL_PASSWORD`: must match your SurrealDB service password (use a strong, unique password)
   - `SURREAL_URL`: keep `ws://surrealdb:8000/rpc` when using this repo's `broccoli_surrealdb` template on the same Docker network
   - Example key generation: `openssl rand -base64 32`

   **broccoli_surrealdb:**
   - `SURREAL_PASS`: required root password (must match `broccoli_open-notebook` `SURREAL_PASSWORD`)
   - `SURREAL_USER`: defaults to `root`

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
- Privacy-focused NotebookLM alternative. Exposes Web UI on 8502 and API on 5055 (used by open-notebook-mcp clients).

### `broccoli_surrealdb`
<img src="https://raw.githubusercontent.com/surrealdb/icons/main/surrealdb.svg" alt="broccoli_surrealdb icon" width="64">

- Template: `templates/broccoli_surrealdb.xml`
- Container image: `surrealdb/surrealdb:latest`
- SurrealDB database service for apps like Open Notebook. Exposes SurrealDB over port 8000, including the WebSocket RPC endpoint used by Open Notebook.

<!-- TEMPLATES:END -->

