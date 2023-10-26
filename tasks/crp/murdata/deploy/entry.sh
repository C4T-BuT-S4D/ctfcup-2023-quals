#!/bin/bash

chown -R www-data:www-data /userdata
php /var/www/html/register_admin.php && rm /var/www/html/register_admin.php && apache2-foreground