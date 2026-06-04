# Broccoli-Unraid-Wrappers

A collection of Unraid 7 Docker templates (wrappers) for self-hosted apps.

## Install a template on Unraid 7 with `curl`

1. SSH into your Unraid server.
2. Download a template into your user templates folder:

**github-mcp-server:**
```bash
curl -fsSL -o /boot/config/plugins/dockerMan/templates-user/github-mcp-server.xml \
  https://raw.githubusercontent.com/julesdg6/Broccoli-Unraid-Wrappers/main/templates/github-mcp-server.xml
```

**mcp-google-map:**
```bash
curl -fsSL -o /boot/config/plugins/dockerMan/templates-user/mcp-google-map.xml \
  https://raw.githubusercontent.com/julesdg6/Broccoli-Unraid-Wrappers/main/templates/mcp-google-map.xml
```

**open-notebook:**
```bash
curl -fsSL -o /boot/config/plugins/dockerMan/templates-user/open-notebook.xml \
  https://raw.githubusercontent.com/julesdg6/Broccoli-Unraid-Wrappers/main/templates/open-notebook.xml
```

3. In the Unraid web UI, go to **Docker** → **Add Container**.
4. In the template dropdown, select the desired template, then review/save.
5. Before starting the container, set required values:

   **github-mcp-server:**
   - `GITHUB_PERSONAL_ACCESS_TOKEN`: optional but recommended for higher API limits and private repo access
   - After the container starts, point your MCP client to `http://<unraid-ip>:8082/`

   **mcp-google-map:**
   - `GOOGLE_MAPS_API_KEY`: your Google Maps API key from [Google Cloud Console](https://console.cloud.google.com)
   - Enable **Places API (New)** and **Routes API** in your Google Cloud project before use
   - After the container starts, point your MCP client to `http://<unraid-ip>:3020/mcp`

   **open-notebook:**
   - `OPEN_NOTEBOOK_ENCRYPTION_KEY`: a unique, cryptographically random secret (recommended 32+ characters)
   - `SURREAL_PASSWORD`: must match your SurrealDB service password (use a strong, unique password)
   - Example key generation: `openssl rand -base64 32`

## Included templates

<!-- TEMPLATES:START -->
This repository provides Unraid Docker templates and matching icons for self-hosted apps.

### `github-mcp-server`
<img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="github-mcp-server icon" width="64">

- Template: `templates/github-mcp-server.xml`
- Container image: `ghcr.io/github/github-mcp-server:latest`
- GitHub MCP server for AI agents. Exposes MCP over HTTP on port 8082.

### `mcp-google-map`
<img src="https://raw.githubusercontent.com/julesdg6/Broccoli-Unraid-Wrappers/main/icons/mcp-google-map.png" alt="mcp-google-map icon" width="64">

- Template: `templates/mcp-google-map.xml`
- Container image: `node:20-alpine`
- MCP server providing 18 Google Maps tools for AI agents — geocode, search, directions, weather, air quality, local rank tracking, and more. Exposes a Streamable HTTP MCP endpoint at /mcp for use with Claude Desktop, Cursor, VS Code, and other MCP clients. Requires a Google Maps API key with Places API (New) and Routes API enabled.

### `open-notebook`
<img src="https://raw.githubusercontent.com/julesdg6/Broccoli-Unraid-Wrappers/main/icons/open-notebook.png" alt="open-notebook icon" width="64">

- Template: `templates/open-notebook.xml`
- Container image: `lfnovo/open_notebook:v1-latest`
- Privacy-focused NotebookLM alternative. Exposes Web UI on 8502 and API on 5055 (used by open-notebook-mcp clients).

<!-- TEMPLATES:END -->

