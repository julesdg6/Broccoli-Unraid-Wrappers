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
4. Select template **open-notebook.xml** (or choose it from the template dropdown), then review/save.
5. Before starting the container, set required values:
   - `OPEN_NOTEBOOK_ENCRYPTION_KEY`: a unique secret string
   - `SURREAL_PASSWORD`: must match your SurrealDB service password (use a strong, unique password)

## Included templates

- `templates/open-notebook.xml` - Open Notebook (`lfnovo/open_notebook:v1-latest`)
  - Web UI port: `8502`
  - API/MCP integration port: `5055`
  - Includes required variables with defaults where available
  - Includes a PNG icon
