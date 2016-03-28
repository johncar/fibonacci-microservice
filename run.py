from app import app
from app import conf
from app.worker import WorkerProcess
from socket import error as socket_error

if __name__ == '__main__':

    try:
        WorkerProcess.start_celery()
        app.run(host=conf.SERVER_NAME, port=conf.SERVER_PORT, debug=conf.DEBUG)

    except socket_error, msg:
        print "Caught exception socket.error : %s" % msg

    finally:
        WorkerProcess.stop_celery()
