

from flask import Flask
from kernels import webKernel


from kernels import MainLoop
# import kernels.Logger as Logger
# import kernels.GlobalInfo as GlobalInfo


app = Flask(__name__, template_folder='adapters/web_view')
app.register_blueprint(webKernel.main)




if __name__ == '__main__':
    MainLoop.MainLooper()
    app.run( port=8080, debug=True)





