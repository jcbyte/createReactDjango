import json
import os
import shutil
import sys
from threading import Event, Thread
from time import sleep


def addToFile(file, startSearch, endSearch, extraContent):
    with open(file, "r") as f:
        content = f.read()
    startPart = content.find(startSearch)
    endPart = len(content[:startPart]) + (content[startPart:]).find(endSearch)
    newPart = content[startPart:endPart]
    newPart += extraContent
    newContent = content[:startPart] + newPart + content[endPart:]
    with open(file, "w") as f:
        f.write(newContent)


# Create api app
if options["api"]:
    cmdCLI(
        sysCmdWheel,
        pythonpath + "manage.py startapp api",
        verbose=options["verbose"],
        before="Creating " + CLIColour("api", "teal") + " app ",
        after=CLIColour("[DONE]\n", "green"),
        wheel=options["verbose"],
    )
    cmdCLI(
        shutil.copy,
        templateFiles + "api\\urls.py",
        "api\\urls.py",
        verbose=options["verbose"],
        before="Creating api\\" + CLIColour("urls.py ", "teal"),
        after=CLIColour("[DONE]\n", "green"),
    )
    cmdCLI(
        shutil.copy,
        templateFiles + "api\\serializers.py",
        "api\\serializers.py",
        verbose=options["verbose"],
        before="Creating api\\" + CLIColour("serializers.py ", "teal"),
        after=CLIColour("[DONE]\n", "green"),
    )

# Setup frontend app and react
cmdCLI(
    shutil.copy,
    templateFiles + "main\\" + ("ts" if options["ts"] else "js") + ".webpack.config.js",
    "webpack.config.js",
    verbose=options["verbose"],
    before="Configuring " + CLIColour("webpack.config.js ", "teal"),
    after=CLIColour("[DONE]\n", "green"),
)
if options["verbose"]:
    sysWrite("Configuring " + CLIColour("package.json ", "teal"))
with open("package.json", "r") as f:
    data = json.load(f)
data["scripts"] = {
    "dev": "webpack --mode development --watch --stats-error-details",
    "build": "webpack --mode production",
}
with open("package.json", "w") as f:
    f.write(json.dumps(data))
if options["verbose"]:
    sysWrite(CLIColour("[DONE]\n", "green"))

cmdCLI(
    os.mkdir,
    "static",
    verbose=options["verbose"],
    before="Creating frontend\\" + CLIColour("static\\ ", "teal"),
    after=CLIColour("[DONE]\n", "green"),
)
cmdCLI(
    os.mkdir,
    "static\\frontend",
    verbose=options["verbose"],
    before="Creating frontend\\static\\" + CLIColour("frontend\\ ", "teal"),
    after=CLIColour("[DONE]\n", "green"),
)
cmdCLI(
    os.mkdir,
    "static\\images",
    verbose=options["verbose"],
    before="Creating frontend\\static\\" + CLIColour("images\\ ", "teal"),
    after=CLIColour("[DONE]\n", "green"),
)
cmdCLI(
    os.mkdir,
    "static\\css",
    verbose=options["verbose"],
    before="Creating frontend\\static\\" + CLIColour("css\\ ", "teal"),
    after=CLIColour("[DONE]\n", "green"),
)
cmdCLI(
    shutil.copy,
    templateFiles + "frontend\\index.css",
    "static\\css\\index.css",
    verbose=options["verbose"],
    before="Creating frontend\\static\\css\\" + CLIColour("index.css ", "teal"),
    after=CLIColour("[DONE]\n", "green"),
)

cmdCLI(
    os.mkdir,
    "src",
    verbose=options["verbose"],
    before="Creating frontend\\" + CLIColour("src\\ ", "teal"),
    after=CLIColour("[DONE]\n", "green"),
)
cmdCLI(
    os.mkdir,
    "src\\components",
    verbose=options["verbose"],
    before="Creating frontend\\src\\" + CLIColour("components\\ ", "teal"),
    after=CLIColour("[DONE]\n", "green"),
)
cmdCLI(
    shutil.copy,
    templateFiles + "frontend\\App." + ("tsx" if options["ts"] else "jsx"),
    "src\\components\\App." + ("tsx" if options["ts"] else "jsx"),
    verbose=options["verbose"],
    before="Creating frontend\\src\\components\\" + CLIColour("App.jsx ", "teal"),
    after=CLIColour("[DONE]\n", "green"),
)
cmdCLI(
    shutil.copy,
    templateFiles + "frontend\\" + ("ts" if options["ts"] else "js") + ".index.js",
    "src\\index.js",
    verbose=options["verbose"],
    before="Creating frontend\\src\\" + CLIColour("index.js ", "teal"),
    after=CLIColour("[DONE]\n", "green"),
)

cmdCLI(
    os.mkdir,
    "templates",
    verbose=options["verbose"],
    before="Creating frontend\\" + CLIColour("templates\\ ", "teal"),
    after=CLIColour("[DONE]\n", "green"),
)
cmdCLI(
    os.mkdir,
    "templates\\frontend",
    verbose=options["verbose"],
    before="Creating frontend\\templates\\" + CLIColour("frontend ", "teal"),
    after=CLIColour("[DONE]\n", "green"),
)
cmdCLI(
    shutil.copy,
    templateFiles + "frontend\\index.html",
    "templates\\frontend\\index.html",
    verbose=options["verbose"],
    before="Creating frontend\\templates\\frontend\\" + CLIColour("index.html ", "teal"),
    after=CLIColour("[DONE]\n", "green"),
)

cmdCLI(
    shutil.copy,
    templateFiles + "frontend\\views.py",
    "views.py",
    verbose=options["verbose"],
    before="Creating frontend\\" + CLIColour("views.py ", "teal"),
    after=CLIColour("[DONE]\n", "green"),
)
cmdCLI(
    shutil.copy,
    templateFiles + "frontend\\urls.py",
    "urls.py",
    verbose=options["verbose"],
    before="Creating frontend\\" + CLIColour("urls.py ", "teal"),
    after=CLIColour("[DONE]\n", "green"),
)

os.chdir("..")

# Finish up
os.chdir(projName)
if options["verbose"]:
    sysWrite("Configuring " + CLIColour("urls.py ", "teal"))
addToFile("urls.py", "from django.urls import path", "\n", ", include")
newUrls = ['path("", include("frontend.urls"))']
if options["api"]:
    newUrls.append('path("api/", include("api.urls"))')
addToFile(
    "urls.py",
    "urlpatterns",
    "]",
    "".join([("\t" + url + ",\n") for url in newUrls]),
)
if options["verbose"]:
    sysWrite(CLIColour("[DONE]\n", "green"))

newSettings = ['"frontend.apps.FrontendConfig"']
if options["api"]:
    newSettings.append('"rest_framework"')
    newSettings.append('"api.apps.ApiConfig"')
if options["cors"]:
    newSettings.append('"corsheaders"')
cmdCLI(
    addToFile,
    "settings.py",
    "INSTALLED_APPS",
    "]",
    "".join([("\t" + setting + ",\n") for setting in newSettings]),
    verbose=options["verbose"],
    before="Configuring " + CLIColour("settings.py ", "teal") + CLIColour("INSTALLED_APPS ", "teal"),
    after=CLIColour("[DONE]\n", "green"),
)
os.chdir("..")

# Extra options
if options["cors"]:
    cmdCLI(
        addToFile,
        projName + "\\settings.py",
        "MIDDLEWARE",
        "]",
        "".join(
            [
                ("\t" + setting + ",\n")
                for setting in [
                    '"corsheaders.middleware.CorsMiddleware"',
                    '"django.middleware.common.CommonMiddleware"',
                ]
            ]
        ),
        verbose=options["verbose"],
        before="Configuring " + CLIColour("settings.py ", "teal") + CLIColour("MIDDLEWARE ", "teal"),
        after=CLIColour("[DONE]\n", "green"),
    )

# Templates
if options["template"]:
    sysWrite("Creating api\\" + CLIColour("views.py ", "teal") + "template ")
    appendText = ""
    with open(templateFiles + "api\\templates\\" + ("jwt." if options["jwt"] else "") + "views.py") as f:
        appendSettings = f.read()
    with open("api\\views.py", "a") as f:
        f.write(appendSettings)
    sysWrite(CLIColour("[DONE]\n", "green"))
    sysWrite("Creating api\\" + CLIColour("urls.py ", "teal") + "template ")
    addToFile(
        "api\\urls.py",
        "",
        "urlpatterns",
        "from .views import Foo\n\n",
    ),
    addToFile("api\\urls.py", "urlpatterns", "]", 'path("Foo", Foo.as_view())'),
    sysWrite(CLIColour("[DONE]\n", "green"))
    cmdCLI(
        shutil.copy,
        templateFiles + "frontend\\templates\\" + ("jwt." if options["jwt"] else "") + "App.tjsx",
        "frontend\\src\\components\\App." + ("tsx" if options["ts"] else "jsx"),
        verbose=options["verbose"],
        before="Creating frontend\\src\\components\\" + CLIColour("App.tjsx ", "teal") + "template ",
        after=CLIColour("[DONE]\n", "green"),
    )

# Database
cmdCLI(
    sysCmdWheel,
    pythonpath + "manage.py makemigrations --verbosity 0 > nul",
    verbose=options["verbose"],
    before="Creating database script ",
    after=CLIColour("[DONE]\n", "green"),
    wheel=options["verbose"],
)
cmdCLI(
    sysCmdWheel,
    pythonpath + "manage.py migrate --verbosity 0 > nul",
    verbose=options["verbose"],
    before="Creating database ",
    after=CLIColour("[DONE]\n", "green"),
    wheel=options["verbose"],
)

sysWrite(CLIColour("\n Project " + projName + " Created\n", "green"))
