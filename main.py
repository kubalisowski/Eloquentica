from config import *
from models import *
from routes import *
from forms import *

app.config.from_object(Config)


if __name__ == '__main__':
    app.run()