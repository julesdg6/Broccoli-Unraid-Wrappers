# Broccoli-Unraid-Wrappers

A collection of Unraid 7 Docker templates (wrappers) for self-hosted apps.

## Install a template on Unraid 7 with `curl`

1. SSH into your Unraid server.
2. Download a template into your user templates folder:

```bash
curl -fsSL -o /boot/config/plugins/dockerMan/templates-user/open-notebook.xml \
  https://raw.githubusercontent.com/julesdg6/Broccoli-Unraid-Wrappers/main/templates/open-notebook.xml
```

3. In the Unraid web UI, go to **Docker** → **Add Container**.
4. In the template dropdown, select **open-notebook** (it may appear as `open-notebook.xml`), then review/save.
5. Before starting the container, set required values:
   - `OPEN_NOTEBOOK_ENCRYPTION_KEY`: a unique, cryptographically random secret (recommended 32+ characters)
   - `SURREAL_PASSWORD`: must match your SurrealDB service password (use a strong, unique password)
   - Example key generation: `openssl rand -base64 32`

## Included templates

<!-- TEMPLATES:START -->
This repository provides Unraid Docker templates and matching icons for self-hosted apps.

### `github-mcp-server`
![github-mcp-server icon](https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png)

- Template: `templates/github-mcp-server.xml`
- Container image: `ghcr.io/github/github-mcp-server:latest`
- GitHub MCP server for AI agents. Exposes MCP over HTTP on port 8082.

### `open-notebook`
![open-notebook icon](https://raw.githubusercontent.com/julesdg6/Broccoli-Unraid-Wrappers/main/icons/open-notebook.png)

- Template: `templates/open-notebook.xml`
- Container image: `lfnovo/open_notebook:v1-latest`
- Privacy-focused NotebookLM alternative. Exposes Web UI on 8502 and API on 5055 (used by open-notebook-mcp clients).

<!-- TEMPLATES:END -->

