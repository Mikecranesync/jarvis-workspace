/**
 * FactoryLM Email Capture API
 * 
 * Simple serverless function for waitlist signup.
 * Deploy to: Vercel, Netlify Functions, or Express server.
 * 
 * Options:
 * 1. Store to JSON file (development)
 * 2. Store to Supabase/Neon database (production)
 * 3. Send to Mailchimp/ConvertKit (marketing)
 */

// For Vercel/Netlify serverless
export default async function handler(req, res) {
    // CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    try {
        const { email } = req.body;

        if (!email || !isValidEmail(email)) {
            return res.status(400).json({ error: 'Invalid email address' });
        }

        // Option 1: Store to file (dev only)
        // await storeToFile(email);

        // Option 2: Store to Supabase
        // await storeToSupabase(email);

        // Option 3: Add to Mailchimp
        // await addToMailchimp(email);

        // For now, just log and return success
        console.log(`New signup: ${email} at ${new Date().toISOString()}`);

        // Track signup count
        const signupCount = await getSignupCount();
        const spotsRemaining = Math.max(0, 50 - signupCount);

        return res.status(200).json({
            success: true,
            message: 'Thanks for joining the waitlist!',
            spotsRemaining
        });

    } catch (error) {
        console.error('Signup error:', error);
        return res.status(500).json({ error: 'Something went wrong' });
    }
}

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// ============================================
// STORAGE OPTIONS (uncomment one to use)
// ============================================

// Option 1: File storage (development)
/*
import fs from 'fs/promises';
import path from 'path';

const SIGNUPS_FILE = path.join(process.cwd(), 'data', 'signups.json');

async function storeToFile(email) {
    let signups = [];
    try {
        const data = await fs.readFile(SIGNUPS_FILE, 'utf-8');
        signups = JSON.parse(data);
    } catch (e) {
        // File doesn't exist yet
    }
    
    if (!signups.find(s => s.email === email)) {
        signups.push({
            email,
            signedUpAt: new Date().toISOString(),
            source: 'landing-page'
        });
        await fs.writeFile(SIGNUPS_FILE, JSON.stringify(signups, null, 2));
    }
}

async function getSignupCount() {
    try {
        const data = await fs.readFile(SIGNUPS_FILE, 'utf-8');
        return JSON.parse(data).length;
    } catch (e) {
        return 0;
    }
}
*/

// Option 2: Supabase storage (recommended for production)
/*
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
    process.env.SUPABASE_URL,
    process.env.SUPABASE_ANON_KEY
);

async function storeToSupabase(email) {
    const { error } = await supabase
        .from('waitlist')
        .upsert({ email, signed_up_at: new Date().toISOString() });
    
    if (error) throw error;
}

async function getSignupCount() {
    const { count } = await supabase
        .from('waitlist')
        .select('*', { count: 'exact', head: true });
    
    return count || 0;
}
*/

// Option 3: Mailchimp (for email marketing)
/*
async function addToMailchimp(email) {
    const MAILCHIMP_API_KEY = process.env.MAILCHIMP_API_KEY;
    const MAILCHIMP_LIST_ID = process.env.MAILCHIMP_LIST_ID;
    const MAILCHIMP_DC = MAILCHIMP_API_KEY.split('-')[1];

    const response = await fetch(
        `https://${MAILCHIMP_DC}.api.mailchimp.com/3.0/lists/${MAILCHIMP_LIST_ID}/members`,
        {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${MAILCHIMP_API_KEY}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email_address: email,
                status: 'subscribed',
                tags: ['founding-member', 'waitlist']
            })
        }
    );

    if (!response.ok && response.status !== 400) {
        throw new Error('Mailchimp error');
    }
}
*/
