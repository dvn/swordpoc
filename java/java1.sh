#!/bin/sh
curl -s -H "X-On-Behalf-Of: obo" http://sword:sword@localhost:8080/swordpoc/servicedocument \
| xmllint --format -
