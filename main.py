from fastapi import FastAPI
from fastapi.responses import JSONResponse
from google.cloud import bigquery

app = FastAPI()

PROJECT_ID = "bufflehead-migration-analysis"
DATASET = "bufflehead_us"
MODEL = "automl_bufflehead_count"

client = bigquery.Client()


@app.get("/")
def home():
    return {"message": "Bufflehead Prediction API is running."}


@app.post("/predict")
def predict(data: dict):
    try:
        # validate input
        required_fields = [
            "locality", "eventdate", "month", "winter_season",
            "day_of_year", "avg_wind_speed", "year",
            "avg_temp", "day", "avg_precipitation"
        ]

        for field in required_fields:
            if field not in data:
                return {"error": f"Missing field: {field}"}

        # extract values
        locality = data["locality"]
        eventdate = data["eventdate"]
        month = data["month"]
        winter_season = data["winter_season"]
        day_of_year = data["day_of_year"]
        avg_wind_speed = data["avg_wind_speed"]  # STRING if model expects it
        year = data["year"]
        avg_temp = data["avg_temp"]
        day = data["day"]
        avg_precipitation = data["avg_precipitation"]

        # query
        query = f"""
        SELECT predicted_individualcount
        FROM ML.PREDICT(
          MODEL `{PROJECT_ID}.{DATASET}.{MODEL}`,
          (
            SELECT
              '{locality}' AS locality,
              DATE('{eventdate}') AS eventdate,
              {month} AS month,
              {winter_season} AS winter_season,
              {day_of_year} AS day_of_year,
              '{avg_wind_speed}' AS avg_wind_speed,
              {year} AS year,
              {avg_temp} AS avg_temp,
              {day} AS day,
              {avg_precipitation} AS avg_precipitation
          )
        )
        LIMIT 1
        """

        result = list(client.query(query).result())[0]

        return JSONResponse({
            "predicted_individualcount": float(result["predicted_individualcount"])
        })

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
