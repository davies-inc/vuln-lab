FROM node:24.6.0
WORKDIR /app

# copy the whole JS app so we can install & run it
COPY vuln-js ./vuln-js
RUN cd vuln-js && npm install

EXPOSE 3000
CMD ["node", "vuln-js/index.js"]