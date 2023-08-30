#!/bin/bash
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 210651441624.dkr.ecr.ap-northeast-2.amazonaws.com
docker buildx build -t 210651441624.dkr.ecr.ap-northeast-2.amazonaws.com/product-range:latest .
docker push 210651441624.dkr.ecr.ap-northeast-2.amazonaws.com/product-range:latest 
aws lambda update-function-code --function-name product-range-func --image-uri 210651441624.dkr.ecr.ap-northeast-2.amazonaws.com/product-range:latest