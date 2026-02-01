/**
 * WhatsApp Web Bridge for Clawdbot
 * Simple version with better error handling
 */

const { default: makeWASocket, DisconnectReason, useMultiFileAuthState, fetchLatestBaileysVersion } = require('@whiskeysockets/baileys');
const express = require('express');
const pino = require('pino');
const qrcode = require('qrcode-terminal');
const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
    apiPort: process.env.BRIDGE_PORT || 3002,
    authFolder: './auth_info'
};

// Create auth folder
if (!fs.existsSync(CONFIG.authFolder)) {
    fs.mkdirSync(CONFIG.authFolder, { recursive: true });
}

// Logger - set to silent to reduce noise
const logger = pino({ level: 'silent' });

// Express app
const app = express();
app.use(express.json());

// Global state
let sock = null;
let qrCode = null;
let connectionStatus = 'disconnected';

async function connectToWhatsApp() {
    try {
        console.log('🔄 Attempting to connect to WhatsApp...');
        
        // Get latest version
        const { version, isLatest } = await fetchLatestBaileysVersion();
        console.log(`📦 Using Baileys version: ${version.join('.')}, isLatest: ${isLatest}`);
        
        const { state, saveCreds } = await useMultiFileAuthState(CONFIG.authFolder);
        
        sock = makeWASocket({
            version,
            logger,
            printQRInTerminal: false,
            auth: state,
            browser: ['ShopTalk', 'Chrome', '120.0.0']
        });
        
        // Handle connection updates
        sock.ev.on('connection.update', async (update) => {
            const { connection, lastDisconnect, qr } = update;
            
            console.log('📡 Connection update:', { connection, hasQR: !!qr });
            
            if (qr) {
                qrCode = qr;
                connectionStatus = 'waiting_for_scan';
                console.log('\n========================================');
                console.log('📱 SCAN THIS QR CODE WITH WHATSAPP');
                console.log('========================================\n');
                qrcode.generate(qr, { small: true });
                console.log('\nWhatsApp > Settings > Linked Devices > Link a Device');
                console.log(`\nOr open: http://localhost:${CONFIG.apiPort}/qr`);
                console.log('========================================\n');
            }
            
            if (connection === 'close') {
                connectionStatus = 'disconnected';
                const statusCode = lastDisconnect?.error?.output?.statusCode;
                const reason = lastDisconnect?.error?.output?.payload?.message || 'unknown';
                console.log(`❌ Connection closed: ${reason} (code: ${statusCode})`);
                
                if (statusCode !== DisconnectReason.loggedOut) {
                    console.log('🔄 Reconnecting in 5 seconds...');
                    setTimeout(connectToWhatsApp, 5000);
                } else {
                    console.log('🚪 Logged out. Clear auth folder and restart to re-link.');
                }
            } else if (connection === 'open') {
                qrCode = null;
                connectionStatus = 'connected';
                const phoneNumber = sock.user?.id?.split(':')[0] || 'unknown';
                console.log('\n✅ WHATSAPP CONNECTED!');
                console.log(`📞 Connected number: ${phoneNumber}`);
                console.log(`🌐 API: http://localhost:${CONFIG.apiPort}`);
                console.log('\n📨 Waiting for messages...\n');
            }
        });
        
        // Save credentials
        sock.ev.on('creds.update', saveCreds);
        
        // Handle messages
        sock.ev.on('messages.upsert', async ({ messages, type }) => {
            if (type !== 'notify') return;
            
            for (const msg of messages) {
                if (msg.key.fromMe) continue;
                
                const from = msg.key.remoteJid;
                const phoneNumber = from?.split('@')[0] || 'unknown';
                const text = msg.message?.conversation 
                    || msg.message?.extendedTextMessage?.text 
                    || '';
                
                if (!text) continue;
                
                console.log(`\n📨 Message from ${phoneNumber}:`);
                console.log(`   "${text}"`);
                
                // Simple echo for testing
                if (text.toLowerCase() === 'ping') {
                    await sock.sendMessage(from, { text: '🏓 Pong! ShopTalk bridge is working.' });
                    console.log('   ↳ Replied with pong');
                }
            }
        });
        
    } catch (err) {
        console.error('❌ Connection error:', err.message);
        console.log('🔄 Retrying in 10 seconds...');
        setTimeout(connectToWhatsApp, 10000);
    }
}

// API Routes
app.post('/send', async (req, res) => {
    const { to, message } = req.body;
    
    if (connectionStatus !== 'connected') {
        return res.status(503).json({ error: 'WhatsApp not connected', status: connectionStatus });
    }
    
    if (!to || !message) {
        return res.status(400).json({ error: 'Missing "to" or "message"' });
    }
    
    try {
        const jid = to.includes('@') ? to : `${to.replace(/\D/g, '')}@s.whatsapp.net`;
        await sock.sendMessage(jid, { text: message });
        console.log(`📤 Sent to ${to}: ${message.substring(0, 50)}...`);
        res.json({ success: true });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.get('/qr', (req, res) => {
    if (!qrCode) {
        const html = `
        <!DOCTYPE html>
        <html>
        <head><title>WhatsApp Bridge</title><meta http-equiv="refresh" content="3"></head>
        <body style="display:flex;justify-content:center;align-items:center;height:100vh;background:#1a1a2e;color:white;font-family:sans-serif;">
            <div style="text-align:center;">
                <h1>${connectionStatus === 'connected' ? '✅ Connected!' : '⏳ Waiting for QR...'}</h1>
                <p>Status: ${connectionStatus}</p>
                <p>Page will refresh automatically...</p>
            </div>
        </body>
        </html>`;
        return res.send(html);
    }
    
    const html = `
    <!DOCTYPE html>
    <html>
    <head><title>Scan QR Code</title></head>
    <body style="display:flex;justify-content:center;align-items:center;height:100vh;background:#1a1a2e;color:white;font-family:sans-serif;">
        <div style="text-align:center;">
            <h1>📱 Scan with WhatsApp</h1>
            <img src="https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=${encodeURIComponent(qrCode)}" />
            <p>Open WhatsApp → Settings → Linked Devices → Link a Device</p>
        </div>
    </body>
    </html>`;
    res.send(html);
});

app.get('/health', (req, res) => {
    res.json({ 
        status: connectionStatus,
        connected: connectionStatus === 'connected',
        number: sock?.user?.id?.split(':')[0] || null,
        needsQR: connectionStatus === 'waiting_for_scan'
    });
});

app.get('/', (req, res) => {
    res.redirect('/qr');
});

// Start
async function main() {
    console.log('========================================');
    console.log('🔌 WhatsApp Bridge for Clawdbot');
    console.log('========================================\n');
    
    app.listen(CONFIG.apiPort, '0.0.0.0', () => {
        console.log(`🌐 Web interface: http://localhost:${CONFIG.apiPort}`);
        console.log(`📱 QR code page: http://localhost:${CONFIG.apiPort}/qr\n`);
    });
    
    await connectToWhatsApp();
}

main().catch(console.error);
