# DaangnMarket_Back-End
DaangnMarket clone project

## Table of contents
- [Prerequisites](#Prerequisites)
- [Installation](#Installation)
- [Setup](#Setup)
- [Deploy](#Deploy)
- [API document](#API document)

## Prerequisites
### Secrets JSON File
`<project-root>/secrets.json`
<details><summary><b>Show Sample</b></summary>

```json
{
    "base": {
        "HOST": "13.125.217.34",
        "SENTRY_DSN": "<SENTRY dsn>",
        "SECRET_KEY": "<SENTRY key>"
    },
    "dev": {
        "DATABASES": {
            "default": {
                "ENGINE": "django.contrib.gis.db.backends.postgis",
                "NAME": "db_daangn",
                "USER": "jam",
                "HOST": "localhost"
            }
        }
    },
    "production": {
        "DATABASES": {
            "default": {
                "ENGINE": "django.contrib.gis.db.backends.postgis",
                "NAME": "<RDS db_name>",
                "USER": "<RDS db_user>",
                "PASSWORD": "<RDS db_password>",
                "HOST": "<RDS Host URI>",
                "PORT": 5432
            }
        },
        "AWS_IAM_S3": {
            "AWS_ACCESS_KEY_ID": "<AWS AccessKeyID (S3 permission)>",
            "AWS_SECRET_ACCESS_KEY": "<AWS SecretAccessKey (S3 permission)>",
            "AWS_STORAGE_BUCKET_NAME": "<AWS Bucket Name>"
        }
    }
}
```

</details>

### Firebase SDK
```sh
$ pip install firebase-admin
```

### Firebase Config JSON
`<project-root>/serviceAccountKey.json`

### [GeoDjango](https://docs.djangoproject.com/en/3.0/ref/contrib/gis/install/#homebrew)  
<details><summary><b>Show requirements</b></summary>

    ```
    // on mac
    $ brew install postgresql
    $ brew install postgis
    $ brew install gdal
    $ brew install libgeoip
    ```
    
</details>

## Installation
```sh
$ pip install -r requirements.txt
```
## Setup
### Database
`POSTGIS="2.5.2 r17328"`

### Extension
- `drf-yasg` : API description generator
- `sentry-sdk`: Error Tracking
- `django-debug-toolbar`: Debuging helper
- `django-extensions`: shell helper

### Dependency
`poetry>=0.12`로 관리
<details><summary><b>Show list</b></summary>

```toml
[tool.poetry.dependencies]
python = "^3.7"
django = "^3.0.4"
djangorestframework = "^3.11.0"
django-filter = "^2.2.0"
markdown = "^3.2.1"
django-import-export = "^2.0.2"
psycopg2-binary = "^2.8.4"
Pillow = "^7.0.0"
requests = "^2.23.0"
supervisor = "^4.1.0"
gunicorn = "^20.0.4"
drf-yasg = "^1.17.1"
sentry-sdk = "^0.14.3"
ssv = "^0.1.1"
flex = "^6.14.1"
firebase-admin = "^4.0.0"
django-cors-headers = "^3.2.1"
django-push-notifications = "^2.0.0"
django-storages = "^1.9.1"
boto3 = "^1.12.39"

[tool.poetry.dev-dependencies]
django-debug-toolbar = "^2.2"
django-extensions = "^2.2.9"
```

</details>

## Deploy
```sh
$ <project-root>/deploy.py
```

## API document
[daangn.shinjam.xyz/docs](http://daangn.shinjam.xyz/docs)
