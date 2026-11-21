![Status](https://img.shields.io/badge/status-completed-brightgreen)
![Maintenance](https://img.shields.io/badge/maintenance-stopped-red)

> [!NOTE]  
> **Completed as part of a summer internship project**  
> and now its no longer actively maintained.

# VulnShop

This repo contains a vulnerable web application built using Python Flask + SQLite + HTML/CSS/JavaScript.

It contains 4 major vulnerabilities:

- **Vulnerability 1** — Cross-Site Scripting (XSS)
- **Vulnerability 2** — SQL Injection (SQLi)
- **Vulnerability 3** — Authentication Bypass
- **Vulnerability 4** — Cross-Site Request Forgery (CSRF)

## Setup

You can use Docker to spawn the lab quickly (**Recommended**)

```bash
docker pull sensurajit/vulnshop
```

```bash
docker build -t vulnshop
```

Then run:

```bash
docker run -it --rm -d -p 5000:5000 --name vulnshop vulnshop:latest
```

---

**Or** you can clone the repo and run it locally:

```bash
pip install -r requirements.txt
```

Create the database first:

```bash
python3 database.py
```

Once done, start the application:

```bash
python3 app.py
```

Now head over to **http://127.0.0.1:5000**

---


