import requests
import json
import os
import snowflake.connector
from datetime import datetime

# -------------------------------
# ENV VARIABLES (NO HARDCODED SECRETS)
# -------------------------------
API_KEY = os.getenv("YOUTUBE_API_KEY")

SNOWFLAKE_CONFIG = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    "database": os.getenv("SNOWFLAKE_DATABASE"),
    "schema": os.getenv("SNOWFLAKE_SCHEMA"),
}

CHANNEL_ID = "UCX6OQ3DkcsbYNE6H8uQQuVA"


# -------------------------------
# FETCH YOUTUBE DATA
# -------------------------------
def fetch_mrbeast_videos():
    print("📡 Fetching YouTube videos...")

    url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "channelId": CHANNEL_ID,
        "maxResults": 30,
        "type": "video",
        "order": "date",
        "key": API_KEY,
    }

    response = requests.get(url, params=params)
    data = response.json()

    video_ids = []

    for item in data.get("items", []):
        vid = item.get("id", {}).get("videoId")
        if vid:
            video_ids.append(vid)

    if not video_ids:
        raise Exception("No videos returned from API")

    print(f"✅ Found {len(video_ids)} videos")

    # Get details
    details_url = "https://www.googleapis.com/youtube/v3/videos"

    details_params = {
        "part": "snippet,statistics,contentDetails",
        "id": ",".join(video_ids),
        "key": API_KEY,
    }

    details_response = requests.get(details_url, params=details_params)

    return details_response.json()


# -------------------------------
# SAVE AS NDJSON
# -------------------------------
def save_as_ndjson(data):
    if not data or "items" not in data:
        raise Exception("Invalid API response")

    filename = "mrbeast_bronze.ndjson"

    with open(filename, "w", encoding="utf-8") as f:
        for item in data["items"]:
            envelope = {
                "video_id": item.get("id"),
                "channel_id": CHANNEL_ID,
                "channel_name": "MrBeast",
                "video_title": item.get("snippet", {}).get("title"),
                "published_at": item.get("snippet", {}).get("publishedAt"),
                "raw_api_response": item,
                "ingested_at": datetime.utcnow().isoformat(),
            }

            f.write(json.dumps(envelope) + "\n")

    print(f"💾 Saved {len(data['items'])} records")

    return filename


# -------------------------------
# UPLOAD TO SNOWFLAKE BRONZE
# -------------------------------
def upload_to_bronze(filename):
    print("☁️ Uploading to Snowflake...")

    conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
    cursor = conn.cursor()

    try:
        cursor.execute("CREATE OR REPLACE TEMP STAGE bronze_stage")

        abs_path = os.path.abspath(filename)

        cursor.execute(
            f"PUT file://{abs_path} @bronze_stage AUTO_COMPRESS=FALSE OVERWRITE=TRUE"
        )

        cursor.execute(
            """
            COPY INTO BRONZE.RAW_YOUTUBE (raw_data)
            FROM @bronze_stage
            FILE_FORMAT = (TYPE = JSON)
            ON_ERROR = 'CONTINUE'
            """
        )

        cursor.execute("SELECT COUNT(*) FROM BRONZE.RAW_YOUTUBE")
        count = cursor.fetchone()[0]

        conn.commit()

        print(f"✅ Loaded {count} records into BRONZE")

        return count

    finally:
        cursor.close()
        conn.close()


# -------------------------------
# MAIN PIPELINE
# -------------------------------
def main():
    print("=" * 60)
    print("🚀 MRBEAST BRONZE INGESTION PIPELINE")
    print("=" * 60)

    if not API_KEY:
        raise Exception("Missing YOUTUBE_API_KEY environment variable")

    # 1. Fetch
    data = fetch_mrbeast_videos()

    # 2. Save
    file = save_as_ndjson(data)

    # 3. Upload
    count = upload_to_bronze(file)

    # 4. Cleanup
    os.remove(file)

    print("🧹 Temporary file cleaned")

    print("=" * 60)
    print(f"🎉 DONE — {count} records loaded into Snowflake")
    print("=" * 60)


if __name__ == "__main__":
    main()