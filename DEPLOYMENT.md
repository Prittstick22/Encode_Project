# Deployment Guide

## Overview
This guide covers deploying the Portfolio Management Application in different environments.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Docker Network                          │
│                                                              │
│  ┌──────────────┐      ┌──────────────┐                    │
│  │   Grafana    │◄─────┤  Prometheus  │                    │
│  │  (Dashboard) │      │  (Metrics)   │                    │
│  │  Port: 3000  │      │  Port: 9090  │                    │
│  └──────┬───────┘      └──────▲───────┘                    │
│         │                     │                              │
│         │                     │ scrape                       │
│         │                     │                              │
│  ┌──────▼──────────────────────────────┐                   │
│  │        Flask Backend API            │                   │
│  │    - Portfolio Management           │                   │
│  │    - yfinance Integration           │                   │
│  │    - OpenAI Integration             │                   │
│  │    - Prometheus Metrics             │                   │
│  │    Port: 5000, 8000                 │                   │
│  └──────────────┬──────────────────────┘                   │
│                 │                                            │
│                 │ SQL                                        │
│                 │                                            │
│  ┌──────────────▼──────────────┐                           │
│  │      PostgreSQL             │                           │
│  │    (Data Storage)           │                           │
│  │      Port: 5432             │                           │
│  └─────────────────────────────┘                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘

External Services:
  - yfinance API (Yahoo Finance)
  - OpenAI API (GPT-3.5)
```

## Local Development

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum
- 10GB disk space

### Setup

1. **Clone Repository**
```bash
git clone https://github.com/Prittstick22/Encode_Project.git
cd Encode_Project
```

2. **Configure Environment**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

3. **Start Services**
```bash
./setup.sh
# or manually:
docker-compose up -d
```

4. **Verify Services**
```bash
docker-compose ps
```

All services should show "Up" status.

5. **Access Applications**
- Backend API: http://localhost:5000
- Grafana: http://localhost:3000 (admin/admin)
- Prometheus: http://localhost:9090

### Development Workflow

**Making Backend Changes:**
```bash
# Edit files in ./backend/
docker-compose restart backend
```

**Viewing Logs:**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
```

**Database Access:**
```bash
docker-compose exec postgres psql -U portfolio_user -d portfolio_db
```

**Running Tests:**
```bash
docker-compose exec backend python -m pytest
```

## Production Deployment

### Security Considerations

1. **Change Default Passwords**
   - Update Grafana admin password
   - Update PostgreSQL password
   - Use strong SECRET_KEY for Flask

2. **Environment Variables**
   - Never commit .env file
   - Use secrets management (AWS Secrets Manager, HashiCorp Vault)
   - Rotate API keys regularly

3. **Network Security**
   - Use HTTPS/TLS for all endpoints
   - Configure firewall rules
   - Use VPC/private networks
   - Enable PostgreSQL SSL

4. **API Keys**
   - Restrict OpenAI API key permissions
   - Monitor API usage and costs
   - Implement rate limiting

### Cloud Deployment Options

#### Option 1: AWS ECS with Docker Compose

1. **Install AWS ECS CLI**
```bash
curl -Lo /usr/local/bin/ecs-cli https://amazon-ecs-cli.s3.amazonaws.com/ecs-cli-linux-amd64-latest
chmod +x /usr/local/bin/ecs-cli
```

2. **Configure ECS**
```bash
ecs-cli configure --cluster portfolio-cluster --region us-east-1 --default-launch-type FARGATE
```

3. **Deploy**
```bash
ecs-cli compose --file docker-compose.yml up --create-log-groups
```

#### Option 2: Google Cloud Run

1. **Build and Push Images**
```bash
# Backend
cd backend
gcloud builds submit --tag gcr.io/PROJECT_ID/portfolio-backend

# Deploy
gcloud run deploy portfolio-backend \
  --image gcr.io/PROJECT_ID/portfolio-backend \
  --platform managed \
  --region us-central1
```

#### Option 3: Azure Container Instances

```bash
az container create \
  --resource-group portfolio-rg \
  --name portfolio-app \
  --image your-registry.azurecr.io/portfolio:latest \
  --dns-name-label portfolio-app \
  --ports 5000 3000
```

#### Option 4: Self-Hosted Server

1. **Install Docker on Server**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

2. **Install Docker Compose**
```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

3. **Setup Application**
```bash
git clone https://github.com/Prittstick22/Encode_Project.git
cd Encode_Project
cp .env.example .env
# Edit .env with production values
docker-compose -f docker-compose.yml up -d
```

4. **Setup Nginx Reverse Proxy**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;  # Grafana
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:5000;  # Backend
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

5. **Setup SSL with Let's Encrypt**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Scaling Considerations

#### Horizontal Scaling
- Use load balancer for backend API
- Deploy multiple backend replicas
- Consider Redis for session/cache storage

#### Database Scaling
- Use PostgreSQL replication for read replicas
- Consider managed database services (AWS RDS, Cloud SQL)
- Implement connection pooling

#### Monitoring & Alerting
- Set up Grafana alerts for:
  - High API response times
  - Database connection issues
  - Service health checks
  - API error rates

### Backup Strategy

**Database Backups:**
```bash
# Daily backup script
docker-compose exec -T postgres pg_dump -U portfolio_user portfolio_db > backup_$(date +%Y%m%d).sql

# Restore
docker-compose exec -T postgres psql -U portfolio_user portfolio_db < backup_YYYYMMDD.sql
```

**Automated Backups:**
- Set up cron job for daily backups
- Store backups in S3/Cloud Storage
- Implement backup rotation (keep 30 days)

### Performance Optimization

1. **Database Indexing**
   - Already included in init.sql
   - Monitor slow queries

2. **Caching**
   - Implement Redis for market data cache
   - Cache portfolio calculations

3. **Rate Limiting**
   - Add rate limiting to API endpoints
   - Use nginx rate limiting

4. **API Response Optimization**
   - Enable gzip compression
   - Implement pagination for large results

### Monitoring Checklist

- [ ] All containers running and healthy
- [ ] Database connections stable
- [ ] API response times < 500ms
- [ ] Prometheus scraping metrics
- [ ] Grafana dashboards displaying data
- [ ] Disk space > 20% free
- [ ] Memory usage < 80%
- [ ] SSL certificates valid
- [ ] Backups completing successfully
- [ ] API keys valid and not rate-limited

### Troubleshooting

**Backend Not Starting:**
```bash
# Check logs
docker-compose logs backend

# Check database connection
docker-compose exec backend python -c "from app import db; print('DB connected')"
```

**Database Connection Issues:**
```bash
# Check PostgreSQL is healthy
docker-compose exec postgres pg_isready -U portfolio_user

# Restart database
docker-compose restart postgres
```

**Grafana No Data:**
```bash
# Check Prometheus targets
curl http://localhost:9090/targets

# Verify backend metrics endpoint
curl http://localhost:5000/metrics
```

### Updates and Maintenance

**Updating Application:**
```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose up -d --build

# Check status
docker-compose ps
```

**Database Migrations:**
```bash
# Backup first!
docker-compose exec -T postgres pg_dump -U portfolio_user portfolio_db > backup_pre_migration.sql

# Apply migrations
docker-compose exec backend python -c "from app import db; db.create_all()"
```

## Support

For deployment issues:
1. Check logs: `docker-compose logs -f`
2. Verify all environment variables are set
3. Check network connectivity
4. Ensure all ports are available
5. Review security group/firewall rules

For questions, open an issue on GitHub.
