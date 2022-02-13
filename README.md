# Comment_app

>Recommend using **Python 3** for this project

**Everything is done in windows terminal or command line **

>Installing virtual environment

```
py -m pip install --user virtualenv
```

>Then for installing required frameworks:

```
 python get-pip.py

 python -m pip install --upgrade pip
``` 

* Navigate to `Comment_app` project and setup a virtual environment in Python
```
cd Comment_app
python -m venv env
```

* Activate the virtual environment on linux
```
source env/Scripts/activate
```
*on windows
```
env/Scripts/activate
```

* Navigate to src folder and install all project and developer dependencies
```
mkdir src
cd src
pip install -r ../requirements.txt
cd ..
```


> Running flask server:

```
 python app.py
```


*
**For creating a new database file[optional]**
```
python
>>from app import db
>>db.create_all()
>>quit()
```

