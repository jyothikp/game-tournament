FROM python:3

WORKDIR /code/game/

COPY consumer.py .
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN python3 -m pip install -i https://test.pypi.org/simple/ game-tournament==0.10.0


ENV PYTHONUNBUFFERED=1

CMD ["python", "/code/game/consumer.py"]