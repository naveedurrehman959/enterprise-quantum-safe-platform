FROM node:22-alpine AS build

LABEL org.opencontainers.image.source="https://github.com/naveedurrehman959/enterprise-quantum-safe-platform"

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

ARG VITE_API_URL=/api/v1
ENV VITE_API_URL=$VITE_API_URL

RUN npm run build


FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

COPY nginx-main.conf /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

RUN mkdir -p \
        /tmp/client_temp \
        /tmp/proxy_temp \
        /tmp/fastcgi_temp \
        /tmp/uwsgi_temp \
        /tmp/scgi_temp \
    && chown -R nginx:nginx \
        /tmp/client_temp \
        /tmp/proxy_temp \
        /tmp/fastcgi_temp \
        /tmp/uwsgi_temp \
        /tmp/scgi_temp \
        /usr/share/nginx/html \
        /etc/nginx/conf.d

EXPOSE 80

USER nginx

CMD ["nginx", "-g", "daemon off;"]
