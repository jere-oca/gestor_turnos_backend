FROM node:18-alpine

WORKDIR /app/frontend

# Copia los archivos package.json desde la subcarpeta
COPY package*.json ./

# Install dependencies
RUN npm install

# Copia el resto de la app
COPY . .

# Set environment variables
ENV PORT=3000
ENV HOST=0.0.0.0

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]