FROM nginx
RUN chmod -R 775 /usr/share/nginx/html/
COPY ./a.html /usr/share/nginx/html/
EXPOSE 80

