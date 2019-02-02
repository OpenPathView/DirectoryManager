FROM python

ENV OPV_DM_PATH /mnt/dm
ENV OPV_DM_PORT 5000
ENV OPV_DM_FTP_PORT 2121
ENV OPV_DM_HTTP_PORT 5050

COPY . /source/DirectoryManager

WORKDIR /source/DirectoryManager

RUN pip3 install -r requirements.txt && \
python3 setup.py install

EXPOSE ${OPV_DM_PORT}:${OPV_DM_PORT}
EXPOSE ${OPV_DM_FTP_PORT}:${OPV_DM_FTP_PORT}
EXPOSE ${OPV_DM_HTTP_PORT}:${OPV_DM_HTTP_PORT}

CMD ["/usr/local/bin/opv_dm_web.py"]
