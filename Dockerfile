FROM python:3

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8501

CMD [ "streamlit", "run", "uber_pickups.py" ]
