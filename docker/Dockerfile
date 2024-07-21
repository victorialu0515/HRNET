FROM public.ecr.aws/lambda/python:3.11

WORKDIR ${LAMBDA_TASK_ROOT}

# Install requirements
COPY docker/requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy stuff
COPY HRNET ${LAMBDA_TASK_ROOT}/HRNET
COPY models ${LAMBDA_TASK_ROOT}/models
COPY *.py ${LAMBDA_TASK_ROOT}

# Set
CMD [ "app.lambda_handler" ]
