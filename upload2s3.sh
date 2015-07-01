#!/usr/bin/env bash
BOX_FILE_PATH=$1
S3_BUCKET=ourvagrantboxes
aws s3 cp ${BOX_FILE_PATH} s3://${S3_BUCKET}/ --grants read=uri=http://acs.amazonaws.com/groups/global/AllUsers

