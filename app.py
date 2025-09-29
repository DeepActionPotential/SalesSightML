from utils import load_artifacts, predict_sales
from ui import build_ui

if __name__ == "__main__":
    model, feature_cols = load_artifacts()
    iface = build_ui(model, feature_cols, predict_sales)
    iface.launch()
