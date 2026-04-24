import pandas as pd

def build_input(pred_duration, pred_title, pred_money, pred_question, pred_numbers,
                pred_hour, pred_weekend, df):

    return pd.DataFrame([{
        "duration_seconds": pred_duration,
        "title_length": len(pred_title) if pred_title else 0,
        "has_money_symbol": int(pred_money),
        "has_question_mark": int(pred_question),
        "has_numbers": int(pred_numbers),
        "publish_hour_utc": pred_hour,
        "is_weekend": int(pred_weekend),

        "rolling_avg_views_5": df["raw_views"].mean(),
        "rolling_avg_engagement_5": df["engagement_rate_pct"].mean(),
        "rolling_avg_duration_5": df["duration_seconds"].mean(),

        "prev_video_views": df["raw_views"].mean(),
        "prev_video_engagement": df["engagement_rate_pct"].mean(),
        "prev_video_has_money": int(pred_money)
    }])