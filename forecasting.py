import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import mean_absolute_error, r2_score
from pathlib import Path
import joblib

# ===== 1️⃣ Define paths =====
DATA_DIR = Path("data")
MODELS_DIR = Path("models")
DATA_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

# ===== 2️⃣ Load data =====
assessments_file = DATA_DIR / "student_assessments.csv"
rank_file = DATA_DIR / "student_rank_range_latest.csv"

data = pd.read_csv(assessments_file)
rank = pd.read_csv(rank_file)

# ===== 3️⃣ Merge student rank into dataset =====
data = data.merge(rank[["P_ID", "Rank_Range"]], on="P_ID", how="left")

# ===== 4️⃣ Encode Topics =====
data["TopicsInvolved"] = data["TopicsInvolved"].apply(lambda x: list(map(int, str(x).split())))
mlb = MultiLabelBinarizer()
topic_encoded = mlb.fit_transform(data["TopicsInvolved"])
topic_df = pd.DataFrame(topic_encoded, columns=[f"Topic_{t}" for t in mlb.classes_])
data = pd.concat([data.drop("TopicsInvolved", axis=1), topic_df], axis=1)

# ===== 5️⃣ Encode Rank Range =====
data = pd.get_dummies(data, columns=["Rank_Range"], drop_first=True)

# ===== 6️⃣ Prepare features and target =====
X = data.drop(columns=["P_ID", "Estimation_time"])
y = data["Estimation_time"]

# ===== 7️⃣ Train/test split =====
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# ===== 8️⃣ Train model =====
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# ===== 9️⃣ Evaluate model =====
y_pred = rf_model.predict(X_test)
print("✅ Model Evaluation")
print(f"Mean Absolute Error: {mean_absolute_error(y_test, y_pred):.2f}")
print(f"R² Score: {r2_score(y_test, y_pred):.2f}")

# ===== 🔟 Save model =====
model_path = MODELS_DIR / "completion_forecast_model.pkl"
joblib.dump(rf_model, model_path)
print(f"✅ Model saved at: {model_path}")

# ===== 11️⃣ Example prediction =====
example_student = pd.DataFrame({
    "Completion_time": [120],
    "Rate_Diff_By_Tutor": [4],
    "Rank_Range_High": [1],
    "Rank_Range_Mid": [0],
    "Rank_Range_Low": [0],
    "Topic_101": [1],
    "Topic_102": [0],
    "Topic_103": [1]
})

predicted_time = rf_model.predict(example_student)[0]
print(f"\nPredicted Completion Time for new assessment: {predicted_time:.2f} minutes")
