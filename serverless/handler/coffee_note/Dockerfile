FROM public.ecr.aws/lambda/python:3.8
# FROM public.ecr.aws/lambda/python:3.8-arm64
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY *.py ./

CMD [ "coffee_note.coffee_note_handler" ]
