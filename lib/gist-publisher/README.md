# Gist Publisher - Document Delivery Service

**Purpose:** Automatically publish documents, BOMs, reports, and any file that needs sharing as a GitHub Gist with a permanent URL.

## Why Gist?

1. **Instant URLs** - No deploy, no hosting, just publish
2. **Version history** - Every edit is tracked
3. **Markdown rendering** - GitHub renders .md beautifully
4. **Raw access** - Direct link to raw content for scripts
5. **Forkable** - Users can fork and modify
6. **Free forever** - No hosting costs

## Usage

### CLI
```bash
# Publish a file
./publish.sh path/to/document.md "Description here"

# Returns: https://gist.github.com/Mikecranesync/abc123...
```

### From Python
```python
from gist_publisher import publish_document

url = publish_document(
    filepath="jobs/JOB-123/BOM.md",
    description="Project BOM",
    public=True
)
print(url)  # https://gist.github.com/...
```

### From Any Agent/Process
Any process that generates a document should call this instead of just saving locally:

```bash
# In your workflow
document_path=$(generate_report)
gist_url=$(publish.sh "$document_path" "Auto-generated report")
echo "Full details: $gist_url"
```

## Elegant Open Source Patterns

### 1. **bl.ocks.org** (RIP, but pattern lives on)
- Rendered Gists as interactive D3.js visualizations
- URL: `bl.ocks.org/username/gist_id`
- Fork: [blockbuilder.org](https://github.com/enjalot/blockbuilder)

### 2. **roughdraft.io**
- Renders Gists as styled web pages
- Pattern: `roughdraft.io/gist_id`
- Good for: Styled documents, proposals

### 3. **nbviewer.org**
- Renders Jupyter notebooks from Gists
- Pattern: `nbviewer.org/gist/username/gist_id`
- Good for: Data analysis, technical reports

### 4. **Gist.io**
- Clean blog-style rendering of Gist markdown
- Pattern: `gist.io/username/gist_id`

### 5. **flatgithub.com**
- Renders CSV/JSON Gists as interactive tables
- Pattern: `flatgithub.com/gist/username/gist_id`
- Good for: BOMs, inventory lists

### 6. **Prose.io + Gist**
- Edit Gists with a nice UI
- Good for: Non-technical collaborators

## PDF Generation Options

### Option A: Pandoc (Local)
```bash
# Convert Gist markdown to PDF
curl -s "https://gist.githubusercontent.com/USER/ID/raw/FILE.md" | \
  pandoc -o output.pdf
```

### Option B: md-to-pdf Service
```bash
# Using a hosted service
curl -X POST https://md-to-pdf.fly.dev \
  -d '{"markdown": "# Title\n\nContent..."}' \
  -o output.pdf
```

### Option C: WeasyPrint (Self-hosted)
```python
from weasyprint import HTML, CSS
HTML(string=markdown_to_html(content)).write_pdf("output.pdf")
```

## Integration Points

1. **Celery workers** - Publish results as Gists
2. **Job completion** - Auto-publish BOMs, reports
3. **Telegram bot** - "Full details: {gist_url}"
4. **Email reports** - Include Gist links
5. **Slack/Discord** - Rich previews from Gist URLs

## Repos to Fork

| Repo | Purpose | Stars |
|------|---------|-------|
| [jonschlinkert/gists](https://github.com/jonschlinkert/gists) | Node.js Gist API wrapper | 150+ |
| [defunkt/gist](https://github.com/defunkt/gist) | Ruby CLI for Gists | 4k+ |
| [jclem/gist.io](https://github.com/jclem/gist.io) | Render Gists as pages | 700+ |
| [nickoala/gist-it](https://github.com/nickoala/gist-it) | Embed file snippets | 200+ |
| [muan/gist-blog](https://github.com/muan/gist-blog) | Blog from Gists | 100+ |

## FactoryLM Convention

All shareable documents follow this pattern:

```
jobs/
  JOB-YYYY-MMDD-NNN/
    README.md          # Auto-published summary
    BOM.md             # Bill of materials
    REPORT.md          # Completion report
    .gist_urls         # Cached Gist URLs
```

When any `.md` file is created in a job folder, it's automatically published and the URL is cached.
