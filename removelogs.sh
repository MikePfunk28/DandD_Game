#!/bin/bash

export MSYS_NO_PATHCONV=1

log_groups=(
  "/aws/lambda/amplify-d10355pa75rc5y-ma-AmplifyBranchLinkerCusto-ZAFZtYyo1YUF"
  "/aws/lambda/amplify-d10355pa75rc5y-ma-CustomCDKBucketDeploymen-hFtmDI74g4IY"
  "/aws/lambda/amplify-d10355pa75rc5y-ma-CustomS3AutoDeleteObject-WDh3npb3Rh6w"
  "/aws/lambda/amplify-d10355pa75rc5y-ma-TableManagerCustomProvid-7aTu4OevKUvp"
  "/aws/lambda/amplify-d10355pa75rc5y-ma-TableManagerCustomProvid-v0qQY7JOG4EE"
  "/aws/vendedlogs/bedrock/knowledge-base/APPLICATION_LOGS/EJB4VJ1CBP"
)

for log_group in "${log_groups[@]}"; do
  /c/Program\ Files/Amazon/AWSCLIV2/aws logs put-retention-policy --log-group-name "$log_group" --retention-in-days 1
done
