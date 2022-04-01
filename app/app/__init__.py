from flask import Flask, request, jsonify, render_template, redirect
from app.utils import Code, PatchStd

app = Flask(__name__)


def get_output(src: str, name: str) -> str:
    """
    Get output of a code snippet.
    :param str src: Code snippet.
    :param str name: Name of the module.
    :return: Output of the code snippet.
    :rtype: str
    """
    out = ""
    with PatchStd() as std:
        module = Code(name, src)
        module.run.r_lambda(*module.run.r_args, **module.run.r_kwargs)
        out = std.out.getvalue()

    return out


@app.route('/', methods=['GET', 'POST'])
def index():
    src = request.args.get('src')
    out = request.args.get('out')

    return render_template('index.html', source=src, output=out)


@app.route('/run', methods=['POST'])
def run():
    out = ""
    src = request.json['code']
    name = request.json['name']

    with PatchStd() as std:
        code = Code(name, request.json['code'])
        code.run.r_lambda(*code.run.r_args, **code.run.r_kwargs)
        out = std.out.getvalue()

    return jsonify({"output": out})


if __name__ == '__main__':
    app.run(debug=True)