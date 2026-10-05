FROM node:20-alpine

LABEL maintainer="Vishwas Vashishtha"
LABEL description="Student Portal Backend API"

WORKDIR /app

# Copy package files first for better layer caching
COPY package.json ./

# Install dependencies
RUN npm install --production

# Copy application code
COPY server.js ./

# Create non-root user
RUN addgroup -S apigroup && adduser -S apiuser -G apigroup
USER apiuser

EXPOSE 3000

HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:3000/api/health || exit 1

CMD ["node", "server.js"]
