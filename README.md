# Hot Wheels Collection PWA - Complete Package

## What's Included

### New Features Added:
✅ **Multiple Images per Car** - Upload multiple photos, set main image
✅ **Color Coding** - Custom border colors for cards and collection lines
✅ **Treasure Hunt Types** - Mainline, TH, Super TH badges
✅ **Complete CollectHW Data** - All columns (Col#, Tampo, Wheel Type, Toy#, Assortment#, Case Letter, Exclusive, Value)
✅ **PWA Support** - Install as app on phone
✅ **Offline Mode** - Works without internet
✅ **25 Real Cars** - Pre-loaded from collecthw.com

## Quick Start

### Option 1: Use Locally
1. Download all files to a folder
2. Open `index.html` in your browser
3. Done!

### Option 2: Deploy to GitHub Pages (RECOMMENDED)

1. **Create GitHub Account** (if you don't have one)
   - Go to github.com
   - Sign up for free

2. **Create New Repository**
   - Click "+" → "New repository"
   - Name: `hotwheels-collection`
   - Make it Public
   - Click "Create repository"

3. **Upload Files**
   - Click "uploading an existing file"
   - Drag all these files:
     - index.html
     - manifest.json
     - service-worker.js
     - icon-192.png
     - icon-512.png
   - Click "Commit changes"

4. **Enable GitHub Pages**
   - Go to Settings → Pages
   - Source: "Deploy from branch"
   - Branch: "main"
   - Click Save

5. **Access Your App**
   - Wait 1-2 minutes
   - Visit: `https://YOUR-USERNAME.github.io/hotwheels-collection`

6. **Install on Phone**
   - Open the URL on your phone
   - Click "Share" → "Add to Home Screen"
   - Now it's an app!

## Features Guide

### Multiple Images
- When adding/editing a car, upload multiple images
- Click an image to set it as the "Main Image"
- Main image shows in collection grid
- Other images visible in expanded view

### Color Coding
- Each car can have a custom border color
- Great for organizing by collection line or rarity
- Pick any color with the color picker

### Treasure Hunt Types
- **Mainline** - Regular production cars (Orange badge)
- **Treasure Hunt (TH)** - Special hidden cars (Green badge)
- **Super Treasure Hunt (STH)** - Ultra-rare (Silver badge)

### All Data Fields
From collecthw.com structure:
- Model Name
- Year
- Series
- Color
- Tampo (decoration details)
- Wheel Type
- Toy Number
- Assortment Number
- Case Letter
- Notes
- Exclusive info
- Estimated Value

## Updating Your Collection

### Add More Cars from CollectHW.com:
1. Open https://collecthw.com
2. Press F12 → Console tab
3. Paste the extraction script
4. Copy the JSON data
5. Add to your database array in index.html

## Need Help?

Check the deployment guide or create an issue!
