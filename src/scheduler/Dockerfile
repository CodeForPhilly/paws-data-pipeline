FROM alpine:3.6

# copy crontabs for root user
COPY cronfile /etc/crontabs/root
RUN apk --no-cache add curl

# start crond with log level 8 in foreground, output to stderr
CMD ["crond", "-f", "-d", "8"]