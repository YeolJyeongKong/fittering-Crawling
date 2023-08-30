#!/bin/bash
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 210651441624.dkr.ecr.ap-northeast-2.amazonaws.com
docker build -t 210651441624.dkr.ecr.ap-northeast-2.amazonaws.com/product-length:latest .
docker push 210651441624.dkr.ecr.ap-northeast-2.amazonaws.com/product-length:latest
aws lambda update-function-code --function-name product-length-func --image-uri 210651441624.dkr.ecr.ap-northeast-2.amazonaws.com/product-length:latest