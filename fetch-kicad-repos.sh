mkdir -p kicad-repos/
PAGE=1
curl -H 'Accept: application/vnd.github.preview.text-match+json' https://api.github.com/search/repositories\?q\=language:KiCad+Schematic\&order\=desc > kicad-repos/page-$PAGE.json

cat kicad-repos/page-$PAGE.json | jq '.items[].html_url' -r > kicad-repos/repos.txt
TOTAL_COUNT=$(cat kicad-repos/page-$PAGE.json | jq '.total_count')
COUNT=$(cat kicad-repos/page-$PAGE.json | jq '.items | length')
while [[ "$COUNT" -lt "$TOTAL_COUNT" ]]; do
    PAGE=$(echo "$PAGE + 1" | bc)
    echo "Fetching page #$PAGE ($COUNT/$TOTAL_COUNT)..."
    curl -H 'Accept: application/vnd.github.preview.text-match+json' https://api.github.com/search/repositories\?q\=language:KiCad+Schematic\&order\=desc\&page=$PAGE > kicad-repos/page-$PAGE.json
    COUNT=$(echo "$COUNT + $(cat kicad-repos/page-$PAGE.json | jq '.items | length')" | bc)
    cat kicad-repos/page-$PAGE.json | jq '.items[].html_url' -r >> kicad-repos/repos.txt
    sleep 5
done
