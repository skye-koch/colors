The main goal of this project is to get an arbitrarily large amount of data into my AWS account so that I can get some practice processing it and moving it.

This lambda function:
  -Gets an image from an s3 bucket
  -Extracts each unique RGB value and the number of times it occurs
  -Writes  to a CSV file
  -Uploads the file to another s3 bucket
