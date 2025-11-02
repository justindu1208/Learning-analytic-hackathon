import pandas as pd
from pathlib import Path

# ===== 1️⃣ Set up data paths =====
DATA_DIR = Path("data")  # folder containing your CSVs
DATA_DIR.mkdir(exist_ok=True)  # create folder if it doesn't exist

marks_file = DATA_DIR / "student_marks.csv"
latest_rank_file = DATA_DIR / "student_rank_range_latest.csv"
history_rank_file = DATA_DIR / "student_rank_range_history.csv"

# ===== 2️⃣ Load marks data =====
# Make sure 'student_marks.csv' is inside the 'data/' folder
marks = pd.read_csv(marks_file)  # columns: P_ID, Module, Mark

# ===== 3️⃣ Calculate average mark and rank =====
rank_df = (
    marks.groupby("P_ID")["Mark"].mean().reset_index()
    .rename(columns={"Mark": "Avg_Mark"})
)
rank_df["Percentile"] = rank_df["Avg_Mark"].rank(pct=True, ascending=True) * 100

# ===== 4️⃣ Categorize into rank ranges =====
def rank_category(p):
    if p >= 80:
        return "High"
    elif p >= 50:
        return "Mid"
    else:
        return "Low"

rank_df["Rank_Range"] = rank_df["Percentile"].apply(rank_category)

# ===== 5️⃣ Save results =====
# (A) Overwrite latest version for use in prediction
rank_df.to_csv(latest_rank_file, index=False)

# (B) Append new records to historical version
rank_df["Generated_Date"] = pd.Timestamp.now()
rank_df.to_csv(history_rank_file, mode="a", header=not history_rank_file.exists(), index=False)

print("✅ Student rank range files created:")
print(f" - Latest version: {latest_rank_file}")
print(f" - History version: {history_rank_file}")

print("\nPreview of latest ranks:")
print(rank_df.head())
