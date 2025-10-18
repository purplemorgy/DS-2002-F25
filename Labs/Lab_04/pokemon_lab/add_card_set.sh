#!/bin/bash
read -p "Enter TCG Card Set ID:" SET_ID

if [ -z "$SET_ID" ]; then
    echo "Error: Set ID cannot be empty." >&2
    exit 1
fi

echo "Fetching card data from $SET_ID..."
curl -o card_set_lookup/$SET_ID.json "https://api.pokemontcg.io/v2/cards?set.id=$SET_ID"