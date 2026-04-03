#!/bin/bash
# Serve the game over HTTP so fetch() can load strategy CSV and sound files (file:// does not).
cd "$(dirname "$0")"
PORT=8090
URL="http://127.0.0.1:$PORT/blackjack.html"

if ! lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  nohup python3 serve.py >/dev/null 2>&1 &
  disown
  sleep 1
fi

open "$URL"
