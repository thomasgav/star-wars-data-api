FROM nginx:1.27-alpine

# Remove default config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config
COPY ./docker/local/nginx/nginx.conf /etc/nginx/conf.d

# Create dirs for static/media and nginx cache
RUN mkdir -p /app/staticfiles /app/mediafiles /var/cache/nginx /var/run /var/log/nginx \
    && chown -R nginx:nginx /app /var/cache/nginx /var/run /var/log/nginx
