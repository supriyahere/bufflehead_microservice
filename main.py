from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from google.cloud import bigquery

app = FastAPI()
templates = Jinja2Templates(directory="templates")

PROJECT_ID = "bufflehead-migration-analysis"
DATASET = "bufflehead_us"
MODEL = "automl_bufflehead_count"

client = bigquery.Client()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/predict", response_class=HTMLResponse)
def predict(
    request: Request,
    locality: str = Form(...),
    eventdate: str = Form(...),
    month: int = Form(...),
    winter_season: int = Form(...),
    day_of_year: int = Form(...),
    avg_wind_speed: float = Form(...),
    year: int = Form(...),
    avg_temp: float = Form(...),
    day: int = Form(...),
    avg_precipitation: float = Form(...)
):
    try:
        query = f"""
        SELECT *
        FROM ML.PREDICT(
          MODEL `{PROJECT_ID}.{DATASET}.{MODEL}`,
          (
            SELECT
              '{locality}' AS locality,
              DATE('{eventdate}') AS eventdate,
              {month} AS month,
              {winter_season} AS winter_season,
              {day_of_year} AS day_of_year,
              {avg_wind_speed} AS avg_wind_speed,
              {year} AS year,
              {avg_temp} AS avg_temp,
              {day} AS day,
              {avg_precipitation} AS avg_precipitation
          )
        )
        """

        results = client.query(query).result()

        prediction = None
        for row in results:
            prediction = row.predicted_individualcount

        return templates.TemplateResponse(
            "result.html",
            {"request": request, "prediction": prediction}
        )

    except Exception as e:
        return templates.TemplateResponse(
            "result.html",
            {"request": request, "prediction": f"Error: {str(e)}"}
        )
