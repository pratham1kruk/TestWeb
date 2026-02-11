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
| **Networking** | Resolver manipulation and WSL networking |
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