#!/bin/bash

EMAIL="auto-test@example.com"
POST_RESPONSE=$(curl -s -X POST http://localhost:5000/api/timeline_post \
  -d "name=Test" \
  -d "email=$EMAIL" \
  -d "content=Test post")

POST_ID=$(echo $POST_RESPONSE | grep -o '"id":[0-9]*' | cut -d ':' -f2)
echo "Created post with ID $POST_ID"

echo "Getting all timeline posts:"
curl -s http://localhost:5000/api/timeline_post

echo "Deleting post $POST_ID"
curl -s -X DELETE http://localhost:5000/api/timeline_post/$POST_ID