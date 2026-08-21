# Practice 1 - Node.js Core Modules

This folder contains exercises practicing Node.js core modules (`fs`, `http`, `path`).

> [!NOTE]
> Since the parent directory's `package.json` contains `"type": "module"`, all files containing CommonJS (`require`) syntax are saved with the `.cjs` extension. This tells Node.js to interpret them as CommonJS modules instead of ES modules.

---

## Files

### 1. File System Operations
- **File:** [fs_demo.cjs](file:///c:/Users/arif3/OneDrive/Attachments/Desktop/newaasss/practice1/fs_demo.cjs)
- **Description:** Demonstrates creating a file, reading it, appending content, and reading it again.
- **Run Command:**
  ```bash
  node fs_demo.cjs
  ```

### 2. Basic HTTP Server
- **File:** [server_basic.cjs](file:///c:/Users/arif3/OneDrive/Attachments/Desktop/newaasss/practice1/server_basic.cjs)
- **Description:** Sets up a basic server that responds with `"Hello World from node.js server"`.
- **Run Command:**
  ```bash
  node server_basic.cjs
  ```

### 3. HTTP Server with Routing
- **File:** [server_routing.cjs](file:///c:/Users/arif3/OneDrive/Attachments/Desktop/newaasss/practice1/server_routing.cjs)
- **Description:** Sets up a server with simple routing (`/`, `/about`, `/products`).
- **Run Command:**
  ```bash
  node server_routing.cjs
  ```

### 4. HTTP Server Serving HTML
- **File:** [server_html.cjs](file:///c:/Users/arif3/OneDrive/Attachments/Desktop/newaasss/practice1/server_html.cjs)
- **Description:** Serves a local HTML file ([index.html](file:///c:/Users/arif3/OneDrive/Attachments/Desktop/newaasss/practice1/index.html)) at the root path (`/`).
- **Run Command:**
  ```bash
  node server_html.cjs
  ```
