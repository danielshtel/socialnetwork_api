# SocialNetwork API

### Clone the project

```shell
git clone git@github.com:danielshtel/socialnetwork_api.git
```

### Settings:

*Create `.env` file in project root directory and set your values*

```shell
SERVER_HOST = your host-value here
SERVER_PORT = your port-value here
DB_PATH = your db connection path here
```

**❗DEFAULT VALUES❗**

```shell
SERVER_HOST=0.0.0.0
SERVER_PORT=80
DB_PATH=sqlite:///./instafood_db
```

## Installation:

### Manual:

<details>
    <summary>Click</summary>

*1. Change directory*

```shell
cd socialnetwork_api
```

*2. Create virtual environment*

```shell
python -m venv venv
```

*3. Activate venv*

```shell
source venv/bin/activate
```

*4. Install dependencies*

```shell
pip install -r requirements.txt
```

#### Initialize database:

```shell
python database.py
```

#### Run the project:

```shell
python main.py
```

</details>

### Docker-compose:

<details>

<summary>Click</summary>

**Make sure you set environment variables in `.env`**

#### To start container:

```shell
docker-compose up -d
```

#### To stop container:

```shell
docker-compose stop
```

</details>

# Usage

**Go to http://localhost/docs to view interactive API docs**
