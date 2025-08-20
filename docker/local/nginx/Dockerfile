FROM nginx:1.27-alpine

# Remove default config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom config
COPY nginx.conf /etc/nginx/conf.d

# Create dirs for static/media
RUN mkdir -p /app/staticfiles /app/mediafiles \
    && chown -R nginx:nginx /app

USER nginx
