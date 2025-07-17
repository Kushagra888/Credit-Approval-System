#!/bin/bash
# Use this script to test if a given TCP host/port is available

CLIENT_TIMEOUT=${CLIENT_TIMEOUT:-15}
CLIENT_INTERVAL=${CLIENT_INTERVAL:-1}

# Process arguments
while [[ $# -gt 0 ]]
do
  key="$1"
  case $key in
    -h|--help)
      echo "Usage: wait-for-it.sh host:port [-- command args]"
      echo "  -h, --help    Show this help message"
      exit 0
      ;;
    *:* )
      hostport=(${1//:/ })
      HOST=${hostport[0]}
      PORT=${hostport[1]}
      shift
      ;;
    -- )
      shift
      CLI="$@"
      break
      ;;
    * )
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
done

if [[ -z "$HOST" || -z "$PORT" ]]; then
  echo "Error: you need to provide a host and port to test."
  exit 1
fi

echo "Waiting for $HOST:$PORT..."

start_ts=$(date +%s)
while :
 do
  (echo > /dev/tcp/$HOST/$PORT) >/dev/null 2>&1
  result=$?
  if [[ $result -eq 0 ]]; then
    end_ts=$(date +%s)
    echo "$HOST:$PORT is available after $((end_ts - start_ts)) seconds"
    break
  fi
  sleep $CLIENT_INTERVAL
  now_ts=$(date +%s)
  if [[ $((now_ts - start_ts)) -gt $CLIENT_TIMEOUT ]]; then
    echo "Timeout after $CLIENT_TIMEOUT seconds waiting for $HOST:$PORT"
    exit 1
  fi
done

if [[ -n $CLI ]]; then
  echo "Running command: $CLI"
  exec $CLI
fi