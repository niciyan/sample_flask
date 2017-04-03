from flask import Flask, render_template
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/')
def main():
    current_time = datetime.utcnow()
    # import pdb; pdb.set_trace()
    return render_template('date.html', current_time=current_time)

if __name__ == '__main__':
    app.run(debug=True)
