#!/bin/bash

# Deploy the Cloud Function
gcloud functions deploy newsletter-sender \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=send_newsletter \
  --trigger-topic=news-newsletter \
  --env-vars-file=.env.yaml \
  --memory=256MB \
  --timeout=60s 