# Deployment Guide

This guide covers various deployment options for Project Prometheus.

## Table of Contents
- [Development Deployment](#development-deployment)
- [Docker Deployment](#docker-deployment)
- [Production Deployment](#production-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Monitoring & Maintenance](#monitoring--maintenance)

## Development Deployment

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### Backend Setup

```bash
# Clone repository
git clone https://github.com/yourusername/project-prometheus.git
cd project-prometheus

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp backend/.env.example backend/.env
# Edit backend/.env with your settings

# Start backend
cd backend
python -m api.main
```

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Access the application at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Docker Deployment

### Quick Start with Docker Compose

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Docker Build

#### Backend Container

```bash
# Build backend image
docker build -t prometheus-backend .

# Run backend container
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/logs:/app/logs \
  --env-file backend/.env \
  prometheus-backend
```

#### Frontend Container

```bash
# Build frontend image
cd frontend
docker build -t prometheus-frontend .

# Run frontend container
docker run -d \
  -p 3000:3000 \
  prometheus-frontend
```

## Production Deployment

### Backend Production Setup

#### Using Gunicorn

```bash
# Install production dependencies
pip install gunicorn

# Start with Gunicorn
gunicorn backend.api.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log
```

#### Using Systemd Service

Create `/etc/systemd/system/prometheus.service`:

```ini
[Unit]
Description=Project Prometheus API
After network.target

[Service]
Type=notify
User=prometheus
WorkingDirectory=/opt/project-prometheus
Environment="PATH=/opt/project-prometheus/venv/bin"
ExecStart=/opt/project-prometheus/venv/bin/gunicorn backend.api.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable prometheus
sudo systemctl start prometheus
sudo systemctl status prometheus
```

### Frontend Production Setup

#### Build for Production

```bash
cd frontend
npm run build
```

#### Serve with Nginx

Create `/etc/nginx/sites-available/prometheus`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    root /opt/project-prometheus/frontend/build;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/prometheus /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Cloud Deployment

### AWS Deployment

#### Using EC2

1. **Launch EC2 Instance**
   - Ubuntu 20.04 LTS
   - t3.medium or larger
   - Security groups: ports 80, 443, 22

2. **Install Dependencies**
```bash
sudo apt update
sudo apt install python3-pip python3-venv nodejs nginx -y
```

3. **Deploy Application**
```bash
# Clone repository
git clone https://github.com/yourusername/project-prometheus.git
cd project-prometheus

# Setup backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup frontend
cd frontend
npm install
npm run build
cd ..

# Configure nginx
sudo cp frontend/nginx.conf /etc/nginx/sites-available/prometheus
sudo ln -s /etc/nginx/sites-available/prometheus /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Using AWS ECS

Create `ecs-task-definition.json`:

```json
{
  "family": "prometheus",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "prometheus-backend",
      "image": "your-ecr-repo/prometheus-backend:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "API_HOST",
          "value": "0.0.0.0"
        }
      ]
    }
  ]
}
```

### Google Cloud Platform

#### Using Cloud Run

```bash
# Build and push container
gcloud builds submit --tag gcr.io/PROJECT_ID/prometheus-backend

# Deploy to Cloud Run
gcloud run deploy prometheus-backend \
  --image gcr.io/PROJECT_ID/prometheus-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Using Google Kubernetes Engine

Create `k8s-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      containers:
      - name: prometheus
        image: gcr.io/PROJECT_ID/prometheus-backend:latest
        ports:
        - containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: prometheus-service
spec:
  selector:
    app: prometheus
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

Deploy:
```bash
kubectl apply -f k8s-deployment.yaml
```

### Azure Deployment

#### Using Azure Container Instances

```bash
# Create resource group
az group create --name prometheus-rg --location eastus

# Create container instance
az container create \
  --resource-group prometheus-rg \
  --name prometheus-backend \
  --image your-registry/prometheus-backend:latest \
  --dns-name-label prometheus-api \
  --ports 8000
```

## Monitoring & Maintenance

### Health Checks

```bash
# Check API health
curl http://localhost:8000/health

# Check service status
sudo systemctl status prometheus
```

### Log Management

```bash
# View application logs
tail -f logs/prometheus.log

# View nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Database Backups

If using PostgreSQL for chain of custody:

```bash
# Backup database
pg_dump prometheus_db > backup_$(date +%Y%m%d).sql

# Restore database
psql prometheus_db < backup_20240115.sql
```

### Updates and Maintenance

```bash
# Update backend dependencies
pip install --upgrade -r requirements.txt

# Update frontend dependencies
cd frontend
npm update

# Rebuild and restart
sudo systemctl restart prometheus
sudo systemctl reload nginx
```

### Security Hardening

1. **SSL/TLS Configuration**
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com
```

2. **Firewall Configuration**
```bash
# Configure UFW
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

3. **Regular Security Updates**
```bash
# Update system packages
sudo apt update && sudo apt upgrade

# Update Python packages
pip list --outdated
pip install --upgrade package_name
```

## Troubleshooting

### Common Issues

**Backend won't start**
```bash
# Check port availability
sudo netstat -tlnp | grep 8000

# Check logs
tail -f logs/prometheus.log

# Verify dependencies
pip install -r requirements.txt --force-reinstall
```

**Frontend build fails**
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

**Docker container won't start**
```bash
# Check container logs
docker logs prometheus-backend

# Rebuild image
docker-compose build --no-cache
docker-compose up -d
```

## Performance Tuning

### Backend Optimization

1. **Increase worker count**
```bash
gunicorn backend.api.main:app --workers 8
```

2. **Enable caching**
```bash
# Install Redis
pip install redis

# Configure in .env
CACHE_URL=redis://localhost:6379/0
```

### Frontend Optimization

1. **Enable compression**
```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
```

2. **CDN deployment**
- Upload build files to Cloudflare CDN
- Configure DNS to point to CDN

## Backup Strategy

### Automated Backups

Create backup script `backup.sh`:

```bash
#!/bin/bash
# Backup script for Project Prometheus

DATE=$(date +%Y%m%d)
BACKUP_DIR="/backups/prometheus"

# Backup database
pg_dump prometheus_db > $BACKUP_DIR/db_$DATE.sql

# Backup configuration files
tar -czf $BACKUP_DIR/config_$DATE.tar.gz backend/.env

# Keep only last 7 days
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

Add to crontab:
```bash
0 2 * * * /path/to/backup.sh
```

## Scaling Considerations

### Horizontal Scaling

- Use load balancer (nginx, AWS ALB)
- Deploy multiple backend instances
- Implement session affinity if needed

### Vertical Scaling

- Increase CPU cores for image/video processing
- Add more RAM for large file processing
- Use GPU instances for ML model inference

### Database Scaling

- Use managed database (RDS, Cloud SQL)
- Implement read replicas for reporting
- Consider sharding for large deployments
