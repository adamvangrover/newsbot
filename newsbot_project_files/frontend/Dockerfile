# Stage 1: Build the React application
FROM node:18-alpine AS build

WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock)
COPY package.json ./
# If you have a lock file, copy it too for reproducible builds
# COPY package-lock.json ./
# COPY yarn.lock ./

# Install dependencies
# If using npm:
RUN npm install
# If using yarn:
# RUN yarn install --frozen-lockfile

# Copy the rest of the application source code
COPY . .

# Build the application for production
# The build script is usually defined in package.json ("build": "tsc && vite build")
RUN npm run build
# If using yarn:
# RUN yarn build

# Stage 2: Serve the built application using a lightweight web server (Nginx)
FROM nginx:1.25-alpine AS production

# Set working directory for Nginx
WORKDIR /usr/share/nginx/html

# Remove default Nginx static assets
RUN rm -rf ./*

# Copy static assets from the build stage
COPY --from=build /app/dist ./
# The /app/dist path depends on your Vite build output directory (vite.config.ts, build.outDir)
# Default for Vite is 'dist' in the project root.

# (Optional) Copy a custom Nginx configuration if needed
# For a Single Page Application (SPA), you often need to configure Nginx
# to redirect all non-asset requests to index.html.
# COPY nginx.conf /etc/nginx/conf.d/default.conf
# Create a basic nginx.conf for SPA routing:
COPY /nginx.conf /etc/nginx/nginx.conf


# Expose port 80 for Nginx
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
