#!/bin/sh
curl --insecure -s -H "X-On-Behalf-Of: obo" --http1.0 --data-binary "@example.zip" -H "Content-Disposition: filename=example.zip" -H "Content-Type: application/zip" https://sword:sword@localhost:8181/swordpoc/collection/a4f21cdc-f20c-4c82-b63e-5df81f809417 \
| xmllint --format -
