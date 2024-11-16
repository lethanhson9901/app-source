#!/bin/bash

# Create project directories
mkdir -p {logs,nginx/{conf.d,ssl},init-scripts/postgres,src/monitoring/{grafana-dashboards,grafana-datasources}}

# Create Nginx configuration
cat > nginx/conf.d/app.conf << 'EOF'
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://app:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /metrics {
        proxy_pass http://prometheus:9090;
    }

    location /grafana/ {
        proxy_pass http://grafana:3000/;
    }
}
EOF

# Create Grafana datasource configuration
cat > src/monitoring/grafana-datasources/datasources.yaml << 'EOF'
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
EOF

# Set permissions
chmod +x setup.sh
chmod -R 755 logs
chmod -R 755 nginx

# Create database initialization script
cat > init-scripts/postgres/01-init.sql << 'EOF'
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_items_name ON items(name);
EOF
