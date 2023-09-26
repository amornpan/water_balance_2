# Use the official Jupyter Notebook base image
FROM jupyter/base-notebook:latest

# Set the Jupyter Notebook password
RUN echo "c.NotebookApp.password = u'sha1:231c840cb3bc:671ee604d5739be508615daea5241a68ee74aed3'" >> ~/.jupyter/jupyter_notebook_config.py
RUN echo "c.NotebookApp.token = ''" >> ~/.jupyter/jupyter_notebook_config.py
RUN echo "c.NotebookApp.open_browser = False" >> ~/.jupyter/jupyter_notebook_config.py

# Set the working directory to /home/jovyan/work.
WORKDIR /home/jovyan/work

COPY jupyter_notebook_config.py /home/jovyan/.jupyter
COPY . /home/jovyan/work

# Add the following lines to the Dockerfile to change permissions
USER root
RUN chmod u+w /home/jovyan/work/.ipynb_checkpoints/
USER jovyan

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir pandas plotly cython geopandas pymongo

# Expose the Jupyter Notebook port
EXPOSE 8888

# Run Jupyter Notebook with the custom configuration
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--config=/etc/jupyter/system_configuration.py", "--allow-root"]
