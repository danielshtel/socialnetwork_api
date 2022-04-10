# socialnetwork_api

# Installation

*Clone the project*

```shell
git clone git@github.com:DaniilLevchenko/socialnetwork_api.git
```

*Change dir*

```shell
cd socialnetwork_api
```

*Create virtual environment*

```shell
python -m venv venv
```

*Activate venv*

```shell
source venv/bin/activate
```

*Install dependencies*

```shell
pip install -r requirements.txt
```

# Settings

*Create `.env` file in project root directory and set your values*

```shell
SERVER_HOST = your host-value here
SERVER_PORT = your port-value here
DB_PATH = your db connection path here
```

**❗DEFAULT VALUES❗**

```shell
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DB_PATH=sqlite:///./instafood_db
```

# Run project

*CLI*

```shell
python main.py
```

# Usage

*Go to http://0.0.0.0:8000/docs to view interactive API docs*
