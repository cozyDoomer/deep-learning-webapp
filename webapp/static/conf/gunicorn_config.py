import multiprocessing, os

port = str(os.environ['PORT'])

bind = "0.0.0.0:" + port 
workers = multiprocessing.cpu_count() * 2 + 1