import gradio as gr

def build_ui(model, feature_cols, predict_fn):
    with gr.Blocks() as demo:
        gr.Markdown("## 🛒 Retail Sales Prediction App")

        with gr.Row():
            promo = gr.Radio([0, 1], label="Promo", value=0)
            holiday = gr.Radio([0, 1], label="Holiday", value=0)

        date = gr.Textbox(label="Date (YYYY-MM-DD)", value="2023-11-01")

        with gr.Row():
            lag_1 = gr.Number(label="Sales Lag 1 Day", value=100)
            lag_7 = gr.Number(label="Sales Lag 7 Days", value=120)
            mean_3 = gr.Number(label="Rolling Mean (3 Days)", value=110)
            mean_7 = gr.Number(label="Rolling Mean (7 Days)", value=115)

        predict_btn = gr.Button("Predict Sales")
        output = gr.Number(label="Predicted Sales", precision=2)

        predict_btn.click(
            fn=lambda p, h, d, l1, l7, m3, m7: predict_fn(model, feature_cols, p, h, d, l1, l7, m3, m7),
            inputs=[promo, holiday, date, lag_1, lag_7, mean_3, mean_7],
            outputs=output
        )

    return demo
