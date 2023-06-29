# Base image
FROM python:3.9

# Set working directory
WORKDIR /sharuk

# Install updates
RUN apt-get update && apt-get install -y tk

RUN pip install --upgrade pip
# Clone the repository
RUN git clone https://github.com/Jayakumar-dev/sharuk.git .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Streamlit runs on
EXPOSE 8501

# Set the command to run your Streamlit app
CMD ["streamlit", "run", "--server.port", "8501", "mainPage.py"]
