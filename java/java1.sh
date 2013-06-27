#!/bin/sh
curl --insecure -s -H "X-On-Behalf-Of: obo" https://sword:sword@localhost:8181/swordpoc/servicedocument \
| xmllint --format -
