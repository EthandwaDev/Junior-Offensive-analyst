# Portfolio Deployment Guide

## Deploy to GitHub Pages (Free & Professional)

### Step 1: Create GitHub Repository
```bash
# Create new repository named: username.github.io
# Replace 'username' with your GitHub username
```

### Step 2: Push Files to GitHub
```bash
cd /workspaces/analyst
git init
git add .
git commit -m "Initial portfolio commit"
git branch -M main
git remote add origin https://github.com/username/username.github.io.git
git push -u origin main
```

### Step 3: Enable GitHub Pages
- Go to repository Settings
- Navigate to "Pages" section
- Source: main branch
- Save

Your portfolio will be live at: `https://username.github.io`

---

## Deploy to Custom Domain

### Option 1: Netlify (Recommended - Free)
1. Go to [netlify.com](https://netlify.com)
2. Click "New site from Git"
3. Connect GitHub repository
4. Deploy settings: Leave defaults
5. Deploy!

Your site publishes automatically with each git push.

---

## Deploy Locally for Testing

### Python
```bash
cd /workspaces/analyst
python3 -m http.server 8000
# Visit: http://localhost:8000
```

### Node.js
```bash
npm install -g http-server
cd /workspaces/analyst
http-server
```

---

## Portfolio Customization Checklist

Before going live:

- [ ] **Update Contact Info**
  - Replace [your.email@example.com] in index.html
  - Replace [LinkedIn] link
  - Replace [GitHub] link
  - Update LinkedIn and GitHub URLs

- [ ] **Customize Project Descriptions**
  - Add specific achievements
  - Include metrics/results
  - Update any placeholder text

- [ ] **Add Your Information**
  - Bio/background
  - Professional summary
  - Career goals

- [ ] **Update Certifications**
  - List accurate certification names
  - Add dates earned
  - Include issuing organizations

- [ ] **Verify All Links**
  - Project links work
  - Navigation smooth
  - No broken links

---

## SEO Optimization

### Add Meta Tags to index.html
```html
<meta name="description" content="Junior Penetration Tester Portfolio - SQL Injection, C++, Security Analysis">
<meta name="keywords" content="penetration testing, cybersecurity, sql injection, secure coding">
<meta name="author" content="Your Name">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

### Google Analytics (Optional)
```html
<!-- Add before closing </head> tag -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_ID');
</script>
```

---

## Mobile Optimization

✓ Already optimized! The CSS includes:
- Responsive media queries
- Mobile-friendly navigation
- Touch-friendly buttons (44+ pixels)
- Flexible layouts

Test on mobile devices before deploying.

---

## Performance Tips

### Optimize Images
```bash
# Reduce image file sizes
jpegoptim image.jpg --max=80 -q
pngquant image.png
```

### Minify CSS/JS (Optional)
```bash
# Using online tools or local tools
csso styles.css -o styles.min.css
terser script.js -o script.min.js
```

### Enable Caching
Set cache headers in hosting provider settings:
- HTML: 1 hour
- CSS/JS: 30 days
- Images: 90 days

---

## Security Considerations

✓ HTTPS enabled (automatic with GitHub Pages)
✓ No sensitive data in repository
✓ Regular updates and maintenance
✓ Backup locally with git

---

## Troubleshooting

**Portfolio not showing?**
- Clear browser cache (Ctrl+Shift+Delete)
- Check file paths are correct
- Verify http.server is running
- Check browser console for errors

**Links not working?**
- Verify paths are relative (not absolute)
- Check file names match exactly
- Ensure directories exist

**Styling not showing?**
- Check styles.css is in same directory
- Clear browser cache
- Check browser console for errors

---

## Share Your Portfolio

Once live, share it on:

✓ LinkedIn profile  
✓ GitHub README  
✓ Resume/CV  
✓ Email signature  
✓ Cover letters  
✓ Job applications  
✓ Professional social media  

---

## Next Steps

1. **Customize** the portfolio with your information
2. **Test** locally with `python3 -m http.server 8000`
3. **Deploy** to GitHub Pages or Netlify
4. **Share** with employers and network
5. **Update** regularly with new projects

---

## Support

If you encounter issues:
1. Check browser console (F12)
2. Verify file paths and names
3. Test in different browser
4. Check hosting provider documentation
5. Verify git repository settings

---

**Your portfolio is ready to impress employers!**

Remember: Keep it updated with new projects, certifications, and skills as you grow in your cybersecurity career.

---

*Last Updated: February 2026*
