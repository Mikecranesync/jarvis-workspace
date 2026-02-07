/**
 * Claude Code + Playwright MCP Debug Script
 * Run with: npx playwright test debug-docs-site.js
 * Or use in Claude Code with Playwright MCP
 */

const { chromium } = require('playwright');

async function debugDocsSite() {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  // URL to test - change this to your docs site URL
  const baseUrl = 'http://localhost:8000'; // MkDocs default
  // const baseUrl = 'https://factorylm.com'; // or production
  
  console.log('🔍 Starting FactoryLM Docs Site Audit...\n');
  
  // Navigate to home page
  await page.goto(baseUrl);
  console.log(`✅ Loaded: ${baseUrl}`);
  
  // Find all links on the page
  const links = await page.$$eval('a[href]', anchors => 
    anchors.map(a => ({
      text: a.textContent.trim().substring(0, 50),
      href: a.href,
      isInternal: a.href.includes(location.host)
    }))
  );
  
  console.log(`\n📋 Found ${links.length} links on homepage\n`);
  
  // Test each internal link
  const broken = [];
  const working = [];
  
  for (const link of links.filter(l => l.isInternal)) {
    try {
      const response = await page.goto(link.href, { timeout: 5000 });
      if (response.status() === 404 || response.status() >= 400) {
        broken.push({ ...link, status: response.status() });
        console.log(`❌ BROKEN: ${link.text} → ${link.href} (${response.status()})`);
      } else {
        working.push(link);
        console.log(`✅ OK: ${link.text}`);
      }
    } catch (err) {
      broken.push({ ...link, error: err.message });
      console.log(`❌ ERROR: ${link.text} → ${err.message}`);
    }
  }
  
  // Summary
  console.log('\n' + '='.repeat(50));
  console.log('📊 SUMMARY');
  console.log('='.repeat(50));
  console.log(`✅ Working links: ${working.length}`);
  console.log(`❌ Broken links: ${broken.length}`);
  
  if (broken.length > 0) {
    console.log('\n🔴 BROKEN LINKS:');
    broken.forEach(b => console.log(`  - ${b.text}: ${b.href}`));
  }
  
  await browser.close();
  return { working, broken };
}

// Run it
debugDocsSite().catch(console.error);
