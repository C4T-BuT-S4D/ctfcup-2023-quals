FROM php:8.1-apache

RUN pecl install redis \
&& docker-php-ext-enable redis

COPY entry.sh /entry.sh
COPY src/ /var/www/html/

WORKDIR /var/www/html

CMD ["/entry.sh"]
