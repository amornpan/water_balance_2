FROM nginx:latest

# Copy your custom Nginx configuration file (if needed)
COPY ./water_balance/nginx.conf /etc/nginx/nginx.conf

# Optionally, copy your website files into the container
COPY ./water_balance /usr/share/nginx/html

# Expose port 7890 to the outside world
EXPOSE 7890

# Start Nginx when the container runs
CMD ["nginx", "-g", "daemon off;"]

#docker build -t amornpan/nginx_service:nginx_container .
#docker push amornpan/nginx_service:nginx_container
