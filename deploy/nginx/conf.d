events {}

http {
    upstream backend {
        server backend:8000;
    }

    server {
        listen 80;
        server_name api.hrcounselor.ru;

        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }

        location / {
            return 301 https://$host$request_uri;
        }
    }

    server {
        listen 443 ssl;
        server_name api.hrcounselor.ru;

        ssl_certificate     /etc/letsencrypt/live/api.hrcounselor.ru/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/api.hrcounselor.ru/privkey.pem;

        location / {
            proxy_pass         http://backend;
            proxy_set_header   Host $host;
            proxy_set_header   X-Real-IP $remote_addr;
            proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header   X-Forwarded-Proto $scheme;
        }
    }
}