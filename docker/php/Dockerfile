FROM php:7.2-fpm

WORKDIR /var/www/html

RUN apt-get update && apt-get install -y \
        libzip-dev \
        libc-client-dev \
        libkrb5-dev \
        libwebp-dev \
        zip \
        libfreetype6-dev \
        libjpeg62-turbo-dev \
        libpng-dev \
        libicu-dev \
        zlib1g-dev \
        ffmpeg \
        libmemcached11 \
        libmemcachedutil2 \
        build-essential \
        libmemcached-dev \
        gnupg2 \
        libpq-dev \
        libpq5

RUN docker-php-ext-configure gd --with-webp-dir=/usr/include/ --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/
RUN docker-php-ext-configure intl
RUN docker-php-ext-configure zip

RUN docker-php-ext-install pdo_mysql zip exif pcntl gd intl fileinfo

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN groupadd -g 1000 www
RUN useradd -u 1000 -ms /bin/bash -g www www

COPY . /var/www/html
COPY --chown=www:www . /var/www/html

USER www

CMD ["php-fpm"]