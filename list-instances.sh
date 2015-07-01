#!/usr/bin/env bash

regions=(
  eu-central-1
  sa-east-1
  ap-northeast-1
  eu-west-1
  us-east-1
  us-west-1
  us-west-2
  ap-southeast-2
  ap-southeast-1
  )

for region_code in ${regions[@]}; do
  echo $region_code
  aws ec2 describe-instances --region $region_code
done
