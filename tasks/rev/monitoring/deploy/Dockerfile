FROM denoland/deno:ubuntu-1.37.2

RUN echo "nobody:x:1000:1000:::" > /etc/passwd
RUN echo "nobody::1000:nobody" > /etc/group

COPY monitoring /monitoring
RUN mkdir /entries

RUN chown -R nobody:nobody /monitoring /entries
RUN chmod 600 /entries
RUN chmod 500 /monitoring

USER nobody

ENTRYPOINT [ "/monitoring" ]
