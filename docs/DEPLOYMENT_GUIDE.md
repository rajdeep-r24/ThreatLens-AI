# ThreatLens-AI — Deployment & DevOps Engineering Guide

## 1. Deployment Architecture Overview

ThreatLens-AI is engineered for rapid, portable deployment across local analyst workstations, on-premise forensic servers, and enterprise cloud infrastructure. The application implements a multi-container topology orchestrated via **Docker Compose**:

```
+-----------------------------------------------------------------------------+
|                               HOST MACHINE                                  |
|                                                                             |
|  +------------------------+                     +------------------------+  |
|  |   Frontend Container   |                     |   Backend Container    |  |
|  |      (Node 20 / Vite)  |                     |  (Python 3.12 / Uvicorn)| |
|  |                        |                     |                        |  |
|  |  * Port: 5173          |  API Proxy Requests |  * Port: 8000          |  |
|  |  * Image: Alpine Linux | ──────────────────> |  * Image: Slim Debian  |  |
|  |  * Static Asset Server |  (Bridge Network)   |  * FastAPI Application |  |
|  +------------------------+                     +-----------+------------+  |
|                                                             |               |
|                                                       Mounted Volumes       |
|                                                             v               |
|                                                 +------------------------+  |
|                                                 | Persistent Host Storage|  |
|                                                 | * threatlens.db        |  |
|                                                 | * /uploads directory   |  |
|                                                 +------------------------+  |
+-----------------------------------------------------------------------------+
```

---

## 2. Prerequisites & Environment Setup

Ensure the following tools are installed on your host system:
* **Docker Engine** (Version 24.0 or higher)
* **Docker Compose** (V2 / Compose CLI plugin)
* **Git** (for repository synchronization)

### Environment Variables Configuration
Copy the template configuration file before launching the services:
```bash
cp .env.example .env
```

Key environment parameters:
```ini
# Core Backend
PORT=8000
HOST=0.0.0.0
ENVIRONMENT=production
SECRET_KEY=threatlens_super_secret_jwt_key_change_in_production
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Database
DATABASE_URL=sqlite:///./threatlens.db

# Frontend Integration
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

---

## 3. Containerized Deployment via Docker Compose

### 3.1. Build and Launch Containers
To build the Docker images and start both frontend and backend microservices in the background:
```bash
docker compose up --build -d
```

### 3.2. Inspect Container Status
Verify that both containers are active and passing health checks:
```bash
docker compose ps
```
**Expected Output:**
```text
NAME                  IMAGE                        COMMAND                  SERVICE    STATUS              PORTS
threatlens-backend    threatlens-ai-backend        "uvicorn app.main:ap…"   backend    running (healthy)   0.0.0.0:8000->8000/tcp
threatlens-frontend   threatlens-ai-frontend       "docker-entrypoint.s…"   frontend   running             0.0.0.0:5173->5173/tcp
```

### 3.3. Live Container Log Streaming
To monitor application telemetry, incoming upload requests, and scan operations:
```bash
# Stream all logs
docker compose logs -f

# Stream only backend API logs
docker compose logs -f backend

# Stream only frontend logs
docker compose logs -f frontend
```

### 3.4. Graceful Shutdown & Teardown
To safely stop the containers while preserving database state and uploaded samples:
```bash
docker compose down
```

---

## 4. Manual Local Development (Without Containers)

If developing locally without Docker, follow these steps:

### 4.1. Backend Service Setup
```bash
cd backend

# Create and activate Python virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
* **Interactive API Documentation:** Available at `http://localhost:8000/docs` (Swagger UI).

### 4.2. Frontend Service Setup
```bash
cd frontend

# Install Node dependencies
npm install

# Start Vite development server
npm run dev
```
* **Security Dashboard:** Available at `http://localhost:5173`.

---

## 5. Enterprise Cloud Production Hardening

For production deployment on cloud platforms (AWS EC2/ECS, DigitalOcean Droplets, Azure VMs, or Kubernetes), implement the following architecture enhancements:

### 5.1. Nginx Reverse Proxy with TLS/SSL
Do not expose the raw Uvicorn server or Vite port directly to the public internet. Deploy an Nginx reverse proxy to terminate HTTPS traffic:

```nginx
server {
    listen 80;
    server_name threatlens.yourdomain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name threatlens.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/threatlens.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/threatlens.yourdomain.com/privkey.pem;

    # Frontend Static Distribution
    location / {
        proxy_pass http://localhost:5173;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Backend API Routing
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        client_max_body_size 50M;  # Allow large executable uploads
    }
}
```

### 5.2. Scaling Storage: SQLite to PostgreSQL
For high-concurrency enterprise deployments with hundreds of analysts:
1. Launch a managed PostgreSQL cluster (AWS RDS or Supabase).
2. Update the `DATABASE_URL` in `.env`:
   ```ini
   DATABASE_URL=postgresql://threatlens_user:SecurePassword@postgres-db.internal:5432/threatlens_prod
   ```
3. Install the async PostgreSQL driver: `pip install psycopg2-binary`.
4. SQLAlchemy will automatically create all tables on first startup without requiring code modifications.

### 5.3. Security Hardening Checklist
* [x] **Non-Root Execution:** Ensure Docker containers execute under dedicated non-root user accounts.
* [x] **File Quarantining:** Ensure the `uploads/` directory mount is configured with `noexec` flags on the Linux filesystem to prevent accidental binary execution.
* [x] **Secret Rotation:** Replace default demo JWT secret keys with cryptographically random 256-bit keys (`openssl rand -hex 32`).
