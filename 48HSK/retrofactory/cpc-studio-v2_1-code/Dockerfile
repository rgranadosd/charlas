FROM python:3.12-slim

# sdcc   — Z80 C compiler used by CPCtelera's Makefile
# g++    — needed to compile iDSK and hex2bin from source
# make   — build system for both CPCtelera projects and the tools themselves
RUN apt-get update && apt-get install -y --no-install-recommends \
        sdcc \
        g++ \
        make \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first — separate layer so it's only rebuilt when
# requirements.txt changes, not on every code change.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Compile iDSK and hex2bin for Linux.
# The repo ships macOS (Mach-O) binaries in the bin/ directories; they must be
# replaced with Linux binaries compiled from the source already in the repo.
RUN make -C cpctelera/cpctelera/tools/iDSK-0.13 \
 && make -C cpctelera/cpctelera/tools/hex2bin-2.0

# Replace the macOS sdcc bundle with symlinks to the apt-installed sdcc.
# CPCtelera's global_paths.mk hardcodes this directory; symlinking avoids
# modifying any Makefile while still pointing at the correct Linux binaries.
RUN cd cpctelera/cpctelera/tools/sdcc-3.6.8-r9946/bin \
 && rm -f * \
 && for t in sdcc sdasz80 sdar sdcpp sdld sdldz80; do \
        p="$(which "$t" 2>/dev/null)"; \
        [ -n "$p" ] && ln -s "$p" "$t"; \
    done

# Ensure the outputs directory exists so the pipeline can write to it at runtime
RUN mkdir -p scene_agent/outputs \
 && useradd -m -u 1000 appuser \
 && chown -R appuser:appuser /app
USER appuser

ENV CPCT_PATH=/app/cpctelera/cpctelera

EXPOSE 8000

CMD ["python", "main.py"]
