# Banking system

### To install and boot this service you would need the following:

> Python 3.8.* \
> Pip3 22.3.* (or any other compatible with Python 3.8)

### Pull the dependencies using the following command

```commandline
pip3 install -r requirements.txt      
```

### Boot it via gunicorn with the command below

```commandline
gunicorn app.main:app -b localhost:8080
```

where `app.main:app` is the reference to the app, and `-b localhost:8080` is bind for a server socket.</br>

You could also specify `-w` parameter and pass an int, which specifies the number of worker processes
