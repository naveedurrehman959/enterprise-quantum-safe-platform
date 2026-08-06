# Enterprise Quantum-Safe Cryptographic Infrastructure Platform

## Overview

The Enterprise Quantum-Safe Cryptographic Infrastructure Platform is a full-stack security platform designed to help organizations prepare for the post-quantum era.

It provides centralized management of cryptographic assets, policy enforcement, risk assessment, post-quantum certificate management, migration planning, compliance reporting, and enterprise dashboards.

---

## Features

- Authentication & RBAC
- Algorithm Inventory
- Risk Assessment Engine
- Policy Engine
- Migration Engine
- Enterprise PKI
- Certificate Lifecycle Management
- Quantum Risk Analysis
- Compliance Dashboard
- Audit Logging
- Reports & Analytics
- Monitoring
- Docker Support
- GitHub Actions CI/CD

---

## Technology Stack

### Frontend

- React
- Material UI
- Axios
- Vite

### Backend

- Flask
- SQLAlchemy
- JWT Authentication
- REST API

### Security

- ML-KEM
- ML-DSA
- AES-256-GCM
- Hybrid Cryptography

### DevOps

- Docker
- Docker Compose
- GitHub Actions

---

## Project Structure

```
frontend/
backend/
docker/
monitoring/
.github/workflows/
docs/
```

---

## Running the Project

### Backend

```
cd backend

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

python wsgi.py
```

### Frontend

```
cd frontend

npm install

npm run dev
```

---

## Docker

```
docker compose up --build
```

---

## CI/CD

Every push automatically:

- Installs dependencies
- Runs backend tests
- Builds React frontend
- Builds Docker images

---

## Future Enhancements

- Kubernetes Deployment
- Vault Integration
- Prometheus & Grafana
- Enterprise PKI Integration
- Multi-Tenant Support

---

## Author

Naveed ur Rehman

DEVSECCOPs

Enterprise Quantum-Safe Cryptographic Infrastructure Platform
