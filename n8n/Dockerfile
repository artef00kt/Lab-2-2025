FROM docker.n8n.io/n8nio/n8n:latest

USER root

# Install ffmpeg only (it works fine on Alpine)
RUN apk add --no-cache ffmpeg

USER node
