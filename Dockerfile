# Use the official Nginx image as the base image
FROM nginx:latest

# Copy your custom Nginx configuration file (if needed)
COPY nginx.conf /etc/nginx/nginx.conf

# Optionally, copy your website files into the container
COPY ./water_balance /usr/share/nginx/html

# Expose port 80 to the outside world
EXPOSE 80

# Start Nginx when the container runs
CMD ["nginx", "-g", "daemon off;"]
