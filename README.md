# Dashboard Trust Auditor

An AI-powered tool that audits dashboard reliability by detecting anomalies, metric inconsistencies, and logical trust gaps before they affect business decisions.

## Why this matters

Most dashboards do not fail loudly. They fail silently.

When revenue does not reconcile, related metrics move in conflicting directions, or data appears suspiciously perfect, teams lose trust and start relying on manual workarounds. This tool adds a trust layer on top of analytics systems.

---

## 🚀 Features

- ✅ **Metric Consistency Validation**  
  Ensures relationships like Revenue = Transactions × Average Order Value are accurate.

- 📊 **Anomaly Detection**  
  Identifies unusual patterns using statistical techniques such as z-score analysis.

- ⚠️ **Logical Inconsistency Checks**  
  Flags contradictions across metrics (e.g., rising transactions but declining revenue).

- 📉 **Trust Score Generation**  
  Quantifies dashboard reliability on a scale of 0–100.

- 🤖 **AI-Powered Executive Summaries**  
  Converts technical issues into business-friendly insights using AI.

- 📈 **Interactive Visualizations**  
  Provides intuitive dashboards built with Streamlit.

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
