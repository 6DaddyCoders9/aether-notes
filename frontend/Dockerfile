# Step 1: Build the React app
FROM node:20-alpine AS build
WORKDIR /app

# Copy only package files first (better caching)
COPY package*.json ./
RUN npm install

# Now copy rest of the code
COPY . .
RUN npm run build

# Step 2: Serve with Nginx
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
