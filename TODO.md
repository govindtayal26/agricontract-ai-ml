# Color Contrast Fix - Plan

## Information Gathered
- `static/styles.css` defines primary green `#22c55e` which has ~2.8:1 contrast on white (fails WCAG AA which requires 4.5:1)
- `index.html` has `body style="background-color: rgba(0, 0, 0, 0.2)"` which darkens everything and reduces contrast
- Inline styles in `index.html` (weather widget, marketplace, nav avatar) use hardcoded greens
- `dashboard.html` and `add_crop.html` have hardcoded greens (`#2d5a27`)
- `script.js` has hardcoded chart colors (`#22c55e`, `#3b82f6`, `#f59e0b`)

## Plan
1. **static/styles.css**: Update CSS variables to darker, higher-contrast colors:
   - `--primary-color`: `#22c55e` → `#15803d` (darker green, 5.4:1 contrast)
   - `--primary-dark`: `#16a34a` → `#166534`
   - `--primary-light`: `#86efac` → `#bbf7d0`
   - Update gradient backgrounds, loading screen, feature icons, etc.
   - Ensure text on colored backgrounds is white/dark enough
2. **marketplace/templates/index.html**: 
   - Remove `body style="background-color: rgba(0, 0, 0, 0.2)"` → change to white or very light gray
   - Update inline weather widget greens to new primary
   - Update marketplace section inline styles
   - Update nav avatar/user dropdown greens
3. **marketplace/templates/dashboard.html**: 
   - Update heading color `#2d5a27` → `#15803d`
   - Update table badge green background for contrast
4. **marketplace/templates/add_crop.html**: 
   - Update heading color `#2d5a27` → `#15803d`
5. **static/script.js**: 
   - Update chart colors to match new palette

## Dependent Files
- `static/styles.css`
- `marketplace/templates/index.html`
- `marketplace/templates/dashboard.html`
- `marketplace/templates/add_crop.html`
- `static/script.js`

## Progress
- [x] Plan created
- [x] User approved
- [ ] static/styles.css
- [ ] marketplace/templates/index.html
- [ ] marketplace/templates/dashboard.html
- [ ] marketplace/templates/add_crop.html
- [ ] static/script.js

## Followup Steps
- Verify visual appearance in browser
- Check that all green elements are consistent

