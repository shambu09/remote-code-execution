from flask import Flask, request, render_template
from utils import Code, PatchStd

app = Flask(__name__)


def get_output(src: str, name: str) -> str:
    """
    Get output of a code snippet.
    :param str src: Code snippet.
    :param str name: Name of the module.
    :return: Output of the code snippet.
    :rtype: str
    """
    with PatchStd() as std:
        module = Code(name, src)
        module.lib.__run()

    return std.value


@app.route('/', methods=['GET', 'POST'])
def index() -> None:
    if request.method == 'POST':
        print(request.form)
        src = request.form['src']
        name = "test_module"

        output = get_output(src, name)
        if output == "": output = "No output"
        return render_template('index.html', source=src, output=output)

    else:
        return render_template('index.html', source="", output="No Output")


if __name__ == '__main__':
    app.run(debug=True)