# 🚀 Production Simulation Lab

![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Status](https://img.shields.io/badge/status-active-success)
![DevOps](https://img.shields.io/badge/focus-DevOps-blue)
![Cloud](https://img.shields.io/badge/cloud-AWS%20%7C%20Tencent-orange)
![Environment](https://img.shields.io/badge/environment-WSL2%20%7C%20Linux-lightgrey)

## 📌 Overview

**Production Simulation Lab** is a comprehensive DevOps experimentation environment designed to simulate real-world production systems for learning, testing, and deployment practice. This repository serves as a professional sandbox for building enterprise-level skills through hands-on infrastructure work.

### What This Lab Offers

- **Real-World Simulation**: Practice production-style deployments in a controlled environment
- **Multi-Cloud Experience**: Experiment with AWS, Tencent Cloud, and future platforms
- **Infrastructure Automation**: Build, break, and fix systems to develop troubleshooting expertise
- **End-to-End Testing**: From DNS configuration to application deployment
- **Safe Experimentation**: Test dangerous operations without production consequences

---

## 🎯 Objectives

- ✅ Practice production-style deployments and configurations
- ✅ Test DevOps tools and workflows safely
- ✅ Experiment with multi-cloud environments
- ✅ Automate infrastructure setup and management
- ✅ Build real-world troubleshooting experience
- ✅ Develop system administration and networking skills
- ✅ Simulate failure scenarios and recovery procedures

---

## 🧱 Tech Stack & Tools

### ☁️ Cloud Platforms

- **AWS** - Amazon Web Services
- **Tencent Cloud** - Cloud infrastructure
- **Future**: GCP, Azure

### 🌐 Servers & Networking

- **Apache2** - Web server
- **BIND9** - DNS server implementation
- **UFW** - Uncomplicated Firewall
- **Custom DNS Mapping** - Local domain resolution
- **WSL2 Networking** - Windows Subsystem for Linux integration

### ⚙️ DevOps & Automation

- **Bash Scripting** - Infrastructure automation
- **Git & GitHub** - Version control and collaboration
- **CI/CD** - Continuous Integration/Deployment (Planned)
- **Infrastructure Testing** - Validation and health checks

### 🖥️ Applications & Development

- **Python** - Core language for GUI development
- **Tkinter** - GUI framework for desktop applications
- **MySQL** - Database management system
- **Web Technologies** - HTML, CSS, JavaScript
- **Static Site Hosting** - AWS deployment testing
- **Web Applications** - Full-stack development practice

---

## 📁 Project Structure

```
production-simulation-lab/
│
├── CCtkinter/            # Currency Converter GUI (Tkinter + MySQL)
├── Honda_Stock_Billing/  # Stock billing web application
├── smart_parking/        # Static website (AWS deployment testing)
├── .gitignore            # Git ignore rules
├── LICENSE               # Apache License 2.0
└── README.md             # This file
```

### Project Details

| Project | Type | Description | Technologies |
|---------|------|-------------|--------------|
| **CCtkinter** | Desktop GUI | Currency converter application with database integration | Python, Tkinter, MySQL |
| **Honda_Stock_Billing** | Web App | Stock billing management system | Web technologies |
| **smart_parking** | Static Website | Basic static website used for AWS deployment testing | HTML, CSS, JavaScript |

> **Note**: Structure evolves organically as experimentation expands.

---

## 🔬 What This Lab Simulates

| Area | Simulation |
|------|------------|
| **DNS Management** | Production-style DNS setup with BIND9 |
| **Web Hosting** | Apache server binding and virtual hosts |
| **Security** | Firewall configuration and port management |
---

## 🚀 Quick Start Guide

### 1. **CCtkinter** - Currency Converter GUI

Desktop application for currency conversion with MySQL database integration.

**Prerequisites:**
- Python 3.8+
- MySQL Server running

**Setup:**
```bash
cd CCtkinter
pip install -r requirements.txt
```

**Run:**
```bash
python currency_converter.py
```

**Features:**
- Real-time currency conversion
- Tkinter GUI interface
- MySQL database backend for historical conversions
- Support for multiple currency pairs

---

### 2. **Honda_Stock_Billing** - Stock Billing Web Application

Web-based stock and billing management system for Honda dealership operations.

**Prerequisites:**
- Python 3.8+
- MySQL Server running

**Setup:**
```bash
cd Honda_Stock_Billing
pip install -r requirements.txt
python init_db.py          # Initialize database
```

**Configuration:**
Edit `config.py` with your database credentials:
```python
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'your_password'
DB_NAME = 'honda_billing'
```

**Run:**
```bash
python app.py
```

Open browser: **http://localhost:5000**

**Features:**
- Vehicle stock management
- Billing and invoicing
- Customer management
- Inventory tracking
- PDF bill generation

---

### 3. **game_lore_api** - Game Metadata Aggregator API

FastAPI REST API that aggregates game data from RAWG and GiantBomb APIs to provide comprehensive game information, franchise timelines, studio histories, and series chains.

**Prerequisites:**
- Python 3.8+
- Free API keys from RAWG and GiantBomb

**Setup:**
```bash
cd game_lore_api

# Create virtual environment
python -m venv venv
source venv/bin/activate          # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Get API Keys:**
| Service | Registration URL | Status |
|---------|-----------------|--------|
| RAWG | https://rawg.io/apidocs | Free tier available |
| GiantBomb | https://www.giantbomb.com/api/ | Free tier available |

**Configure Environment:**
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```env
RAWG_API_KEY=your_rawg_api_key_here
GIANTBOMB_API_KEY=your_giantbomb_api_key_here
HOST=0.0.0.0
PORT=5000
```

**Run:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

Open browser: **http://localhost:5000/docs** (Interactive Swagger UI)

**API Endpoints:**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API health check and endpoints info |
| `/search?name=<game_name>` | GET | Search game by name — returns full details (release, studio, story, ratings) |
| `/lore/{game_slug}` | GET | Get game lore, description, storyline, themes |
| `/franchise/{franchise_name}/timeline` | GET | Get all franchise entries in chronological order |
| `/studio/{studio_name}/games` | GET | Get all games from a developer in release order |
| `/series/{game_name}/chain` | GET | Get predecessor → successor chain for a game series |

**Example Requests:**
```bash
# Search for a game
curl "http://localhost:5000/search?name=The+Witcher+3"

# Get game lore
curl "http://localhost:5000/lore/the-witcher-3-wild-hunt"

# Get franchise timeline
curl "http://localhost:5000/franchise/Assassin%27s%20Creed/timeline"

# Get studio history
curl "http://localhost:5000/studio/Naughty%20Dog/games"

# Get series chain
curl "http://localhost:5000/series/Assassin%27s%20Creed/chain"
```

**Architecture:**
```
Client Request
    ↓
FastAPI Router (main.py)
    ↓
Game Aggregator Service (aggregator.py)
    ↓
    ├→ RAWG Service (rawg.py)
    │   └→ RAWG API
    │
    └→ GiantBomb Service (giantbomb.py)
        └→ GiantBomb API
    ↓
Unified Response (models.py)
    ↓
Client
```

**Troubleshooting:**
- If API keys are invalid: Check .env file and verify keys at respective API websites
- If port 5000 is in use: Change PORT in .env and uvicorn command
- For CORS issues: The API allows all origins by default; modify main.py if needed

---

### 4. **smart_parking** - Static Website

Static website used for AWS deployment testing and hosting practice.

**Setup:**
```bash
cd smart_parking
# No dependencies needed - pure HTML/CSS/JavaScript
```

**Serve Locally:**
```bash
# Using Python 3
python -m http.server 8000

# Or using Node.js http-server
npx http-server
```

Open browser: **http://localhost:8000**

**Features:**
- Responsive design
- Smart parking booking interface
- User profiles and booking history
- Real-time parking availability visualization

---

## 🔌 Port Configuration

| Service | Default Port | Environment Variable |
|---------|--------------|----------------------|
| game_lore_api (FastAPI) | 5000 | `PORT` in `.env` |
| Honda_Stock_Billing | 5000 | `FLASK_PORT` in `config.py` |
| smart_parking (Static) | 8000 | CLI argument |
| CCtkinter | N/A | Desktop app |

> **Note**: Ensure ports are available before starting services. If a port is already in use, modify the port configuration accordingly.

---

## 💾 Database Setup

### CCtkinter & Honda_Stock_Billing
Both applications use MySQL. Ensure MySQL is running:

**Windows:**
```bash
# Start MySQL service
net start MySQL80  # or your version
```

**Linux/WSL:**
```bash
sudo service mysql start
```

**Create Databases:**
```bash
mysql -u root -p

CREATE DATABASE currency_converter;
CREATE DATABASE honda_billing;
```

---

## 📋 Environment Files

Each project may require `.env` file configuration:
- `game_lore_api/.env` - API keys and server config
- `Honda_Stock_Billing/config.py` - Database credentials

Always copy from `.example` files and fill in your credentials before running.

---

## 🛠 Development Workflow

1. **Clone/Navigate** to project directory
2. **Install** dependencies (`pip install -r requirements.txt`)
3. **Configure** environment variables (`.env` or config files)
4. **Start** the service (run script or uvicorn/flask command)
5. **Test** via browser or curl/Postman
6. **Debug** using logs and API documentation

---

## ✅ Testing the Setup

### Verify All Services
```bash
# Test game_lore_api
curl http://localhost:5000/

# Test Honda_Stock_Billing
curl http://localhost:5000/

# Test smart_parking
curl http://localhost:8000/
```

---| **Networking** | Resolver manipulation and WSL networking |
| **Deployment** | Multi-application hosting strategies |
| **Cloud Operations** | AWS/Tencent deployment experiments |
| **Validation** | Service health checks and monitoring |
| **Recovery** | Infrastructure rollback and reconfiguration |

This lab enables **controlled failure testing** — a critical DevOps skill that can't be practiced in production.

---

## 🧪 Current Projects & Experiments

### 💱 **CCtkinter** - Currency Converter
A desktop GUI application built with Python's Tkinter framework and MySQL database integration. Demonstrates:
- GUI development with Tkinter
- Database connectivity and operations
- Real-time data handling
- Cross-platform desktop application development

### 🚗 **Honda_Stock_Billing** - Stock Management System
A web-based billing and stock management application. Features:
- Stock inventory tracking
- Billing system implementation
- Web application architecture
- Database-driven operations

### 🅿️ **smart_parking** - Static Website
A basic static website used as a testing ground for AWS deployment workflows. Use cases:
- Cloud deployment practice (AWS)
- Static site hosting
- Infrastructure testing
- DNS and domain configuration
- Production deployment simulation

### Additional Experiments
- 🌍 Hosting web applications via Apache
- 🔗 Mapping custom domains to local servers
- 📡 Running private DNS servers with BIND9
- ☁️ Testing deployment workflows to AWS
- 🔐 Simulating production port exposure and security
- 🤖 Automating service configuration and management
- 💥 Intentionally breaking and restoring configurations

---

## 🚀 Getting Started

### Clone the Repository

```bash
git clone git@github.com:pratham1kruk/production-simulation-lab.git
cd production-simulation-lab
```

### Explore Projects

Navigate to specific projects based on your learning focus:

```bash
# Currency Converter GUI
cd CCtkinter/

# Stock Billing System
cd Honda_Stock_Billing/

# Static Website (AWS Testing)
cd smart_parking/
```

Each project contains its own setup instructions and dependencies.

---

## 🧠 Learning Focus

This lab emphasizes hands-on understanding of:

- **System Architecture**: How production systems actually work
- **Network Debugging**: Resolving DNS, routing, and connectivity issues
- **Service Management**: Working with systemd and service orchestration
- **DNS Resolution**: Understanding the complete resolution chain
- **Cloud Infrastructure**: Fundamentals of cloud platform operations
- **Security Practices**: Implementing secure configuration patterns
- **Automation Mindset**: Thinking in terms of repeatable processes

---

## 🛠️ Prerequisites

- Linux environment (Ubuntu/Debian recommended) or WSL2
- Basic command-line proficiency
- Understanding of networking concepts
- Git installed and configured
- Cloud account (for cloud experiments)

---

## ⚠️ Disclaimer

This repository is intended for:

- 📚 **Learning and Education**
- 🔬 **Experimentation and Testing**
- 💪 **Skill Development**

**Important**: This is not production-ready code. Do not deploy directly to production without proper security hardening, code review, and testing.

---

## 📈 Roadmap

- [ ] Dockerize applications for containerization
- [ ] Add reverse proxy with Nginx
- [ ] Implement SSL/TLS with Let's Encrypt
- [ ] Build complete CI/CD pipeline
- [ ] Add monitoring stack (Prometheus/Grafana)
- [ ] Multi-cloud deployment automation
- [ ] Infrastructure as Code with Terraform
- [ ] Kubernetes orchestration experiments
- [ ] Log aggregation and analysis
- [ ] Automated backup and recovery

---

## 👨‍💻 Author

**Pratham Kumar Uikey**  
DevOps & Infrastructure Enthusiast

Passionate about building, breaking, and fixing systems to develop real-world production expertise.

---

## 📜 License

This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.

```
Copyright 2025 Pratham Kumar Uikey

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

---

## ⭐ Why This Project Matters

> **Production experience doesn't come from tutorials.**

It comes from:

1. **Building Systems** - Implementing infrastructure from scratch
2. **Breaking Systems** - Understanding failure modes and edge cases
3. **Fixing Systems** - Developing troubleshooting and recovery skills

This lab simulates that complete journey in a safe, repeatable environment.

---

## 🤝 Contributing

While this is primarily a personal learning repository, suggestions and feedback are welcome:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/experiment`)
3. Commit your changes (`git commit -m 'Add experiment description'`)
4. Push to the branch (`git push origin feature/experiment`)
5. Open a Pull Request

---

## 📚 Additional Resources

- [Apache HTTP Server Documentation](https://httpd.apache.org/docs/)
- [BIND9 Documentation](https://bind9.readthedocs.io/)
- [AWS Documentation](https://docs.aws.amazon.com/)
- [DevOps Roadmap](https://roadmap.sh/devops)

---

## 🔗 Connect

Feel free to reach out for collaboration or discussion about DevOps practices and infrastructure automation.

---

**Built with ☕ and determination to master production systems**