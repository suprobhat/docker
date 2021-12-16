FROM ubuntu

# File Author / Maintainer
MAINTAINER rmuktader

# Update the repository sources list
RUN apt-get update

# Install and run apache
RUN apt-get install -y apache2 && apt-get clean
COPY index.html /var/www/html
EXPOSE 80
CMD apachectl -D FOREGROUND

CMD ["apache2ctl", "-D", "FOREGROUND"]
