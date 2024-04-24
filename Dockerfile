FROM python:alpine
WORKDIR /app
#ici on met tt les dependences
COPY dependence.txt .
RUN pip install -r dependence.txt
#bach tcopier les fichier diawlk 
COPY . .
CMD [ "uvicorn", "app:app", "--host","0.0.0.0", "--port", "3000" ]