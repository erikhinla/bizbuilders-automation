# Deployment Guide - BizBuilders Automation System

## 🎯 System Capabilities Overview

This project is a comprehensive **Digital Marketing Automation System** with the following capabilities:

### 1. **React Frontend Website (TransformBy10X.ai)**
- Modern, responsive landing page built with React + Vite
- SEO-optimized with meta tags and structured data
- Lead capture forms with email collection
- Animated UI with Framer Motion
- Conversion-optimized design

### 2. **Python Automation Backend**
- **Trend Monitoring System**: Real-time trend analysis and content opportunity identification
- **Integration Hub**: Central coordinator connecting all systems
- **SEO Optimization**: Automated SEO analysis and optimization
- **Daily Briefings**: Automated daily trend reports
- **Social Media Automation**: Content generation and scheduling
- **Performance Monitoring**: Website health checks and metrics tracking

### 3. **Social Media Automation Stack**
- **Notion**: Content hub for drafting and approving posts
- **Activepieces**: Automation engine for workflows
- **Postiz**: Social media publisher

---

## 🚀 Deployment Options

### Option 1: Deploy React Frontend to Vercel (Recommended - Easiest)

**Best for**: Quick deployment of the React website

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm i -g vercel
   ```

2. **Navigate to project directory**:
   ```bash
   cd /Users/erikhowerbush/Documents/bizbuilders/ai-pitch-accelerator/bizbuilders-automation
   ```

3. **Deploy**:
   ```bash
   vercel
   ```
   - Follow the prompts to link your project
   - Vercel will auto-detect React/Vite and configure build settings

4. **For production domain**:
   ```bash
   vercel --prod
   ```

**Advantages**: 
- Free tier available
- Automatic HTTPS
- Global CDN
- Auto-deploys on git push
- Zero configuration needed

---

### Option 2: Deploy React Frontend to Netlify

1. **Install Netlify CLI**:
   ```bash
   npm i -g netlify-cli
   ```

2. **Deploy**:
   ```bash
   netlify deploy --prod
   ```

3. **Or connect via GitHub**: Push to GitHub, then connect repo in Netlify dashboard

**Advantages**: 
- Free tier
- Easy custom domain setup
- Form handling built-in

---

### Option 3: Deploy React Frontend to Cloudflare Pages

1. **Install Wrangler CLI**:
   ```bash
   npm i -g wrangler
   ```

2. **Login**:
   ```bash
   wrangler login
   ```

3. **Deploy**:
   ```bash
   npx wrangler pages deploy dist --project-name=bizbuilders-automation
   ```

**Advantages**: 
- Free tier with generous limits
- Fast global CDN
- Built-in analytics

---

### Option 4: Deploy Python Backend to Cloud Server (AWS/DigitalOcean/Linode)

**Best for**: Running the automation scripts continuously

#### Setup on Ubuntu Server:

1. **SSH into your server**:
   ```bash
   ssh user@your-server-ip
   ```

2. **Install Python and dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv git -y
   ```

3. **Clone repository**:
   ```bash
   git clone git@github.com:erikhinla/bizbuilders-automation.git
   cd bizbuilders-automation
   ```

4. **Create virtual environment**:
   ```bash
   python3 -venv venv
   source venv/bin/activate
   ```

5. **Install Python dependencies** (create requirements.txt first - see below):
   ```bash
   pip install requests schedule sqlite3
   ```

6. **Set up systemd service** (for auto-start on boot):
   ```bash
   sudo nano /etc/systemd/system/bizbuilders-automation.service
   ```

   Add this content:
   ```ini
   [Unit]
   Description=BizBuilders Automation Hub
   After=network.target

   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/bizbuilders-automation
   Environment="PATH=/home/ubuntu/bizbuilders-automation/venv/bin"
   ExecStart=/home/ubuntu/bizbuilders-automation/venv/bin/python3 integration_automation_hub.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

7. **Start the service**:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable bizbuilders-automation
   sudo systemctl start bizbuilders-automation
   sudo systemctl status bizbuilders-automation
   ```

---

### Option 5: Deploy Everything with Docker (Recommended for Full Stack)

1. **Create Dockerfile for React app**:
   ```dockerfile
   FROM node:18-alpine as build
   WORKDIR /app
   COPY package*.json ./
   RUN npm install
   COPY . .
   RUN npm run build

   FROM nginx:alpine
   COPY --from=build /app/dist /usr/share/nginx/html
   COPY nginx.conf /etc/nginx/conf.d/default.conf
   EXPOSE 80
   CMD ["nginx", "-g", "daemon off;"]
   ```

2. **Create docker-compose.yml**:
   ```yaml
   version: '3.8'
   services:
     frontend:
       build: .
       ports:
         - "80:80"
       restart: always
     
     automation:
       build:
         context: .
         dockerfile: Dockerfile.python
       volumes:
         - ./data:/app/data
       restart: always
       environment:
         - PYTHONUNBUFFERED=1
   ```

3. **Deploy**:
   ```bash
   docker-compose up -d
   ```

---

## 📋 Pre-Deployment Checklist

### For React Frontend:
- [ ] Create `vite.config.js` if missing
- [ ] Ensure all environment variables are set
- [ ] Test build locally: `npm run build`
- [ ] Verify all assets load correctly
- [ ] Test on mobile devices

### For Python Backend:
- [ ] Create `requirements.txt` with all dependencies
- [ ] Set up environment variables (API keys, etc.)
- [ ] Configure database paths
- [ ] Test scripts locally
- [ ] Set up log rotation
- [ ] Configure monitoring/alerting

---

## 🔧 Required Configuration Files

### Create `vite.config.js`:
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
  },
  server: {
    port: 5173,
    host: true,
  },
})
```

### Create `requirements.txt`:
```txt
requests>=2.31.0
schedule>=1.2.0
```

---

## 🌐 Domain Setup

### For Vercel/Netlify:
1. Add your domain in the platform dashboard
2. Update DNS records as instructed
3. SSL certificate is automatic

### For Custom Server:
1. Point domain A record to server IP
2. Install Certbot for SSL:
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d transformby10x.ai
   ```

---

## 📊 Monitoring & Maintenance

### Check Python Automation Status:
```bash
# On server
sudo systemctl status bizbuilders-automation
tail -f /var/log/bizbuilders-automation.log
```

### View Integration Reports:
```bash
# Reports are saved to:
/home/ubuntu/integration_report.json
```

### Restart Services:
```bash
sudo systemctl restart bizbuilders-automation
```

---

## 🚨 Troubleshooting

### React Build Fails:
- Check Node.js version (need 18+)
- Clear node_modules and reinstall
- Check for missing dependencies

### Python Scripts Not Running:
- Check Python version (need 3.8+)
- Verify all dependencies installed
- Check file permissions
- Review logs for errors

### Automation Not Working:
- Verify API keys are set correctly
- Check database file permissions
- Ensure network connectivity
- Review integration status in database

---

## 📞 Next Steps After Deployment

1. **Set up monitoring**: Use services like UptimeRobot or Pingdom
2. **Configure backups**: Regular backups of database and config files
3. **Set up alerts**: Email/SMS alerts for system failures
4. **Performance monitoring**: Track website speed and automation metrics
5. **Regular updates**: Keep dependencies and system updated

---

## 💡 Recommended Deployment Strategy

**For Quick Launch:**
- Frontend: Deploy to Vercel (5 minutes)
- Backend: Deploy to DigitalOcean Droplet ($5/month)

**For Production:**
- Frontend: Vercel or Cloudflare Pages
- Backend: AWS EC2 or DigitalOcean with auto-scaling
- Database: Managed PostgreSQL (if upgrading from SQLite)
- Monitoring: CloudWatch or Datadog

---

## 🔐 Security Checklist

- [ ] Use environment variables for all API keys
- [ ] Enable HTTPS everywhere
- [ ] Set up firewall rules (only allow necessary ports)
- [ ] Regular security updates
- [ ] Use strong passwords/SSH keys
- [ ] Enable 2FA on all services
- [ ] Regular backups
- [ ] Monitor for suspicious activity

