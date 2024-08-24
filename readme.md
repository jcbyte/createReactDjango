# start-react-django

Python script to automate the creation of web apps with react frontend and django backend.

## Usage

`start-react-django [-h] [-env NAME] [-ts] [-cors] name`

The command is available once the start-react-django module has been installed, this can be done through pip:

```bash
pip install git+https://github.com/jcbyte/start-react-django.git
```

## Django & React

### React

**Note:** These commands should be run from within `$PROJNAME$\frontend\`.

Once the project has been created the react web app can be compiled whilst watching for changes using:

```bash
npm run dev
```

To compile a production build:

```bash
npm run build
```

### Django

**Note:** These commands should be run from within `$PROJNAME$\`.

To serve the app and start the django API we run:

```bash
python manage.py runserver
```

## Authors

- [@jcbyte](https://www.github.com/jcbyte)
