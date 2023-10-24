FROM busybox:1.36.1

RUN echo "nobody:x:1337:1337:::" >> /etc/passwd
RUN echo "nobody::1337:nobody" >> /etc/group

WORKDIR /static

COPY . .
RUN chown -R nobody:nobody /static

USER nobody

CMD ["busybox", "httpd", "-f", "-v", "-p", "8080"]
