FROM python:alpine

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the Django project files to the container
COPY . /app/

# Grant execute permissions to the entrypoint script
RUN chmod +x /app/entrypoint.sh

# Start the development server using the custom entrypoint script
ENTRYPOINT ["sh"] 
CMD ["/app/entrypoint.sh"]


