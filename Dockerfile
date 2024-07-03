FROM python:3

WORKDIR /app

COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install prisma

COPY prisma/schema.prisma /app/prisma/

RUN prisma generate

# Make port 80 available to the world outside this container
EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
