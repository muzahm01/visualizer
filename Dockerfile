# Use an official Python 3.12 slim image as the base.
FROM python:3.12-slim

# Set the working directory in the container.
WORKDIR /app

# Copy the project files.
COPY pyproject.toml README.md ./
COPY visualizer/ ./visualizer/

# Install build dependencies and your package.
RUN pip install --upgrade pip && pip install -e .

# Expose the port that Streamlit uses.
EXPOSE 8501

# Run the Streamlit app.
CMD ["streamlit", "run", "visualizer/app.py", "--server.enableCORS", "false"]
