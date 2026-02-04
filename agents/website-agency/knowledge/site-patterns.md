# FactoryLM Website Patterns

## Current Tech Stack
- Pure HTML/CSS/JS (no build step)
- Tailwind CSS via CDN
- Vanilla JavaScript for interactivity
- Static hosting on Caddy server

## Design System

### Colors
- Primary: Blue gradient (`from-blue-600 to-purple-600`)
- Background: Dark (`bg-gray-900`, `bg-gray-800`)
- Text: White/Gray (`text-white`, `text-gray-300`)
- Accents: Cyan, Purple, Green for highlights

### Typography
- Headings: Bold, large (`text-4xl font-bold`)
- Body: `text-gray-300` on dark backgrounds
- Code/Technical: Monospace elements

### Components
- Cards: `bg-gray-800 rounded-xl p-6` with hover states
- Buttons: Gradient backgrounds, rounded, with transitions
- Sections: Full-width with consistent padding

### Current Pages
- `/` - Main landing page
- `/edge/` - Edge device product page (USB configurator)
- `/blog/` - Blog section

## UX Principles (Mike's Preferences)
- Intuitive over clever
- Visual hierarchy matters
- Interactive elements should have clear affordances
- Cards should feel "grabbable" if draggable
- USB ports should look like... USB ports

## Known Issues to Address
- Edge page: Card/USB interaction not intuitive
- Need clearer visual cues for interactive elements
