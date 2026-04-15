import os
from io import StringIO

import pandas as pd
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Dashboard Trust Auditor", layout="wide")
st.title("Dashboard Trust Auditor")
st.caption("Audit dashboard data for trust gaps, anomalies, and logical inconsistencies.")

# -----------------------------
# Upload / Sample Data
# -----------------------------
uploaded_file = st.file_uploader("Upload data", type=["csv"])

sample_csv = """date,active_users,new_users,transactions,revenue,avg_order_value,refunds,marketing_spend
2026-03-01,1200,300,180,36000,200,5,8000
2026-03-08,1500,400,250,30000,200,3,9700
2026-03-09,1550,420,260,52000,200,2,10000
"""

if st.button("Load Sample Data"):
    uploaded_file = StringIO(sample_csv)

if uploaded_file is None:
    st.warning("Upload a CSV to start auditing")
    st.stop()

# -----------------------------
# Read and validate data
# -----------------------------
df = pd.read_csv(uploaded_file)
df.columns = df.columns.str.strip().str.lower()

required_columns = [
    "date",
    "active_users",
    "new_users",
    "transactions",
    "revenue",
    "avg_order_value",
    "refunds",
    "marketing_spend",
]

missing = [col for col in required_columns if col not in df.columns]

if missing:
    st.error(f"Missing columns: {missing}")
    st.stop()

df["date"] = pd.to_datetime(df["date"], errors="coerce")

numeric_cols = [
    "active_users",
    "new_users",
    "transactions",
    "revenue",
    "avg_order_value",
    "refunds",
    "marketing_spend",
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.sort_values("date").reset_index(drop=True)

# -----------------------------
# Core calculations
# -----------------------------
df["expected_revenue"] = df["transactions"] * df["avg_order_value"]
df["revenue_gap"] = df["revenue"] - df["expected_revenue"]

mismatch = df[df["revenue"] != df["expected_revenue"]]

mean = df["revenue"].mean()
std = df["revenue"].std()

if std == 0 or pd.isna(std):
    df["zscore"] = 0
else:
    df["zscore"] = (df["revenue"] - mean) / std

anomalies = df[df["zscore"].abs() > 2]

df["prev_revenue"] = df["revenue"].shift(1)
df["prev_transactions"] = df["transactions"].shift(1)

logic_issue = df[
    (df["revenue"] < df["prev_revenue"]) &
    (df["transactions"] > df["prev_transactions"])
]

# -----------------------------
# Trust score
# -----------------------------
trust_score = 100
trust_score -= len(mismatch) * 15
trust_score -= len(anomalies) * 10
trust_score -= len(logic_issue) * 10

if df["avg_order_value"].nunique() == 1:
    trust_score -= 5

trust_score = max(0, trust_score)

# -----------------------------
# Issues list
# -----------------------------
issues = []

if not mismatch.empty:
    for _, row in mismatch.iterrows():
        issues.append(
            f"Revenue mismatch on {row['date'].date()}: expected {row['expected_revenue']}, actual {row['revenue']}."
        )

if not anomalies.empty:
    for _, row in anomalies.iterrows():
        issues.append(
            f"Revenue anomaly on {row['date'].date()}: revenue {row['revenue']} with z-score {row['zscore']:.2f}."
        )

if not logic_issue.empty:
    for _, row in logic_issue.iterrows():
        issues.append(
            f"Logical inconsistency on {row['date'].date()}: transactions increased while revenue declined."
        )

if df["avg_order_value"].nunique() == 1:
    issues.append(
        "Average order value is constant across the dataset, which may indicate over-aggregated or synthetic data."
    )

# -----------------------------
# Rule-based summary
# -----------------------------
def generate_rule_based_summary(issues, trust_score):
    if not issues:
        return f"No major trust issues were detected. Overall trust score is {trust_score}/100."

    return (
        f"The audit detected {len(issues)} issue(s). "
        f"The dashboard trust score is {trust_score}/100. "
        "The data may contain inconsistencies, anomalies, or overly clean patterns that should be investigated."
    )

# -----------------------------
# AI summary
# -----------------------------
def generate_ai_summary(issues, trust_score):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return generate_rule_based_summary(issues, trust_score)

    if not issues:
        return f"No major trust issues were detected. Overall trust score is {trust_score}/100."

    try:
        client = OpenAI(api_key=api_key)

        prompt = f"""
You are a product analytics auditor.

A dashboard dataset was analyzed and received a trust score of {trust_score}/100.

Detected issues:
{chr(10).join("- " + issue for issue in issues)}

Write a concise business-friendly summary in 4-5 lines.
Explain:
1. what is wrong,
2. why it matters,
3. likely causes,
4. what should be investigated next.

Do not use bullets.
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You explain analytics trust issues for product and business teams."
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return (
            f"{generate_rule_based_summary(issues, trust_score)} "
            f"AI summary could not be generated: {e}"
        )

summary = generate_ai_summary(issues, trust_score)

# -----------------------------
# Recommendations
# -----------------------------
def get_recommendations(issues):
    recommendations = []
    issue_text = " ".join(issues).lower()

    if "revenue mismatch" in issue_text:
        recommendations.append("Verify revenue aggregation logic and source-to-dashboard mapping.")
    if "anomaly" in issue_text:
        recommendations.append("Check whether the anomaly was caused by a real business event or a data pipeline issue.")
    if "logical inconsistency" in issue_text:
        recommendations.append("Review event tracking, joins, and transformation logic for transaction and revenue metrics.")
    if "constant" in issue_text:
        recommendations.append("Validate whether average order value is hardcoded, defaulted, or overly aggregated.")

    if not recommendations:
        recommendations.append("No immediate follow-up actions required.")

    return recommendations

# -----------------------------
# Issue table
# -----------------------------
issue_rows = []

if not mismatch.empty:
    for _, row in mismatch.iterrows():
        issue_rows.append({
            "date": row["date"].date(),
            "issue_type": "Revenue mismatch",
            "details": f"Expected {row['expected_revenue']}, actual {row['revenue']}"
        })

if not anomalies.empty:
    for _, row in anomalies.iterrows():
        issue_rows.append({
            "date": row["date"].date(),
            "issue_type": "Anomaly",
            "details": f"Revenue {row['revenue']} (z-score {row['zscore']:.2f})"
        })

if not logic_issue.empty:
    for _, row in logic_issue.iterrows():
        issue_rows.append({
            "date": row["date"].date(),
            "issue_type": "Logical inconsistency",
            "details": "Transactions increased but revenue dropped"
        })

if df["avg_order_value"].nunique() == 1:
    issue_rows.append({
        "date": "All",
        "issue_type": "Too perfect metric",
        "details": "avg_order_value is constant"
    })

issue_df = pd.DataFrame(issue_rows)

# -----------------------------
# Trust label
# -----------------------------
def get_trust_label(score):
    if score >= 85:
        return "High Trust"
    elif score >= 65:
        return "Medium Trust"
    return "Low Trust"

label = get_trust_label(trust_score)

# -----------------------------
# UI Rendering
# -----------------------------
st.subheader("Trust Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Trust Score", f"{trust_score}/100")
col2.metric("Issues Detected", len(issues))
col3.metric("Rows Analyzed", len(df))

st.subheader("Audit Verdict")
if label == "High Trust":
    st.success(label)
elif label == "Medium Trust":
    st.warning(label)
else:
    st.error(label)

st.subheader("AI Executive Summary")
st.info(summary)

st.subheader("Recommended Next Checks")
for rec in get_recommendations(issues):
    st.write(f"- {rec}")

st.subheader("Revenue Validation")
st.line_chart(df.set_index("date")[["revenue", "expected_revenue"]])

st.subheader("Revenue Gap (Actual vs Expected)")
st.bar_chart(df.set_index("date")["revenue_gap"])

st.subheader("Volume Trends")
st.line_chart(df.set_index("date")[["transactions", "active_users", "new_users"]])

st.subheader("Detected Issues")
if issues:
    for issue in issues:
        st.warning(issue)
else:
    st.success("No major issues detected.")

st.subheader("Issue Details Table")
if not issue_df.empty:
    st.dataframe(issue_df, use_container_width=True)
else:
    st.write("No issue details to display.")

st.subheader("Analyzed Data")
st.write("Columns:", df.columns.tolist())
st.dataframe(df, use_container_width=True)

