FROM shilajitgr/csv_manager:standalone
WORKDIR /app
RUN rm -rf ./*
COPY csv_manager/ ./
COPY setup.py ./
