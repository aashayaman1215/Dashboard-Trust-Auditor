# Dashboard Trust Auditor

An AI-powered tool that audits dashboard reliability by detecting anomalies, metric inconsistencies, and logical trust gaps before they affect business decisions.

## Why this matters

Most dashboards do not fail loudly. They fail silently.

When revenue does not reconcile, related metrics move in conflicting directions, or data appears suspiciously perfect, teams lose trust and start relying on manual workarounds. This tool adds a trust layer on top of analytics systems.

---

## 🚀 Features

- ✅ Metric Consistency Validation
- 📊 Anomaly Detection using Statistical Methods
- ⚠️ Logical Inconsistency Checks
- 📉 Trust Score Generation
- 🤖 AI-Powered Executive Summaries
- 📈 Interactive Visualizations using Streamlit

---

## 🛠️ Tech Stack

- **Python**
- **Pandas**
- **NumPy**
- **Streamlit**
- **OpenAI API**

---

## 📸 Demo

### Dashboard Overview
![Dashboard Screenshot](assets/dashboard_screenshot.png)

### Architecture Diagram
![Architecture Diagram](assets/architecture_diagram.png)

---

## 🏗️ Architecture Overview

```plaintext
CSV Upload
    ↓
Data Validation & Preprocessing
    ↓
Trust Checks Engine
(Metric Consistency, Anomaly Detection, Logical Validation)
    ↓
Trust Score & AI Insights
    ↓
Interactive Streamlit Dashboard
