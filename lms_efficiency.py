import pandas as pd
from pathlib import Path

# ===== 1️⃣ Define paths =====
DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "material_efficiency_report.csv"
DATA_DIR.mkdir(exist_ok=True)

# ===== 2️⃣ Load relevant CSV files =====
lms_activity = pd.read_csv(DATA_DIR / "la_dataset_lms_item_activity_by_session_fact.csv")
lms_item = pd.read_csv(DATA_DIR / "la_dataset_lms_item_dim.csv")
video_activity = pd.read_csv(DATA_DIR / "la_dataset_video_activity_by_view_fact.csv")
outcomes = pd.read_csv(DATA_DIR / "la_dataset_person_module_instance_outcome_fact.csv")

# ===== 3️⃣ Merge and process =====
lms_merged = lms_activity.merge(lms_item, on="LMS_ITEM_ID", how="left")
lms_merged = lms_merged.merge(outcomes, on=["P_ID", "MODULE_INSTANCE_ID"], how="left")

# Aggregate metrics per LMS material
material_stats = (
    lms_merged.groupby(["LMS_ITEM_ID", "MODULE_INSTANCE_ID"])
    .agg({
        "INTERACTION_COUNT": "sum",
        "MARK": "mean"
    })
    .rename(columns={"INTERACTION_COUNT": "Total_Interactions", "MARK": "Avg_Mark_Using"})
    .reset_index()
)

# Average lecture time per module
video_summary = (
    video_activity.groupby("MODULE_INSTANCE_ID")["TOTAL_MINUTES_DELIVERED"]
    .mean().reset_index().rename(columns={"TOTAL_MINUTES_DELIVERED": "Avg_Lecture_Time"})
)

# Merge lecture data
material_stats = material_stats.merge(video_summary, on="MODULE_INSTANCE_ID", how="left")

# Baseline average mark
overall_avg = outcomes["MARK"].mean()

# Calculate Material Efficiency Score (MES)
material_stats["Material_Efficiency_Score"] = (
    (material_stats["Avg_Mark_Using"] - overall_avg)
    / material_stats["Total_Interactions"].replace(0, 1)
)

material_stats = material_stats.sort_values("Material_Efficiency_Score", ascending=False)

# ===== 4️⃣ Save results =====
material_stats.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Material Efficiency Report saved at: {OUTPUT_FILE}")
print(material_stats.head())
