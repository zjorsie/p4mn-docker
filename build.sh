#!/bin/bash

docker build -t zjorsie/p4mn-docker:latest .

docker login --username= # FILL IN USERNAME

docker push zjorsie/p4mn-docker:latest