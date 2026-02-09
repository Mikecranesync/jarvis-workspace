/**
 * Second Brain Portal Server
 * Secure document management system for Jarvis workspace
 * 
 * @author Jarvis QA Agent
 * @version 1.1.0
 * @port 3001
 */

const express = require('express');
const fs = require('fs').promises;
const fsSync = require('fs');
const path = require('path');
const { marked } = require('marked');
const DOMPurify = require('isomorphic-dompurify');

const app = express();
const PORT = 3001;
const BRAIN_PATH = '/root/jarvis-workspace/brain';
const WORKSPACE_PATH = '/root/jarvis-workspace';

// Security: Allowed categories and file name validation
const ALLOWED_CATEGORIES = ['concepts', 'journals', 'research', 'workflows'];
const WORKSPACE_FILES = ['MEMORY.md', 'CONSTITUTION.md', 'ENGINEERING_COMMANDMENTS.md', 'AGENTS.md', 'SOUL.md', 'USER.md'];

app.use(express.json({ limit: '10mb' }));
app.use(express.static('public'));

/**
 * Validates and sanitizes category name
 * @param {string} category - Category name to validate
 * @returns {boolean} True if valid category
 */
function isValidCategory(category) {
  return ALLOWED_CATEGORIES.includes(category);
}

/**
 * Validates and sanitizes file name
 * Prevents path traversal attacks
 * @param {string} filename - Filename to validate
 * @returns {boolean} True if valid filename
 */
function isValidFilename(filename) {
  // Only allow alphanumeric, hyphens, underscores
  const sanitized = filename.replace(/[^a-zA-Z0-9\-_]/g, '');
  return sanitized === filename && filename.length > 0 && filename.length < 100;
}

/**
 * Safely constructs file path within brain directory
 * @param {string} category - Document category
 * @param {string} filename - Document filename (without .md)
 * @returns {string|null} Safe file path or null if invalid
 */
function getSafeFilePath(category, filename) {
  if (!isValidCategory(category) || !isValidFilename(filename)) {
    return null;
  }
  
  const safePath = path.join(BRAIN_PATH, category, filename + '.md');
  
  // Ensure path is still within BRAIN_PATH (prevent directory traversal)
  const normalizedPath = path.resolve(safePath);
  const normalizedBrainPath = path.resolve(BRAIN_PATH);
  
  if (!normalizedPath.startsWith(normalizedBrainPath)) {
    return null;
  }
  
  return safePath;
}

/**
 * Safely constructs workspace file path
 * @param {string} filename - Workspace filename
 * @returns {string|null} Safe file path or null if invalid
 */
function getSafeWorkspacePath(filename) {
  if (!WORKSPACE_FILES.includes(filename)) {
    return null;
  }
  
  return path.join(WORKSPACE_PATH, filename);
}

/**
 * Sanitizes HTML content to prevent XSS
 * @param {string} html - HTML content to sanitize
 * @returns {string} Sanitized HTML
 */
function sanitizeHtml(html) {
  return DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'br', 'strong', 'em', 'code', 'pre', 'ul', 'ol', 'li', 'a', 'blockquote', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'hr'],
    ALLOWED_ATTR: ['href', 'title']
  });
}

/**
 * Error response helper
 * @param {object} res - Express response object
 * @param {number} status - HTTP status code
 * @param {string} message - Error message
 * @param {object} details - Optional error details
 */
function sendError(res, status, message, details = {}) {
  console.error(`[${new Date().toISOString()}] Error ${status}: ${message}`, details);
  res.status(status).json({ 
    error: message,
    timestamp: new Date().toISOString()
  });
}

/**
 * Get all documents from brain directory
 * @route GET /api/documents
 */
app.get('/api/documents', async (req, res) => {
  try {
    const documents = [];
    
    for (const category of ALLOWED_CATEGORIES) {
      const categoryPath = path.join(BRAIN_PATH, category);
      
      try {
        await fs.access(categoryPath);
        const files = await fs.readdir(categoryPath);
        
        for (const file of files) {
          if (file.endsWith('.md') && isValidFilename(file.replace('.md', ''))) {
            const filePath = path.join(categoryPath, file);
            
            try {
              const stat = await fs.stat(filePath);
              const content = await fs.readFile(filePath, 'utf-8');
              
              documents.push({
                path: `${category}/${file}`,
                name: file.replace('.md', '').replace(/-/g, ' '),
                category: category.charAt(0).toUpperCase() + category.slice(1),
                content,
                modified: stat.mtime.toISOString(),
                size: stat.size
              });
            } catch (fileError) {
              console.warn(`Error reading file ${filePath}:`, fileError.message);
              continue;
            }
          }
        }
      } catch (dirError) {
        // Category directory doesn't exist, skip
        continue;
      }
    }
    
    documents.sort((a, b) => new Date(b.modified) - new Date(a.modified));
    res.json(documents);
    
  } catch (error) {
    sendError(res, 500, 'Failed to load documents', { error: error.message });
  }
});

/**
 * Get single document by category and filename
 * @route GET /api/documents/:category/:file
 */
app.get('/api/documents/:category/:file', async (req, res) => {
  try {
    const { category, file } = req.params;
    const filePath = getSafeFilePath(category, file);
    
    if (!filePath) {
      return sendError(res, 400, 'Invalid category or filename');
    }
    
    try {
      await fs.access(filePath);
      const content = await fs.readFile(filePath, 'utf-8');
      const html = sanitizeHtml(marked.parse(content));
      
      res.json({ 
        content, 
        html,
        path: `${category}/${file}`,
        lastModified: (await fs.stat(filePath)).mtime.toISOString()
      });
      
    } catch (fileError) {
      if (fileError.code === 'ENOENT') {
        sendError(res, 404, 'Document not found');
      } else {
        sendError(res, 500, 'Failed to read document', { error: fileError.message });
      }
    }
    
  } catch (error) {
    sendError(res, 500, 'Server error', { error: error.message });
  }
});

/**
 * Create or update document
 * @route POST /api/documents/:category/:file
 */
app.post('/api/documents/:category/:file', async (req, res) => {
  try {
    const { category, file } = req.params;
    const { content } = req.body;
    
    // Validate input
    if (typeof content !== 'string') {
      return sendError(res, 400, 'Content must be a string');
    }
    
    if (content.length > 1000000) { // 1MB limit
      return sendError(res, 400, 'Content too large (max 1MB)');
    }
    
    const categoryPath = path.join(BRAIN_PATH, category);
    const filePath = getSafeFilePath(category, file);
    
    if (!filePath) {
      return sendError(res, 400, 'Invalid category or filename');
    }
    
    // Create category directory if needed
    try {
      await fs.access(categoryPath);
    } catch {
      await fs.mkdir(categoryPath, { recursive: true });
    }
    
    // Write file
    await fs.writeFile(filePath, content, 'utf-8');
    
    res.json({ 
      success: true, 
      path: `${category}/${file}`,
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    sendError(res, 500, 'Failed to save document', { error: error.message });
  }
});

/**
 * Delete document
 * @route DELETE /api/documents/:category/:file
 */
app.delete('/api/documents/:category/:file', async (req, res) => {
  try {
    const { category, file } = req.params;
    const filePath = getSafeFilePath(category, file);
    
    if (!filePath) {
      return sendError(res, 400, 'Invalid category or filename');
    }
    
    try {
      await fs.access(filePath);
      await fs.unlink(filePath);
      res.json({ 
        success: true,
        deleted: `${category}/${file}`,
        timestamp: new Date().toISOString()
      });
      
    } catch (fileError) {
      if (fileError.code === 'ENOENT') {
        sendError(res, 404, 'Document not found');
      } else {
        sendError(res, 500, 'Failed to delete document', { error: fileError.message });
      }
    }
    
  } catch (error) {
    sendError(res, 500, 'Server error', { error: error.message });
  }
});

/**
 * Get workspace files (read-only)
 * @route GET /api/workspace
 */
app.get('/api/workspace', async (req, res) => {
  try {
    const docs = [];
    
    for (const filename of WORKSPACE_FILES) {
      const filePath = getSafeWorkspacePath(filename);
      
      if (!filePath) continue;
      
      try {
        await fs.access(filePath);
        const stat = await fs.stat(filePath);
        const content = await fs.readFile(filePath, 'utf-8');
        
        docs.push({
          path: filename,
          name: filename.replace('.md', ''),
          content,
          modified: stat.mtime.toISOString(),
          size: stat.size
        });
        
      } catch (fileError) {
        // File doesn't exist, skip
        continue;
      }
    }
    
    res.json(docs);
    
  } catch (error) {
    sendError(res, 500, 'Failed to load workspace files', { error: error.message });
  }
});

/**
 * Get system status (safe system information only)
 * @route GET /api/status
 */
app.get('/api/status', async (req, res) => {
  try {
    const status = {
      timestamp: new Date().toISOString(),
      server: 'second-brain',
      port: PORT
    };
    
    // Safe system information
    try {
      const uptimeData = await fs.readFile('/proc/uptime', 'utf-8');
      const uptimeSeconds = parseFloat(uptimeData.split(' ')[0]);
      status.uptime = Math.floor(uptimeSeconds / 3600) + 'h';
    } catch {
      status.uptime = 'N/A';
    }
    
    try {
      const meminfo = await fs.readFile('/proc/meminfo', 'utf-8');
      const memTotalMatch = meminfo.match(/MemTotal:\s+(\d+)/);
      const memAvailMatch = meminfo.match(/MemAvailable:\s+(\d+)/);
      
      if (memTotalMatch && memAvailMatch) {
        const memTotal = parseInt(memTotalMatch[1]) / 1024;
        const memAvail = parseInt(memAvailMatch[1]) / 1024;
        
        status.memory = {
          total: Math.round(memTotal) + 'MB',
          available: Math.round(memAvail) + 'MB',
          used: Math.round(((memTotal - memAvail) / memTotal) * 100) + '%'
        };
      }
    } catch {
      status.memory = { error: 'Unable to read memory info' };
    }
    
    // Document counts
    try {
      let totalDocs = 0;
      for (const category of ALLOWED_CATEGORIES) {
        const categoryPath = path.join(BRAIN_PATH, category);
        try {
          const files = await fs.readdir(categoryPath);
          totalDocs += files.filter(f => f.endsWith('.md')).length;
        } catch {
          // Directory doesn't exist, skip
        }
      }
      status.documents = totalDocs;
    } catch {
      status.documents = 'N/A';
    }
    
    res.json(status);
    
  } catch (error) {
    sendError(res, 500, 'Failed to get system status', { error: error.message });
  }
});

/**
 * Health check endpoint
 * @route GET /health
 */
app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

/**
 * Main page - serves the web interface
 * @route GET /
 */
app.get('/', (req, res) => {
  res.send(`<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🧠 Jarvis Portal</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
  <style>
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #0f0f17; }
    ::-webkit-scrollbar-thumb { background: #3d3d5c; border-radius: 4px; }
    ::selection { background: rgba(139, 92, 246, 0.3); }
    .prose h1 { font-size: 1.875rem; font-weight: 700; margin-top: 1.5rem; margin-bottom: 0.75rem; color: white; }
    .prose h2 { font-size: 1.5rem; font-weight: 600; margin-top: 1.25rem; margin-bottom: 0.5rem; color: #c4b5fd; }
    .prose h3 { font-size: 1.25rem; font-weight: 600; margin-top: 1rem; margin-bottom: 0.5rem; color: #a78bfa; }
    .prose p { margin-bottom: 0.75rem; line-height: 1.7; }
    .prose ul, .prose ol { margin-left: 1.5rem; margin-bottom: 0.75rem; }
    .prose li { margin-bottom: 0.25rem; }
    .prose code { background: #1e1e2e; padding: 0.15rem 0.35rem; border-radius: 4px; font-size: 0.85rem; color: #a6e3a1; }
    .prose pre { background: #1e1e2e; padding: 1rem; border-radius: 8px; overflow-x: auto; margin-bottom: 1rem; }
    .prose pre code { background: none; padding: 0; }
    .prose blockquote { border-left: 3px solid #8b5cf6; padding-left: 1rem; color: #9ca3af; font-style: italic; margin: 1rem 0; }
    .prose table { width: 100%; border-collapse: collapse; margin-bottom: 1rem; font-size: 0.9rem; }
    .prose th, .prose td { border: 1px solid #374151; padding: 0.5rem; text-align: left; }
    .prose th { background: #1f2937; color: white; }
    .prose strong { color: white; }
    .prose a { color: #a78bfa; }
    .prose hr { border-color: #374151; margin: 1.5rem 0; }
    .tab-active { background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%); }
    .glow { box-shadow: 0 0 20px rgba(139, 92, 246, 0.3); }
    @keyframes pulse-glow { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
    .status-active { animation: pulse-glow 2s infinite; }
    .error-toast { position: fixed; top: 1rem; right: 1rem; background: #dc2626; color: white; padding: 1rem; border-radius: 0.5rem; z-index: 1000; }
  </style>
</head>
<body class="bg-[#0a0a0f] text-gray-300 min-h-screen">
  <div class="flex h-screen">
    <!-- Sidebar -->
    <div id="sidebar" class="w-64 bg-[#12121a] border-r border-gray-800/50 flex flex-col">
      <!-- Logo -->
      <div class="p-4 border-b border-gray-800/50">
        <h1 class="text-xl font-bold text-white flex items-center gap-2">
          <span class="text-2xl">🧠</span> Jarvis
        </h1>
        <p class="text-xs text-gray-500 mt-1">Second Brain Portal v1.1</p>
      </div>

      <!-- Navigation -->
      <nav class="p-2">
        <button onclick="setTab('documents')" id="tab-documents" class="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm hover:bg-gray-800/50 tab-active text-white mb-1">
          📄 Documents
        </button>
        <button onclick="setTab('workspace')" id="tab-workspace" class="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm hover:bg-gray-800/50 text-gray-400 mb-1">
          ⚙️ Workspace
        </button>
        <button onclick="setTab('status')" id="tab-status" class="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm hover:bg-gray-800/50 text-gray-400 mb-1">
          📊 Status
        </button>
      </nav>

      <!-- Search -->
      <div class="p-2">
        <input type="text" id="search" placeholder="Search..." 
          class="w-full bg-gray-900/50 border border-gray-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-purple-500/50">
      </div>

      <!-- Document List -->
      <div id="docList" class="flex-1 overflow-y-auto p-2"></div>

      <!-- Footer -->
      <div class="p-3 border-t border-gray-800/50 text-xs text-gray-600">
        <span id="docCount">0</span> docs • <span id="lastRefresh">--</span>
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col">
      <!-- Top Bar -->
      <div class="h-12 border-b border-gray-800/50 flex items-center justify-between px-4 bg-[#12121a]/50">
        <div class="flex items-center gap-2">
          <span id="currentIcon" class="text-purple-400">📄</span>
          <span id="currentDoc" class="font-medium text-white text-sm">Select a document</span>
        </div>
        <div class="flex items-center gap-2">
          <button onclick="toggleEdit()" id="editBtn" class="px-3 py-1 text-xs bg-gray-800 hover:bg-gray-700 rounded-lg hidden">
            ✏️ Edit
          </button>
          <button onclick="newDoc()" class="px-3 py-1 text-xs bg-purple-600 hover:bg-purple-500 rounded-lg text-white">
            + New
          </button>
        </div>
      </div>

      <!-- Content Area -->
      <div id="content" class="flex-1 overflow-y-auto p-6">
        <div class="max-w-4xl mx-auto prose"></div>
      </div>

      <!-- Editor (hidden by default) -->
      <div id="editor" class="flex-1 overflow-hidden hidden flex flex-col">
        <textarea id="editorArea" class="flex-1 bg-[#0a0a0f] p-6 text-gray-300 font-mono text-sm resize-none focus:outline-none"></textarea>
        <div class="p-3 border-t border-gray-800/50 flex justify-end gap-2 bg-[#12121a]">
          <button onclick="cancelEdit()" class="px-4 py-2 text-sm bg-gray-800 hover:bg-gray-700 rounded-lg">Cancel</button>
          <button onclick="saveDoc()" class="px-4 py-2 text-sm bg-purple-600 hover:bg-purple-500 rounded-lg text-white">Save</button>
        </div>
      </div>
    </div>
  </div>

  <script>
    let documents = [];
    let workspaceFiles = [];
    let currentDoc = null;
    let currentTab = 'documents';
    let isEditing = false;

    function showError(message) {
      const toast = document.createElement('div');
      toast.className = 'error-toast';
      toast.textContent = message;
      document.body.appendChild(toast);
      setTimeout(() => toast.remove(), 5000);
    }

    async function apiCall(url, options = {}) {
      try {
        const response = await fetch(url, options);
        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.error || 'Request failed');
        }
        return await response.json();
      } catch (error) {
        showError(error.message);
        throw error;
      }
    }

    async function loadDocuments() {
      try {
        documents = await apiCall('/api/documents');
        if (currentTab === 'documents') renderDocList();
        document.getElementById('docCount').textContent = documents.length;
        document.getElementById('lastRefresh').textContent = new Date().toLocaleTimeString();
      } catch (error) {
        console.error('Failed to load documents:', error);
      }
    }

    async function loadWorkspace() {
      try {
        workspaceFiles = await apiCall('/api/workspace');
        if (currentTab === 'workspace') renderWorkspaceList();
      } catch (error) {
        console.error('Failed to load workspace:', error);
      }
    }

    async function loadStatus() {
      try {
        const status = await apiCall('/api/status');
        
        const content = document.querySelector('#content .prose');
        content.innerHTML = \`
          <h1>📊 System Status</h1>
          <div class="grid grid-cols-2 gap-4 mt-6">
            <div class="bg-gray-900/50 p-4 rounded-xl border border-gray-800/50">
              <div class="text-xs text-gray-500 mb-1">Uptime</div>
              <div class="text-2xl font-bold text-white">\${status.uptime || 'N/A'}</div>
            </div>
            <div class="bg-gray-900/50 p-4 rounded-xl border border-gray-800/50">
              <div class="text-xs text-gray-500 mb-1">Memory</div>
              <div class="text-2xl font-bold text-white">\${status.memory?.used || 'N/A'}</div>
              <div class="text-xs text-gray-500">\${status.memory?.available || ''} available</div>
            </div>
            <div class="bg-gray-900/50 p-4 rounded-xl border border-gray-800/50">
              <div class="text-xs text-gray-500 mb-1">Documents</div>
              <div class="text-2xl font-bold text-white">\${status.documents || 0}</div>
            </div>
            <div class="bg-gray-900/50 p-4 rounded-xl border border-gray-800/50">
              <div class="text-xs text-gray-500 mb-1">Server</div>
              <div class="text-2xl font-bold text-green-400">Active</div>
              <div class="text-xs text-gray-500">Port \${status.port}</div>
            </div>
          </div>
          <h2 class="mt-6">Last Updated</h2>
          <p class="text-gray-400">\${new Date(status.timestamp).toLocaleString()}</p>
        \`;
      } catch (error) {
        console.error('Failed to load status:', error);
      }
    }

    function renderDocList(filter = '') {
      const filtered = documents.filter(d => 
        d.name.toLowerCase().includes(filter.toLowerCase()) ||
        d.content.toLowerCase().includes(filter.toLowerCase())
      );
      
      const categories = [...new Set(filtered.map(d => d.category))];
      let html = '';
      
      for (const cat of categories) {
        html += '<div class="text-[10px] font-semibold text-gray-500 uppercase tracking-wider px-2 py-1 mt-2">' + cat + '</div>';
        filtered.filter(d => d.category === cat).forEach(doc => {
          const active = currentDoc?.path === doc.path ? 'bg-purple-600/20 border-l-2 border-purple-500' : 'hover:bg-gray-800/50';
          html += '<button onclick="selectDoc(\\'' + doc.path + '\\')" class="w-full text-left px-2 py-1.5 text-sm rounded-r ' + active + '">' +
            '<div class="font-medium text-gray-200 truncate text-xs">' + doc.name.charAt(0).toUpperCase() + doc.name.slice(1) + '</div>' +
            '</button>';
        });
      }
      
      document.getElementById('docList').innerHTML = html;
    }

    function renderWorkspaceList() {
      let html = '<div class="text-[10px] font-semibold text-gray-500 uppercase tracking-wider px-2 py-1 mt-2">Core Files</div>';
      
      workspaceFiles.forEach(doc => {
        const active = currentDoc?.path === doc.path ? 'bg-purple-600/20 border-l-2 border-purple-500' : 'hover:bg-gray-800/50';
        html += '<button onclick="selectWorkspaceFile(\\'' + doc.path + '\\')" class="w-full text-left px-2 py-1.5 text-sm rounded-r ' + active + '">' +
          '<div class="font-medium text-gray-200 truncate text-xs">' + doc.name + '</div>' +
          '</button>';
      });
      
      document.getElementById('docList').innerHTML = html;
    }

    async function selectDoc(docPath) {
      try {
        currentDoc = documents.find(d => d.path === docPath);
        if (!currentDoc) return;
        
        document.getElementById('currentDoc').textContent = currentDoc.name.charAt(0).toUpperCase() + currentDoc.name.slice(1);
        document.getElementById('editBtn').classList.remove('hidden');
        
        const [cat, file] = docPath.split('/');
        const data = await apiCall('/api/documents/' + cat + '/' + file.replace('.md', ''));
        
        document.querySelector('#content .prose').innerHTML = data.html;
        hljs.highlightAll();
        renderDocList(document.getElementById('search').value);
        
        if (isEditing) cancelEdit();
      } catch (error) {
        console.error('Failed to load document:', error);
      }
    }

    function selectWorkspaceFile(path) {
      currentDoc = workspaceFiles.find(d => d.path === path);
      if (!currentDoc) return;
      
      document.getElementById('currentDoc').textContent = currentDoc.name;
      document.getElementById('editBtn').classList.add('hidden');
      
      const html = marked.parse(currentDoc.content);
      document.querySelector('#content .prose').innerHTML = html;
      hljs.highlightAll();
      renderWorkspaceList();
    }

    function setTab(tab) {
      currentTab = tab;
      currentDoc = null;
      
      document.querySelectorAll('[id^="tab-"]').forEach(el => {
        el.classList.remove('tab-active', 'text-white');
        el.classList.add('text-gray-400');
      });
      document.getElementById('tab-' + tab).classList.add('tab-active', 'text-white');
      document.getElementById('tab-' + tab).classList.remove('text-gray-400');
      
      document.getElementById('editBtn').classList.add('hidden');
      document.getElementById('currentDoc').textContent = 'Select a document';
      document.querySelector('#content .prose').innerHTML = '';
      
      if (tab === 'documents') {
        renderDocList();
      } else if (tab === 'workspace') {
        loadWorkspace();
      } else if (tab === 'status') {
        document.getElementById('docList').innerHTML = '';
        loadStatus();
      }
    }

    function toggleEdit() {
      if (!currentDoc) return;
      isEditing = true;
      document.getElementById('content').classList.add('hidden');
      document.getElementById('editor').classList.remove('hidden');
      document.getElementById('editorArea').value = currentDoc.content;
      document.getElementById('editBtn').textContent = '👁️ Preview';
    }

    function cancelEdit() {
      isEditing = false;
      document.getElementById('content').classList.remove('hidden');
      document.getElementById('editor').classList.add('hidden');
      document.getElementById('editBtn').textContent = '✏️ Edit';
    }

    async function saveDoc() {
      try {
        if (!currentDoc) return;
        const content = document.getElementById('editorArea').value;
        const [cat, file] = currentDoc.path.split('/');
        
        await apiCall('/api/documents/' + cat + '/' + file.replace('.md', ''), {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ content })
        });
        
        currentDoc.content = content;
        cancelEdit();
        await loadDocuments();
        selectDoc(currentDoc.path);
      } catch (error) {
        console.error('Failed to save document:', error);
      }
    }

    function newDoc() {
      const name = prompt('Document name (e.g., my-notes):');
      if (!name || !/^[a-zA-Z0-9\\-_]+$/.test(name)) {
        showError('Invalid name. Use only letters, numbers, hyphens and underscores.');
        return;
      }
      
      const category = prompt('Category (concepts, journals, research, workflows):', 'concepts');
      if (!['concepts', 'journals', 'research', 'workflows'].includes(category)) {
        showError('Invalid category.');
        return;
      }
      
      const path = category + '/' + name.toLowerCase() + '.md';
      currentDoc = { path, name, category, content: '# ' + name + '\\n\\nWrite your content here...' };
      
      document.getElementById('currentDoc').textContent = name;
      document.getElementById('editBtn').classList.remove('hidden');
      toggleEdit();
    }

    marked.setOptions({ breaks: true, gfm: true });

    document.getElementById('search').addEventListener('input', (e) => {
      if (currentTab === 'documents') renderDocList(e.target.value);
    });

    // Initial load
    loadDocuments();
    setInterval(loadDocuments, 30000);
  </script>
</body>
</html>`);
});

/**
 * 404 handler
 */
app.use((req, res) => {
  sendError(res, 404, 'Not found');
});

/**
 * Global error handler
 */
app.use((error, req, res, next) => {
  console.error('[Global Error]', error);
  sendError(res, 500, 'Internal server error');
});

/**
 * Start server
 */
app.listen(PORT, '0.0.0.0', () => {
  console.log(`🧠 Jarvis Portal v1.1.0 running at http://localhost:${PORT}`);
  console.log(`Security: Enhanced validation and sanitization enabled`);
  console.log(`Time: ${new Date().toISOString()}`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('SIGINT received, shutting down gracefully');
  process.exit(0);
});