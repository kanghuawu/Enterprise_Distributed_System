FROM python:2.7.13
MAINTAINER Your Name "kang-hua.wu@sjsu.edu"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python","app.py"]
# following command will be replace with new argument
CMD ["https://github.com/kanghuawu/my-test-repo.git"]