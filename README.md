# Bufflehead Prediction Microservice

This project implements a containerized machine learning microservice that predicts bufflehead bird counts based on environmental and temporal inputs. The model is built using Google BigQuery AutoML and is served through a FastAPI-based web application.


## Overview

The application allows users to input parameters such as location, date, month, year, temperature, wind speed, and precipitation through a web interface. These inputs are sent to a BigQuery ML model, which returns a prediction about bufflehead count.

The service is containerized using Docker and deployed on Google Cloud Run for public access.


## Technologies Used

- Python (FastAPI)
- Jinja2 (HTML templating)
- Google BigQuery ML (AutoML Regressor)
- Docker (containerization)
- Google Cloud Run (deployment)

