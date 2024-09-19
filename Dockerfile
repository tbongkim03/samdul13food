FROM python:3.11

WORKDIR /code

# COPY . /code/
COPY src/samdul13food/main.py /code/
# COPY requirements.txt /code/

RUN pip install --no-cache-dir --upgrade git+https://github.com/Seokxkyu/samdul13food.git@main

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
