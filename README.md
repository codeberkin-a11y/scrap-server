# Nesine Scraper API - Vercel Server

🚀 **Production-ready Vercel API server for Nesine.com scraping**

## 🎯 Overview

This is a Vercel-hosted API server that scrapes Nesine.com betting fixtures and serves them to GitHub Pages clients. It uses Python 3.9 runtime with Selenium WebDriver for robust web scraping.

## ✅ Current Status

- ✅ **API Implementation**: Complete with direct scraper integration
- ✅ **Local Testing**: Successfully tested and validated
- ✅ **CORS Configuration**: Enabled for GitHub Pages clients
- ✅ **Dependencies**: Optimized for Vercel serverless environment
- 🚀 **Ready for Deployment**: All tests passing

## 📡 API Endpoints

### POST /api/scrape

Scrape live matches for specified sport and date.

**Request:**

```json
{
  "sport": "futbol", // futbol, basketbol, karma
  "date": "24.11.2025" // DD.MM.YYYY format (optional, defaults to today)
}
```

**Response:**

```json
{
  "matches": [
    {
      "kod": "2442934",
      "saat": "45'+",
      "mac": "Costa Do SolFer. de Maputo",
      "mbs": "C",
      "spor": "Futbol",
      "odd_1": "9.60",
      "odd_x": "3.49",
      "odd_2": "1.18",
      "under_odd": "",
      "over_odd": ""
    }
  ],
  "count": 41,
  "sport": "futbol",
  "date": "24.11.2025",
  "status": "success"
}
```

### GET /api/scrape

Health check endpoint.

**Response:**

```json
{
  "status": "OK",
  "service": "Nesine Scraper API",
  "version": "1.0.0",
  "timestamp": "2025-11-24T16:30:00"
}
```

## 🧪 Local Testing

Test the scraper logic locally:

```bash
# Run comprehensive test
python3 test_api.py
```

**Expected Output:**

```
🧪 Starting Nesine Scraper Logic Test
========================================
🔧 Testing scraper logic...
🔍 Scraping: https://www.nesine.com/iddaa?dt=24.11.2025
📊 Found 41 match containers
✅ Successfully parsed 41 matches
🎉 Scraper logic works! API is ready for deployment.
```

## 🚀 Deployment

See detailed deployment instructions in [DEPLOYMENT.md](DEPLOYMENT.md)

### Quick Deploy

```bash
# Install Vercel CLI
npm i -g vercel

# Login and deploy
vercel login
vercel --prod
```

## 🌐 CORS Configuration

API is configured to allow requests from any origin (`Access-Control-Allow-Origin: *`) making it compatible with:

- GitHub Pages clients
- Local development servers
- Any frontend framework

## 📱 Client Integration

GitHub Pages client can consume this API:

```javascript
const response = await fetch("https://your-api.vercel.app/api/scrape", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ sport: "futbol", date: "24.11.2025" }),
});

const data = await response.json();
console.log(`Found ${data.count} matches`);

// Process matches
data.matches.forEach((match) => {
  console.log(`${match.saat} - ${match.mac} - MBS: ${match.mbs}`);
});
```

## 🏗️ Project Structure

```
scrapper-server/
├── api/
│   └── scrape.py          # Main API endpoint with Selenium logic
├── vercel.json            # Vercel configuration with CORS headers
├── requirements.txt       # Python dependencies optimized for Vercel
├── test_api.py           # Local test script
├── DEPLOYMENT.md         # Detailed deployment guide
└── README.md             # This file
```

## 🔧 Technical Details

- **Runtime**: Python 3.9 (Vercel serverless)
- **Scraper**: Selenium WebDriver with Chrome headless
- **Driver Management**: webdriver-manager for automatic setup
- **Parsing**: BeautifulSoup for HTML parsing
- **Timeout**: 60 seconds per request (Vercel limit)
- **Headers**: CORS enabled for all origins
- **Response Format**: JSON with structured match data

## 📊 Performance

- **Cold Start**: ~5-10 seconds (first request)
- **Warm Requests**: ~3-5 seconds
- **Matches Found**: ~40-60 typical per request
- **Success Rate**: High reliability with error handling

## 🔍 Data Fields

Each match contains:

- `kod`: Nesine match ID
- `saat`: Match time/status
- `mac`: Team names
- `mbs`: Match status (C=Live, etc.)
- `spor`: Sport type (Futbol, Basketbol)
- `odd_1`, `odd_x`, `odd_2`: Main odds
- `under_odd`, `over_odd`: Total goals odds

Perfect for serverless architecture! 🎉
