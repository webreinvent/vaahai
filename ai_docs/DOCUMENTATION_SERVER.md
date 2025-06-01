# Setting Up a Documentation Server for Vaahai AI Docs

This document outlines several approaches to view the Vaahai AI documentation in a browser.

## Option 1: Simple HTTP Server

Python's built-in HTTP server provides a quick way to serve markdown files.

### Setup Instructions

1. Navigate to the project root directory:
   ```bash
   cd /Volumes/Data/Projects/vaahai
   ```

2. Start the Python HTTP server:
   ```bash
   python -m http.server 8000
   ```

3. Access the documentation at:
   ```
   http://localhost:8000/ai_docs/
   ```

**Note**: This approach serves the raw markdown files. For better rendering, consider the options below.

## Option 2: Docsify

[Docsify](https://docsify.js.org/) is a lightweight documentation site generator that doesn't generate static HTML files.

### Setup Instructions

1. Install Docsify CLI globally:
   ```bash
   npm install -g docsify-cli
   ```

2. Initialize Docsify in the ai_docs directory:
   ```bash
   cd /Volumes/Data/Projects/vaahai/ai_docs
   docsify init .
   ```

3. Customize the `index.html` file:
   ```html
   <!DOCTYPE html>
   <html>
   <head>
     <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
     <meta name="viewport" content="width=device-width,initial-scale=1">
     <meta charset="UTF-8">
     <title>Vaahai AI Documentation</title>
     <link rel="stylesheet" href="//cdn.jsdelivr.net/npm/docsify@4/themes/vue.css">
   </head>
   <body>
     <div id="app"></div>
     <script>
       window.$docsify = {
         name: 'Vaahai AI Docs',
         repo: 'https://github.com/webreinvent/vaahai',
         loadSidebar: true,
         subMaxLevel: 3,
         auto2top: true,
         search: {
           maxAge: 86400000,
           paths: 'auto',
           placeholder: 'Search',
           noData: 'No Results',
           depth: 6
         }
       }
     </script>
     <script src="//cdn.jsdelivr.net/npm/docsify@4"></script>
     <script src="//cdn.jsdelivr.net/npm/docsify/lib/plugins/search.min.js"></script>
     <script src="//cdn.jsdelivr.net/npm/prismjs/components/prism-bash.min.js"></script>
     <script src="//cdn.jsdelivr.net/npm/prismjs/components/prism-python.min.js"></script>
     <script src="//cdn.jsdelivr.net/npm/prismjs/components/prism-json.min.js"></script>
     <script src="//cdn.jsdelivr.net/npm/prismjs/components/prism-toml.min.js"></script>
   </body>
   </html>
   ```

4. Create a `_sidebar.md` file:
   ```markdown
   - [Home](/)
   - [AI Context](AI_CONTEXT.md)
   - [Architecture](ARCHITECTURE.md)
   - [API Reference](API_REFERENCE.md)
   - [Design Patterns](DESIGN_PATTERNS.md)
   - [Business Logic](BUSINESS_LOGIC.md)
   - [Testing Strategy](TESTING_STRATEGY.md)
   - [Implementation Roadmap](IMPLEMENTATION_ROADMAP.md)
   - [AI Integration](AI_INTEGRATION.md)
   ```

5. Start the Docsify server:
   ```bash
   docsify serve
   ```

6. Access the documentation at:
   ```
   http://localhost:3000
   ```

## Option 3: MkDocs

[MkDocs](https://www.mkdocs.org/) is a fast, simple static site generator for documentation with a focus on speed and simplicity.

### Setup Instructions

1. Install MkDocs and the Material theme:
   ```bash
   pip install mkdocs mkdocs-material
   ```

2. Create a new MkDocs project:
   ```bash
   cd /Volumes/Data/Projects/vaahai
   mkdocs new docs
   ```

3. Configure MkDocs by editing `mkdocs.yml`:
   ```yaml
   site_name: Vaahai AI Documentation
   theme:
     name: material
     palette:
       primary: indigo
       accent: indigo
   
   nav:
     - Home: index.md
     - AI Context: ai_context.md
     - Architecture: architecture.md
     - API Reference: api_reference.md
     - Design Patterns: design_patterns.md
     - Business Logic: business_logic.md
     - Testing Strategy: testing_strategy.md
     - Implementation Roadmap: implementation_roadmap.md
     - AI Integration: ai_integration.md
   
   markdown_extensions:
     - pymdownx.highlight
     - pymdownx.superfences
     - pymdownx.tabbed
     - pymdownx.tasklist
     - admonition
   ```

4. Copy the AI documentation files to the docs directory:
   ```bash
   cp ai_docs/*.md docs/
   # Rename files to lowercase for consistency
   cd docs
   for file in *.md; do mv "$file" "$(echo $file | tr '[:upper:]' '[:lower:]')"; done
   # Update the index.md with the README.md content
   cp ai_docs/README.md docs/index.md
   ```

5. Build and serve the documentation:
   ```bash
   mkdocs serve
   ```

6. Access the documentation at:
   ```
   http://localhost:8000
   ```

## Option 4: GitBook

[GitBook](https://www.gitbook.com/) is a modern documentation platform that can be used to create beautiful documentation.

### Setup Instructions

1. Install GitBook CLI:
   ```bash
   npm install -g gitbook-cli
   ```

2. Initialize GitBook in a new directory:
   ```bash
   mkdir -p /Volumes/Data/Projects/vaahai/gitbook
   cd /Volumes/Data/Projects/vaahai/gitbook
   gitbook init
   ```

3. Create a `SUMMARY.md` file:
   ```markdown
   # Summary
   
   * [Introduction](README.md)
   * [AI Context](ai_context.md)
   * [Architecture](architecture.md)
   * [API Reference](api_reference.md)
   * [Design Patterns](design_patterns.md)
   * [Business Logic](business_logic.md)
   * [Testing Strategy](testing_strategy.md)
   * [Implementation Roadmap](implementation_roadmap.md)
   * [AI Integration](ai_integration.md)
   ```

4. Copy and rename the AI documentation files:
   ```bash
   cp /Volumes/Data/Projects/vaahai/ai_docs/README.md ./README.md
   cp /Volumes/Data/Projects/vaahai/ai_docs/AI_CONTEXT.md ./ai_context.md
   cp /Volumes/Data/Projects/vaahai/ai_docs/ARCHITECTURE.md ./architecture.md
   cp /Volumes/Data/Projects/vaahai/ai_docs/API_REFERENCE.md ./api_reference.md
   cp /Volumes/Data/Projects/vaahai/ai_docs/DESIGN_PATTERNS.md ./design_patterns.md
   cp /Volumes/Data/Projects/vaahai/ai_docs/BUSINESS_LOGIC.md ./business_logic.md
   cp /Volumes/Data/Projects/vaahai/ai_docs/TESTING_STRATEGY.md ./testing_strategy.md
   cp /Volumes/Data/Projects/vaahai/ai_docs/IMPLEMENTATION_ROADMAP.md ./implementation_roadmap.md
   cp /Volumes/Data/Projects/vaahai/ai_docs/AI_INTEGRATION.md ./ai_integration.md
   ```

5. Serve the GitBook:
   ```bash
   gitbook serve
   ```

6. Access the documentation at:
   ```
   http://localhost:4000
   ```

## Option 5: VS Code Extension

For a simpler approach without setting up a server, you can use VS Code extensions.

### Setup Instructions

1. Install the "Markdown Preview Enhanced" extension in VS Code
2. Open any markdown file in the ai_docs directory
3. Press `Cmd+K V` (Mac) or `Ctrl+K V` (Windows/Linux) to open a preview pane
4. For a more browser-like experience, click the "Open Preview in Browser" button in the preview pane

## Option 6: GitHub Pages

If the repository is hosted on GitHub, you can use GitHub Pages to host the documentation.

### Setup Instructions

1. Push the repository to GitHub
2. Enable GitHub Pages in the repository settings
3. Configure it to use the `/docs` directory or the `gh-pages` branch
4. If using the `/docs` directory approach:
   ```bash
   mkdir -p /Volumes/Data/Projects/vaahai/docs
   cp /Volumes/Data/Projects/vaahai/ai_docs/*.md /Volumes/Data/Projects/vaahai/docs/
   ```
5. Create an `index.html` file in the docs directory or use a Jekyll theme

## Recommended Approach

For the Vaahai project, we recommend using **Option 2: Docsify** for the following reasons:

1. **Simplicity**: No build process required
2. **Live Reload**: Changes are reflected immediately
3. **Modern UI**: Clean, responsive design
4. **Search Functionality**: Built-in search capabilities
5. **Code Highlighting**: Syntax highlighting for code blocks
6. **Minimal Configuration**: Quick to set up and maintain

This approach provides a good balance between ease of setup and rich features for documentation viewing.
