#/home/jovyan/.jupyter
#$ cat jupyter_notebook_config.py
# sudo nano jupyter_notebook_config.py
c = get_config()
c.NotebookApp.password = u'sha1:231c840cb3bc:671ee604d5739be508615daea5241a68ee74aed3'
c.NotebookApp.token = ''
c.NotebookApp.open_browser = False
c.NotebookApp.ip = '*'
c.NotebookApp.port = 8888
c.NotebookApp.iopub_data_rate_limit = int(1e7)  # Set a higher limit (e.g., 10 MB/s)