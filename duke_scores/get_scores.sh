#!/bin/bash

sports=(baseball mens-basketball womens-basketball football mens-lacrosse womens-lacrosse mens-soccer womens-soccer mens-tennis womens-tennis)

function get_scores {
    url="https://goduke.com/sports/$1/schedule"

    if [ $1 == "football" ]; then
        url="https://goduke.com/sports/football/schedule/2023"
    fi

    wget -q -O- $url > temp.txt

    grep -o -E "<span>[0-9]+-[0-9]+</span>" temp.txt | sed -E "s/<span>|<\/span>//g" > scores.txt
    sed -n -E '/<div class="sidearm-schedule-game-opponent-name">/,/<\/div>/p' temp.txt | grep 'target="_blank">' | sed -E 's/.*>(.*)<\/a>/\1/'> opponents.txt
    sed -n -E '/<div class="sidearm-schedule-game-opponent-logo noprint">/,/<\/div>/p' temp.txt | grep 'data-src' | sed -E 's/.*src="(.*)".*/\1/' | sed 's/".*//' > logos.txt
    
    rm temp.txt
    
    sleep 1 # Let's not get banned
}

rm -rf data data.json

for sport in ${sports[@]}; do
    mkdir -p data/$sport
    cd data/$sport
    get_scores $sport
    cd ../..
done

python3 json_format.py

rm -rf data

echo "Congrats, you have committed an ethical violation"