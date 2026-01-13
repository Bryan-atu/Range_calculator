FROM ubuntu:24.04
RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y --no-install-recommends ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --chmod=0755 range_test /app/range_test
RUN useradd -m appuser
USER appuser
ENTRYPOINT ["/app/range_test"]
