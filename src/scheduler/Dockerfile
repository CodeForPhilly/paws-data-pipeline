FROM alpine:latest
RUN apk add --no-cache curl bash jq

COPY  --chmod=755 trigger.sh /usr/src/trigger.sh

CMD ["/usr/src/trigger.sh"]