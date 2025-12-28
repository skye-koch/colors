The main goal of this project is to get an arbitrarily large amount of data into my AWS account so I can get some practice processing it and moving it around. 

This function automatically triggered when I upload an image file to my input bucket.

This lambda:
  - Gets an image from an s3 bucket
  - Extracts each unique RGB value and the number of times it occurs
  - Writes to a CSV file
  - Uploads the file to another s3 bucket

Performance considerations:
  - Packaged for an ARM-based architecture to take advantage of [AWS Graviton performance and cost benefits](https://aws.amazon.com/blogs/apn/comparing-aws-lambda-arm-vs-x86-performance-cost-and-analysis-2/)
  - Images can potentially be very large, and this function uses a lot of RAM. I increased the configured memory from 128MB to 1024MB to allow for more in-memory processing. This decreased average execution time and billing duration by about half.
  - Using itertools.batched() dramatically reduced my CSV file creation time

Cost:
  - Testing data:
      - 40 images with an average size of 2MB
      - Lambda configured with 1024MB of memory and 512MB of ephemeral storage
      - Average billed duration of 800ms
  - According to the [AWS pricing calculator](https://calculator.aws/#/createCalculator/Lambda), I could invoke this function 500k/month and remain on the lambda free tier. 

