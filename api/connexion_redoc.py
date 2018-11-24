"""Add a route to ReDoc."""

from flask import render_template_string

REDOC_TEMPLATE = '''
<!DOCTYPE html>
<html>
  <head>
    <title>ReDoc</title>
    <!-- needed for adaptive design -->
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">

    <!--
    ReDoc doesn't change outer page styles
    -->
    <style>
      body {
        margin: 0;
        padding: 0;
      }
    </style>
  </head>
  <body>
    <redoc spec-url="{{spec_url}}"></redoc>
    <script src="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"> </script>
  </body>
</html>
'''


def redoc_view(spec_url):
    """
    Render OpenAPI specification using ReDoc.

    :param str spec_url: URL to the JSON specification file
    """
    return render_template_string(REDOC_TEMPLATE, spec_url=spec_url)


def add_redoc_route(app, spec_url):
    """
    Add a '/redoc' route pointing to de ReDoc page.

    :param FlaskAPP app: the connexion application
    :param str penapi_json_url: the URL of the OpenAPI JSON spec
    """
    app.app.add_url_rule('/redoc', 'redoc', redoc_view, defaults={'spec_url': spec_url})
