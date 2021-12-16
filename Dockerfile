FROM ubuntu



# Update the repository sources list
RUN apt-get update

# Install and run apache
RUN apt-get install -y apache2 && apt-get clean

#ENTRYPOINT ["/usr/sbin/apache2", "-k", "start"]


#ENV APACHE_RUN_USER www-data
#ENV APACHE_RUN_GROUP www-data
#ENV APACHE_LOG_DIR /var/log/apache2


CMD service apache2 start
COPY index.html /var/www/html
EXPOSE 31001
CMD ["apache2ctl", "-D", "FOREGROUND"]
