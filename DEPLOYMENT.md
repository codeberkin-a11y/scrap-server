# 🚀 Deployment Guide - Nesine Scraper API

## 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Push your code to GitHub
3. **Git**: Ensure your project is in a Git repository

## 🔧 Setup Steps

### 1. Initialize Git Repository (if not done)

```bash
cd /Users/berkin/Documents/scrapper-server
git init
git add .
git commit -m "Initial commit: Nesine Scraper API"
```

### 2. Create GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Name it `nesine-scraper-api` or similar
3. **Don't initialize with README** (we already have files)

### 3. Connect Local to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/nesine-scraper-api.git
git branch -M main
git push -u origin main
```

### 4. Deploy to Vercel

#### Option A: Via Vercel CLI (Recommended)

```bash
# Login to Vercel (one-time setup)
vercel login

# Deploy
vercel --prod
```

#### Option B: Via Vercel Dashboard

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click **"New Project"**
3. Import your GitHub repository
4. Click **Deploy**

## 🔗 API Endpoints

Once deployed, your API will be available at:

```
https://your-project-name.vercel.app/api/scrape
```

### Test Endpoints

**Health Check:**

```bash
curl https://your-project-name.vercel.app/api/scrape
```

**Scrape Matches:**

```bash
curl -X POST https://your-project-name.vercel.app/api/scrape \
  -H "Content-Type: application/json" \
  -d '{"sport": "futbol", "date": "24.11.2025"}'
```

## 🌐 Frontend Integration

Update your GitHub Pages client to use the Vercel API:

```javascript
// Replace CORS proxy with Vercel API
const API_BASE = "https://your-project-name.vercel.app/api";

async function fetchMatches(sport, date) {
  const response = await fetch(`${API_BASE}/scrape`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sport, date }),
  });

  const data = await response.json();
  return data.matches;
}
```

## 🔍 Monitoring & Debugging

### View Logs

```bash
vercel logs
```

### Check Function Performance

- Go to Vercel Dashboard → Project → Functions tab
- Monitor execution time and errors

### Environment Variables (if needed)

```bash
vercel env add VARIABLE_NAME
```

## ⚡ Performance Tips

1. **Cold Start**: First request may take ~5-10 seconds
2. **Timeout**: Functions have 10s timeout on Hobby plan
3. **Caching**: Consider caching responses for frequent requests

## 🎯 Success Checklist

- [ ] ✅ Local test passed (`python3 test_api.py`)
- [ ] ✅ Code pushed to GitHub
- [ ] ✅ Vercel project deployed
- [ ] ✅ API health check works
- [ ] ✅ POST endpoint returns match data
- [ ] ✅ Frontend updated to use new API
- [ ] ✅ CORS working from GitHub Pages

## 🆘 Troubleshooting

### Common Issues

**1. ChromeDriver not found**

- Solution: webdriver-manager handles this automatically

**2. Timeout errors**

- Check Vercel logs: `vercel logs`
- Consider optimizing scraper logic

**3. CORS errors**

- Verify `vercel.json` CORS headers
- Check frontend domain configuration

**4. Import errors**

- Ensure all dependencies in `requirements.txt`
- Check Python version compatibility

---

🎉 **Your Nesine Scraper API is now production-ready!**
