# Use official slim Python image — smaller attack surface than full image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Create a dedicated non-root user — containers should NEVER run as root
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy dependencies list first — Docker caches this layer
# so rebuilds are faster when only code changes
COPY requirements.txt .

# Install dependencies without caching — keeps image smaller
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the application files needed
COPY app.py .
COPY secure_headers.py .
COPY monitor.py .

# Transfer ownership of all files to the non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user before running anything
USER appuser

# Tell Docker which port the app listens on
EXPOSE 5000

# Health check — Docker restarts container if this fails 3 times
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/api/public')" || exit 1

# Run the application
CMD ["python3", "app.py"]
