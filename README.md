# Running a bokeh server with Binder

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/cnicolas662/Bokeh_Binder/master?urlpath=%2Fproxy%2F5006%2Fbokeh-app)


This repository demonstrates how to run a Bokeh server from within Binder. To do so, we did the following things:

1. Created a `bokeh-app` directory in the repo with a `main.py` file in it. This is the application that will be served. 
2. Installed `bokeh` for the viz and `jupyter_server_proxy` which we'll use to direct people to the port on which Bokeh runs. See `environment.yml`.
3. Added a custom server extension (`bokehserverextension.py`) that will be run to direct people to the Bokeh app (which is run on a port)
4. Used `postBuild` to enable the `jupyter_server_proxy` extension, then set up and enable our custom server extension for Bokeh. 
5. Created a Binder link that uses `urlpath` to point users to the port on which the Bokeh server will run:

   ```
   https://mybinder.org/v2/gh/cnicolas662/Bokeh_Binder/master?urlpath=%2Fproxy%2F5006%2Fbokeh-app

   ```
   
When people click on the Binder link, they should be directed to the running Bokeh app.
