# Stage 1: Build
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install --frozen-lockfile

# Copy application files
COPY . .

# Set production environment
ENV NODE_ENV=production
ENV NEXT_PUBLIC_API_URL=http://127.0.0.1:5000

# Build the application
RUN npm run build

# Stage 2: Production
FROM node:18-alpine AS runner

# Set working directory
WORKDIR /app

# Install production dependencies
COPY --from=builder /app/package*.json ./
RUN npm install --only=production --frozen-lockfile

# Copy built application
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/next.config.js ./next.config.js

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000
ENV NEXT_PUBLIC_API_URL=http://127.0.0.1:5000

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "start"] 