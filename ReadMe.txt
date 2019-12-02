to run the app: 


--- docker ---:
run: 
docker-compose up

or
run:
docker build -t flask-docker .
docker run --name my_flask_container -p 5000:5000 flask-docker


--- direct run --- : (you should have pip and python)
pip install -r requirement.txt
flask run (or specify port: flask run --host=0.0.0.0 --port=5000)