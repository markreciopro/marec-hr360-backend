import pandas as pd

def generate_insights(df, analytics):
    insights = []
    recommendations = []

    headcount = analytics.get("headcount", 0)
    attrition = analytics.get("attrition", 0)
    avg_salary = analytics.get("avg_salary", 0)
    avg_tenure = analytics.get("avg_tenure", 0)

    # =========================
    # ATTRITION INSIGHT
    # =========================
    if attrition > 20:
        insights.append("High attrition detected across workforce.")
        recommendations.append("🚨 Immediate retention strategy required (exit interviews, compensation review).")

    elif attrition > 10:
        insights.append("Moderate attrition observed.")
        recommendations.append("⚠️ Monitor turnover trends and engagement levels.")

    else:
        insights.append("Attrition is within a healthy range.")
        recommendations.append("✅ Maintain current workforce strategy.")

    # =========================
    # SALARY INSIGHT
    # =========================
    if avg_salary < 45000:
        insights.append("Average salary is below market benchmark.")
        recommendations.append("💰 Review compensation structure to remain competitive.")

    elif avg_salary > 120000:
        insights.append("High salary distribution detected.")
        recommendations.append("📊 Optimize compensation efficiency and ROI.")

    # =========================
    # TENURE INSIGHT
    # =========================
    if avg_tenure < 2:
        insights.append("Low employee tenure suggests retention issues.")
        recommendations.append("🧩 Improve onboarding and early engagement programs.")

    elif avg_tenure > 6:
        insights.append("High tenure workforce indicates strong retention.")
        recommendations.append("🏆 Leverage experienced employees for leadership development.")

    # =========================
    # DEPARTMENT RISK
    # =========================
    if "dept" in df.columns:
        dept_counts = df["dept"].value_counts()

        if not dept_counts.empty:
            largest_dept = dept_counts.idxmax()
            insights.append(f"{largest_dept} department has the highest headcount.")
            recommendations.append(f"📌 Focus workforce planning on {largest_dept} team.")

    return {
        "insights": insights,
        "recommendations": recommendations
    }