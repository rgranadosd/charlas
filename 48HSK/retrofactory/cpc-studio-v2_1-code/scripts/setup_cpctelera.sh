#!/usr/bin/env bash
set -e

PROJECT_ROOT="/Users/rafagranados/Develop/charlas/48HSK/retrofactory/cpc-studio-v2_1-code"
CPCT_ROOT="$PROJECT_ROOT/tools/cpctelera"

echo "Cleaning stale build artifacts..."
find "$CPCT_ROOT/cpctelera/tools" \( -name "*.o" -o -name "*.lo" -o -name "*.la" -o -name "*.a" \) -delete 2>/dev/null || true
find "$CPCT_ROOT/cpctelera/tools/sdcc-3.6.8-r9946/obj" \( -name "*.o" -o -name "*.lo" -o -name "*.la" -o -name "*.a" \) -delete 2>/dev/null || true

cd "$CPCT_ROOT"

CPPFLAGS="-I/opt/homebrew/include -I/opt/homebrew/opt/boost/include -I/opt/homebrew/opt/freeimage/include" \
CXXFLAGS="-I/opt/homebrew/include -I/opt/homebrew/opt/boost/include -I/opt/homebrew/opt/freeimage/include" \
CFLAGS="-I/opt/homebrew/include" \
CPATH="/opt/homebrew/include:/opt/homebrew/opt/boost/include:/opt/homebrew/opt/freeimage/include" \
CPLUS_INCLUDE_PATH="/opt/homebrew/include:/opt/homebrew/opt/boost/include:/opt/homebrew/opt/freeimage/include" \
LDFLAGS="-L/opt/homebrew/lib -L/opt/homebrew/opt/boost/lib -L/opt/homebrew/opt/freeimage/lib" \
./setup.sh --skip-examples
