# GadgetZone E-commerce Shop

An online E-commerce store made with Python Django.

| Previews                                                                                     |
| -------------------------------------------------------------------------------------------- |
| *Homepage*<br/><img src="previews/1.png" title="" alt="" width="372">                        |
| *Admin panel*<br/><img title="" src="previews/2.png" alt="" width="358" data-align="inline"> |
| *Customer's dashboard*<br/><img src="previews/3.png" title="" alt="" width="278">            |

---

## Requirements

- Python 3.11 or higher

- smtp4dev

- Git Bash (Optional)

---

## Installation

Open `cmd` or `bash` in the project directory.

**Install Python virtual environment**

```bash
pip install virtualenv
```

**Create a virtual environment**

```bash
virtualenv env_name
```

**Activate virtual environment**

On `Mac` and `Linux` (Also if you are using `bash` on `Windows`)

```bash
source env_name/bin/activate
```

On `Windows` (If you are using `cmd`)

```bash
.\env_name\Scripts\activate
```

**Install dependencies**

```bash
pip install -r requirements.txt
```

---

## Run Locally

**Migrate database**

```bash
python manage.py makemigrations && python manage.py migrate
```

**Create an admin user**

```bash
python manage.py createsuperuser
```

**Run the `Django` server**

```bash
python manage.py runserver
```

**Run the `smtp4dev` server to prevent any potential errors while creating restaurant and customer accounts or carrying out food ordering processes.**

***Or***

**Configure `smtp` in the `settings.py` to use your own email server.**

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.your-email-provider.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-email-App-password'
```

You can access the website at http://127.0.0.1:8000/ and the admin panel at http://127.0.0.1:8000/admin

---

## License

[MIT](https://choosealicense.com/licenses/mit/)
