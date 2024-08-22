# start-react-django

Python script to automate the creation of web apps with react frontend and django backend.

## Usage

`start-react-django [-h] [-env NAME] [-ts] [-cors] name`

The command is available once the start-react-django module has been installed, this can be done locally:

```bash
pip install -e .
```

## Django & React

### React

Once the command has finished the react web app can be built using:

```bash
npm run dev
```

to compile and watch for changes, or to compile a production build:

```bash
npm run build
```

### Django

To serve this and start the django API we run:

```bash
python manage.py runserver
```

from within

## Authors

- [@jcbyte](https://www.github.com/jcbyte)
