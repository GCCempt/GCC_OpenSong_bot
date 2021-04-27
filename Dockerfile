# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

# Discord Bot Tokens and keys
ENV DISCORD_TOKEN_DEV=''
ENV READCHANNELID_DEV=''
ENV POSTCHANNELID_DEV=''
ENV DROPBOX_ACCESS_TOKEN=''
ENV FTP_PASSWORD=''
ENV FTP_HOSTNAME=''
ENV FTP_USERNAME=''

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "rundiscord.py"]
