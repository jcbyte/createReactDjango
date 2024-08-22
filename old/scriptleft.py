import os
from threading import Event, Thread
from time import sleep

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
