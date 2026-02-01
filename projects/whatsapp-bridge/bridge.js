/**
 * WhatsApp Web Bridge for Clawdbot
 * 
 * Connects to WhatsApp via QR code and forwards messages to Clawdbot.
 * Run: npm start
 * Then scan the QR code with your phone.
 */

import pkg from '@whiskeysockets/baileys';
const { 
    default: makeWASocket, 
    DisconnectReason, 
    useMultiFileAuthState 
} = pkg;
// Boom is built into baileys
import express from 'express';
import pino from 'pino';
import qrcode from 'qrcode-terminal';
import fs from 'fs';

// Configuration
const CONFIG = {
    // Clawdbot webhook (we'll set this up)
    clawdbotWebhook: process.env.CLAWDBOT_WEBHOOK || 'http://localhost:18789/webhook/whatsapp',
    clawdbotToken: process.env.CLAWDBOT_TOKEN || 'e4d794504a4e47459ac08b26f5c668677aae6088d7f6a841',
    
    // Bridge API port
    apiPort: process.env.BRIDGE_PORT || 3001,
    
    // Auth storage
    authFolder: './auth_info',
    
    // Allowed numbers (empty = all)
    allowedNumbers: process.env.ALLOWED_NUMBERS?.split(',') || []
};

// Logger
const logger = pino({ level: 'info' });

// Express app for sending messages
const app = express();
app.use(express.json());

// Simple message cache
const messageCache = new Map();

// Global socket reference
let sock = null;

async function connectToWhatsApp() {
    const { state, saveCreds } = await useMultiFileAuthState(CONFIG.authFolder);
    
    sock = makeWASocket({
        logger,
        printQRInTerminal: false,  // We'll handle QR ourselves
        auth: state,
        getMessage: async (key) => {
            return messageCache.get(key.id)?.message || undefined;
        }
    });
    
    // Handle connection updates
    sock.ev.on('connection.update', async (update) => {
        const { connection, lastDisconnect, qr } = update;
        
        if (qr) {
            console.log('\n========================================');
            console.log('📱 SCAN THIS QR CODE WITH WHATSAPP');
            console.log('========================================\n');
            qrcode.generate(qr, { small: true });
            console.log('\nOpen WhatsApp > Settings > Linked Devices > Link a Device');
            console.log('========================================\n');
        }
        
        if (connection === 'close') {
            const statusCode = lastDisconnect?.error?.output?.statusCode;
            const shouldReconnect = statusCode !== DisconnectReason.loggedOut;
            
            console.log('Connection closed due to', lastDisconnect?.error, ', reconnecting:', shouldReconnect);
            
            if (shouldReconnect) {
                setTimeout(connectToWhatsApp, 3000);
            }
        } else if (connection === 'open') {
            console.log('\n✅ WHATSAPP CONNECTED!');
            console.log(`📞 Your number: ${sock.user?.id?.split(':')[0]}`);
            console.log(`\n🌐 Bridge API running on http://localhost:${CONFIG.apiPort}`);
            console.log('\nReady to receive messages!\n');
        }
    });
    
    // Save credentials on update
    sock.ev.on('creds.update', saveCreds);
    
    // Handle incoming messages
    sock.ev.on('messages.upsert', async ({ messages, type }) => {
        if (type !== 'notify') return;
        
        for (const msg of messages) {
            if (msg.key.fromMe) continue;  // Skip our own messages
            
            const from = msg.key.remoteJid;
            const phoneNumber = from.split('@')[0];
            
            // Check allowlist
            if (CONFIG.allowedNumbers.length > 0 && !CONFIG.allowedNumbers.includes(phoneNumber)) {
                console.log(`Ignored message from non-allowed number: ${phoneNumber}`);
                continue;
            }
            
            // Extract message text
            const text = msg.message?.conversation 
                || msg.message?.extendedTextMessage?.text 
                || msg.message?.imageMessage?.caption
                || '';
            
            if (!text) continue;
            
            console.log(`\n📨 Message from ${phoneNumber}: ${text.substring(0, 50)}...`);
            
            // Forward to Clawdbot
            try {
                const response = await fetch(CONFIG.clawdbotWebhook, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${CONFIG.clawdbotToken}`
                    },
                    body: JSON.stringify({
                        channel: 'whatsapp',
                        from: phoneNumber,
                        fromName: msg.pushName || phoneNumber,
                        text: text,
                        messageId: msg.key.id,
                        timestamp: msg.messageTimestamp
                    })
                });
                
                if (response.ok) {
                    console.log(`✅ Forwarded to Clawdbot`);
                } else {
                    console.log(`⚠️ Clawdbot response: ${response.status}`);
                }
            } catch (err) {
                console.error(`❌ Failed to forward to Clawdbot:`, err.message);
            }
        }
    });
    
    return sock;
}

// API endpoint to send messages
app.post('/send', async (req, res) => {
    const { to, message } = req.body;
    
    if (!sock) {
        return res.status(503).json({ error: 'WhatsApp not connected' });
    }
    
    if (!to || !message) {
        return res.status(400).json({ error: 'Missing "to" or "message"' });
    }
    
    try {
        // Format number for WhatsApp
        const jid = to.includes('@') ? to : `${to.replace(/\D/g, '')}@s.whatsapp.net`;
        
        await sock.sendMessage(jid, { text: message });
        
        console.log(`📤 Sent to ${to}: ${message.substring(0, 50)}...`);
        res.json({ success: true, to, message });
    } catch (err) {
        console.error(`❌ Send error:`, err.message);
        res.status(500).json({ error: err.message });
    }
});

// Health check
app.get('/health', (req, res) => {
    res.json({ 
        status: sock ? 'connected' : 'disconnected',
        number: sock?.user?.id?.split(':')[0] || null
    });
});

// Status endpoint
app.get('/status', (req, res) => {
    res.json({
        connected: !!sock,
        number: sock?.user?.id?.split(':')[0] || null,
        uptime: process.uptime()
    });
});

// Start the bridge
async function main() {
    console.log('========================================');
    console.log('🔌 WhatsApp Bridge for Clawdbot');
    console.log('========================================\n');
    
    // Start API server
    app.listen(CONFIG.apiPort, () => {
        console.log(`🌐 API server starting on port ${CONFIG.apiPort}...`);
    });
    
    // Connect to WhatsApp
    await connectToWhatsApp();
}

main().catch(err => {
    console.error('Fatal error:', err);
    process.exit(1);
});
