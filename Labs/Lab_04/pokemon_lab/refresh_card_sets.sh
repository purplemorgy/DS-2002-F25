#!/bin/bash
echo "Refreshing all card sets in card_set_lookup..."
for FILE in card_set_lookup/*.json; do
    SET_ID=$(basename "$FILE" .json)
    echo "Updating $SET_ID.json..."
    curl -o card_set_lookup/$SET_ID "https://api.pokemontcg.io/v2/cards?set.id=$SET_ID"
    echo "$SET_ID.json updated."
done
echo "All card sets refreshed."