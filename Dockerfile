FROM ubuntu:24.04
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates \
 && apt-get purge -y --auto-remove gpgv \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --chmod=0755 range_test /app/range_test
RUN useradd -m appuser
USER appuser
ENTRYPOINT ["/app/range_test"]
