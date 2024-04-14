# Use Alpine Linux as a parent image
FROM alpine:latest

# Install Python and pip
RUN apk add --no-cache python3 py3-pip

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Run main.py when the container launches
CMD ["python3", "main.py"]