MAX_RETRIES=10
RETRY_DELAY=5  # seconds

for pdf in *.pdf; do
    svg="${pdf%.pdf}.svg"
    # Only convert if PDF is newer than SVG or SVG does not exist
    if [[ ! -e "$svg" || "$pdf" -nt "$svg" ]]; then
        for ((i=1; i<=MAX_RETRIES; i++)); do
            if lsof "$pdf" >/dev/null 2>&1; then
                echo "$pdf is busy. Retry $i/$MAX_RETRIES in $RETRY_DELAY seconds..."
                sleep $RETRY_DELAY
            else
                /opt/homebrew/bin/pdf2svg "$pdf" "$svg"
                break
            fi
            if [ $i -eq $MAX_RETRIES ]; then
                echo "Failed to process $pdf after $MAX_RETRIES retries."
            fi
        done
    fi
done