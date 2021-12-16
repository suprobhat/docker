FROM nginx
EXPOSE 31001
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY / /usr/share/nginx/html
