const express = require('express');
const fs = require('fs');
const path = require('path');
const { marked } = require('marked');

const app = express();
const PORT = 3001;
const BRAIN_PATH = '/root/jarvis-workspace/brain';

// Serve static files
app.use(express.static('public'));

// Get all documents
app.get('/api/documents', (req, res) => {
  const documents = [];
  const categories = ['concepts', 'journals', 'research', 'workflows'];
  
  for (const category of categories) {
    const categoryPath = path.join(BRAIN_PATH, category);
    if (fs.existsSync(categoryPath)) {
      const files = fs.readdirSync(categoryPath);
      for (const file of files) {
        if (file.endsWith('.md')) {
          const filePath = path.join(categoryPath, file);
          const stat = fs.statSync(filePath);
          const content = fs.readFileSync(filePath, 'utf-8');
          
          documents.push({
            path: `${category}/${file}`,
            name: file.replace('.md', '').replace(/-/g, ' '),
            category: category.charAt(0).toUpperCase() + category.slice(1),
            content,
            modified: stat.mtime.toISOString()
          });
        }
      }
    }
  }
  
  // Sort by modified date, newest first
  documents.sort((a, b) => new Date(b.modified) - new Date(a.modified));
  res.json(documents);
});

// Get single document as HTML
app.get('/api/documents/:category/:file', (req, res) => {
  const filePath = path.join(BRAIN_PATH, req.params.category, req.params.file + '.md');
  if (fs.existsSync(filePath)) {
    const content = fs.readFileSync(filePath, 'utf-8');
    res.json({ content, html: marked(content) });
  } else {
    res.status(404).json({ error: 'Document not found' });
  }
});

// Main page
app.get('/', (req, res) => {
  res.send(`<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🧠 Second Brain | Jarvis</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
  <style>
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #1a1a2e; }
    ::-webkit-scrollbar-thumb { background: #3d3d5c; border-radius: 4px; }
    ::selection { background: rgba(139, 92, 246, 0.3); }
    .prose h1 { font-size: 1.875rem; font-weight: 700; margin-top: 2rem; margin-bottom: 1rem; color: white; }
    .prose h2 { font-size: 1.5rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.75rem; color: #c4b5fd; }
    .prose h3 { font-size: 1.25rem; font-weight: 600; margin-top: 1rem; margin-bottom: 0.5rem; color: #a78bfa; }
    .prose p { margin-bottom: 1rem; line-height: 1.75; }
    .prose ul, .prose ol { margin-left: 1.5rem; margin-bottom: 1rem; }
    .prose li { margin-bottom: 0.25rem; }
    .prose code { background: #1e1e2e; padding: 0.2rem 0.4rem; border-radius: 4px; font-size: 0.875rem; }
    .prose pre { background: #1e1e2e; padding: 1rem; border-radius: 8px; overflow-x: auto; margin-bottom: 1rem; }
    .prose pre code { background: none; padding: 0; }
    .prose blockquote { border-left: 3px solid #8b5cf6; padding-left: 1rem; color: #9ca3af; font-style: italic; }
    .prose table { width: 100%; border-collapse: collapse; margin-bottom: 1rem; }
    .prose th, .prose td { border: 1px solid #374151; padding: 0.5rem 1rem; text-align: left; }
    .prose th { background: #1f2937; color: white; }
    .prose strong { color: white; }
    .prose a { color: #a78bfa; }
    .prose hr { border-color: #374151; margin: 2rem 0; }
  </style>
</head>
<body class="bg-gray-950 text-gray-300 min-h-screen flex">
  <!-- Sidebar -->
  <div id="sidebar" class="w-72 bg-gray-900 border-r border-gray-800 flex flex-col h-screen fixed">
    <div class="p-4 border-b border-gray-800">
      <h1 class="text-xl font-bold text-white flex items-center gap-2">
        <span class="text-2xl">🧠</span> Second Brain
      </h1>
      <p class="text-xs text-gray-500 mt-1">Jarvis Knowledge Base</p>
    </div>
    <div class="p-3">
      <input type="text" id="search" placeholder="Search documents..." 
        class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-purple-500">
    </div>
    <div id="docList" class="flex-1 overflow-y-auto"></div>
    <div class="p-4 border-t border-gray-800 text-xs text-gray-600">
      <span id="docCount">0</span> documents
    </div>
  </div>

  <!-- Main Content -->
  <div class="flex-1 ml-72">
    <div class="h-14 border-b border-gray-800 flex items-center px-6 bg-gray-900/50 sticky top-0">
      <span class="text-purple-400 mr-2">📄</span>
      <span id="currentDoc" class="font-medium text-white">Select a document</span>
      <span id="currentCategory" class="ml-auto text-xs text-gray-500"></span>
    </div>
    <div id="content" class="p-8 max-w-4xl mx-auto prose"></div>
  </div>

  <script>
    let documents = [];
    let currentDoc = null;

    async function loadDocuments() {
      const res = await fetch('/api/documents');
      documents = await res.json();
      renderDocList();
      document.getElementById('docCount').textContent = documents.length;
      if (documents.length > 0) selectDoc(documents[0]);
    }

    function renderDocList(filter = '') {
      const filtered = documents.filter(d => 
        d.name.toLowerCase().includes(filter.toLowerCase()) ||
        d.content.toLowerCase().includes(filter.toLowerCase())
      );
      
      const categories = [...new Set(filtered.map(d => d.category))];
      let html = '';
      
      for (const cat of categories) {
        html += '<div class="px-4 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider">' + cat + '</div>';
        filtered.filter(d => d.category === cat).forEach(doc => {
          const active = currentDoc?.path === doc.path ? 'bg-gray-800 border-l-2 border-purple-500' : '';
          const date = new Date(doc.modified).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
          html += '<button onclick="selectDoc(documents.find(d=>d.path===\\'' + doc.path + '\\'))" class="w-full text-left px-4 py-2 text-sm hover:bg-gray-800 ' + active + '">' +
            '<div class="font-medium text-gray-200 truncate">' + doc.name.charAt(0).toUpperCase() + doc.name.slice(1) + '</div>' +
            '<div class="text-xs text-gray-500">' + date + '</div></button>';
        });
      }
      
      document.getElementById('docList').innerHTML = html;
    }

    async function selectDoc(doc) {
      currentDoc = doc;
      document.getElementById('currentDoc').textContent = doc.name.charAt(0).toUpperCase() + doc.name.slice(1);
      document.getElementById('currentCategory').textContent = doc.category;
      
      const res = await fetch('/api/documents/' + doc.path.replace('.md', ''));
      const data = await res.json();
      document.getElementById('content').innerHTML = data.html;
      hljs.highlightAll();
      renderDocList(document.getElementById('search').value);
    }

    document.getElementById('search').addEventListener('input', (e) => {
      renderDocList(e.target.value);
    });

    loadDocuments();
    setInterval(loadDocuments, 30000); // Refresh every 30s
  </script>
</body>
</html>`);
});

app.listen(PORT, '0.0.0.0', () => {
  console.log('🧠 Second Brain running at http://localhost:' + PORT);
});
