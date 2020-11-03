#!/bin/bash

# Print Helm template.
helm template cam cam --set elasticsearch.username=reader --set elasticsearch.password=reader

# Install Helm chart.
helm install cam cam --set elasticsearch.username=reader --set elasticsearch.password=reader
