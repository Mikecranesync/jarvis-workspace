# Website Team Resources

## Forked UI Libraries (GitHub: mikecranesync)

These repos are forked to Mike's account for reference and potential customization:

### Core UI Components
| Repo | Purpose | URL |
|------|---------|-----|
| **ui** (Shadcn) | Copy-paste React components | https://github.com/Mikecranesync/ui |
| **magicui** | Animated landing page components | https://github.com/Mikecranesync/magicui |
| **spectrum-ui** | Combined Aceternity + Magic + Shadcn | https://github.com/Mikecranesync/spectrum-ui |
| **daisyui** | Tailwind CSS component library | https://github.com/Mikecranesync/daisyui |

### Animation & Styling
| Repo | Purpose | URL |
|------|---------|-----|
| **motion** | Framer Motion animations | https://github.com/Mikecranesync/motion |
| **tailwindcss** | Utility-first CSS framework | https://github.com/Mikecranesync/tailwindcss |

---

## How to Use

### For Landing Pages (Samsara-style)
1. Reference **spectrum-ui** for pre-built animated sections
2. Use **magicui** for hero animations, floating elements
3. Apply **Shadcn/ui** patterns for forms, buttons, cards

### For Copy-Paste Components
```bash
# Clone spectrum-ui locally
git clone https://github.com/Mikecranesync/spectrum-ui.git

# Browse components in /components directory
# Copy relevant code into /var/www/factorylm/preview/
```

### Recommended Stack
- **Framework:** Next.js 14 or Astro
- **Styling:** Tailwind CSS
- **Components:** Shadcn/ui + Magic UI
- **Animations:** Framer Motion
- **Icons:** Lucide React

---

## Component Sources (External)

### Copy-Paste Ready
- **Aceternity UI:** https://ui.aceternity.com
- **Magic UI:** https://magicui.design
- **Uiverse:** https://uiverse.io
- **Shadcn:** https://ui.shadcn.com

### Design Inspiration
- **Samsara:** https://samsara.com (target aesthetic)
- **Linear:** https://linear.app (clean SaaS)
- **Vercel:** https://vercel.com (dark mode done right)

---

## Standing Orders for Website Team

1. **Always check forked repos first** before writing custom components
2. **Copy from spectrum-ui** when animated sections are needed
3. **Match Samsara aesthetic** - dark heroes, alternating sections, big stats
4. **Mobile-first** - test on 375px width minimum
5. **Performance** - lazy load images, minimize JS

---

*Last Updated: 2026-02-05*
