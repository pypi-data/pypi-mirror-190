""" Sensical overrides to Flask-Smorest, primarily around authentication
    and bootstrapping.
"""
try:
    from flask_smorest import Blueprint as SmorestBlueprint, Api as SmorestApi
except Exception:
    Api = None
    Blueprint = None
else:
    from flask import abort as flask_abort, jsonify, render_template,\
        make_response
    from webargs.flaskparser import FlaskParser
    from werkzeug.exceptions import HTTPException
    from werkzeug.http import HTTP_STATUS_CODES

    class Api(SmorestApi):

        def __init__(self, *args, **kwargs):
            """ Override swagger-ui template.
            """
            self._openapi_swagger_ui = self.__openapi_swagger_ui
            super().__init__(*args, **kwargs)

        # We override this funciton because we want to control how we customize
        # the swagger-ui template and title.
        def __openapi_swagger_ui(self):
            """Expose OpenAPI spec with Swagger UI"""
            return render_template(
                self._app.config.get('OPENAPI_SWAGGER_BASE_TEMPLATE',
                                     'swagger_ui.html'),
                title=self._app.config.get('OPENAPI_SWAGGER_APP_NAME',
                                           self._app.name),
                swagger_ui_url=self._swagger_ui_url,
            )

    class CustomParser(FlaskParser):
        DEFAULT_VALIDATION_STATUS = 400

        def handle_error(self, error, req, schema, error_status_code,
                         error_headers):
            """ Handles errors during parsing. Aborts the current HTTP request
                and responds with a 422 error.
            """

            # This is custom. If we have error messages, simply send them back
            if error.messages:
                msg = jsonify(error.messages)
                msg.status_code = self.DEFAULT_VALIDATION_STATUS
                return flask_abort(msg)

            # Otherwise execute the base function
            return super(CustomParser,
                         self).handle_error(error, req, schema,
                                            error_status_code, error_headers)

    class Blueprint(SmorestBlueprint):
        ARGUMENTS_PARSER = CustomParser()

    def abort(code, message=None, api_response=False):
        """ Properly abort the current request.

        Attaches `message` to response if given.

        :code int HTTP status code for abort
        :message str message Custom message to send with response
        :api_response boolean for responding to a webapp or an api
        :raise HTTPException:
        """
        try:
            if api_response:
                response = make_response(
                    jsonify({
                        "code": code,
                        "message": message,
                        "status": HTTP_STATUS_CODES[code]
                    }), code)
                flask_abort(response)
            else:
                flask_abort(code)
        except HTTPException as e:
            if message:
                e.data = {'message': str(message)}
            raise
