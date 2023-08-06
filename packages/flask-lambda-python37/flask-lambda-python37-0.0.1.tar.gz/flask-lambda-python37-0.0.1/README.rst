flask-lambda-python37
============================================================

**Python 3.7+ Only**
------------------------------------------------------------

For older versions of python use the original flask-lambda library which this code is adapted from:
https://github.com/sivel/flask-lambda

See this example flask project for how to use and deploy a flask app using this library:
https://github.com/techjacker/flask-lambda-example


Installation
------------

pip install flask-lambda-python37


Usage
-----

Here is an example of what ``my_python_file.py`` would look like::

    from flask_lambda import FlaskLambda

    app = FlaskLambda(__name__)


    @app.route('/foo', methods=['GET', 'POST'])
    def foo():
        data = {
            'form': request.form.copy(),
            'args': request.args.copy(),
            'json': request.json
        }
        return (
            json.dumps(data, indent=4, sort_keys=True),
            200,
            {'Content-Type': 'application/json'}
        )


    if __name__ == '__main__':
        app.run(debug=True)
