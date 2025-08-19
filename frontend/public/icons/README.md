# PWA Icons

This directory contains the icons needed for the Pot Logic PWA.

## Current Files
- `icon.svg` - Source SVG icon with poker theme (spades, hearts, diamonds, clubs)

## Required PNG Icons

The following PNG icons need to be generated from the `icon.svg` file:

### Main App Icons
- `icon-72x72.png` (72x72 pixels)
- `icon-96x96.png` (96x96 pixels)
- `icon-128x128.png` (128x128 pixels)
- `icon-144x144.png` (144x144 pixels)
- `icon-152x152.png` (152x152 pixels)
- `icon-192x192.png` (192x192 pixels)
- `icon-384x384.png` (384x384 pixels)
- `icon-512x512.png` (512x512 pixels)

### Shortcut Icons
- `shortcut-hand-96x96.png` (96x96 pixels) - Hand evaluator shortcut
- `shortcut-pot-96x96.png` (96x96 pixels) - Pot odds calculator shortcut
- `shortcut-history-96x96.png` (96x96 pixels) - Game history shortcut

## How to Generate Icons

### Option 1: Online Tools
1. Use online SVG to PNG converters like:
   - https://convertio.co/svg-png/
   - https://cloudconvert.com/svg-to-png
   - https://www.svgviewer.dev/

2. Upload the `icon.svg` file and convert to different sizes

### Option 2: Command Line (if you have ImageMagick)
```bash
# Install ImageMagick first, then run:
convert icon.svg -resize 72x72 icon-72x72.png
convert icon.svg -resize 96x96 icon-96x96.png
convert icon.svg -resize 128x128 icon-128x128.png
convert icon.svg -resize 144x144 icon-144x144.png
convert icon.svg -resize 152x152 icon-152x152.png
convert icon.svg -resize 192x192 icon-192x192.png
convert icon.svg -resize 384x384 icon-384x384.png
convert icon.svg -resize 512x512 icon-512x512.png
```

### Option 3: Using Node.js with sharp
```bash
npm install -g sharp-cli
sharp -i icon.svg -o icon-72x72.png resize 72 72
sharp -i icon.svg -o icon-96x96.png resize 96 96
# ... repeat for all sizes
```

### Option 4: Design Tools
- Use Figma, Sketch, or Adobe Illustrator to export the SVG at different sizes
- Use GIMP or Photoshop to resize the base icon

## Icon Requirements

- **Format**: PNG
- **Purpose**: All icons should support both "any" and "maskable" purposes
- **Background**: Icons should have a solid background (not transparent) for better PWA compatibility
- **Quality**: Use high-quality exports to ensure crisp appearance on all devices

## Testing

After generating the icons, test the PWA by:
1. Running the development server
2. Opening Chrome DevTools
3. Going to Application tab > Manifest
4. Verifying all icons are loaded correctly
5. Testing the "Install" prompt in the browser 