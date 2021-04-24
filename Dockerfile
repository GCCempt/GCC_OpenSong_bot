FROM python:3
ADD rundiscord.py /
CMD [ "python", "./rundiscord.py" ]