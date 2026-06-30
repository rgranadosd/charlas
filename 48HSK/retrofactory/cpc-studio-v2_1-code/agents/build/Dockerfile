FROM python:3.12-slim

# Build deps for sdcc 3.6.8 + the DSK tools (g++/make/gcc), plus runtime.
RUN apt-get update && apt-get install -y --no-install-recommends \
        g++ gcc make file bison flex libboost-dev zlib1g-dev texinfo \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir fastapi==0.115.0 uvicorn==0.30.6 pydantic==2.9.2

# The CPCtelera SDK + project template. cpctelera/ is .gitignored (493MB), so
# this image MUST be built locally with podman, then pushed to the k3d registry.
COPY cpctelera cpctelera
COPY pruebacpct/Makefile pruebacpct/Makefile
COPY pruebacpct/cfg pruebacpct/cfg

# Build the CPCtelera DSK tools from source for the container arch (the shipped
# binaries are x86_64 Mach-O).
RUN for d in cpctelera/cpctelera/tools/2cdt cpctelera/cpctelera/tools/dskgen \
             cpctelera/cpctelera/tools/hex2bin-2.0 cpctelera/cpctelera/tools/iDSK-0.13; do \
      [ -f "$d/Makefile" ] || continue; \
      make -C "$d" clean || true; \
      find "$d" -type f -exec sh -c 'file "$1" | grep -q "Mach-O" && rm -f "$1"' _ {} \; ; \
      make -C "$d" || echo "WARN: $d"; \
    done

# Build CPCtelera's OWN sdcc 3.6.8 from source (Z80 port only) so the pipeline
# compiles with the EXACT same compiler/standard (C89) as the real toolchain,
# instead of Debian's permissive sdcc 4.x. The shipped sdcc binary is x86_64
# Mach-O and cannot run on this arm64 Linux node.
RUN cd cpctelera/cpctelera/tools/sdcc-3.6.8-r9946/src \
    && find . -type f -name 'sdcc' -path '*/bin/*' -delete 2>/dev/null || true \
    && ./configure \
         --disable-mcs51-port --disable-z180-port --disable-r2k-port \
         --disable-r2ka-port --disable-r3ka-port --disable-gbz80-port \
         --disable-tlcs90-port --disable-ds390-port --disable-ds400-port \
         --disable-pic14-port --disable-pic16-port --disable-hc08-port \
         --disable-s08-port --disable-stm8-port --disable-pdk13-port \
         --disable-pdk14-port --disable-pdk15-port --disable-ucsim \
         --disable-device-lib --disable-packihx \
    && make -j"$(nproc)" MAKEINFO=true \
    && cp bin/sdcc bin/sdcpp bin/sdasz80 bin/sdld bin/sdar bin/sdldz80 ../bin/ \
    && ../bin/sdcc --version

COPY agents/build/main.py main.py

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

ENV CPCT_PATH=/app/cpctelera/cpctelera
ENV CPC_TEMPLATE=/app/pruebacpct

EXPOSE 8000
CMD ["python", "main.py"]
