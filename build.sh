#!/bin/bash

docker build -t zjorsie/p4mn-docker:nologging .

docker login --username= # FILL IN USERNAME

docker push zjorsie/p4mn-docker:nologging