import argparse

def main():
        
    parser = argparse.ArgumentParser(description='Parse config to use in SAM CLI deploy')
    parser.add_argument('--env', type=str, choices=['dev', 'test', 'preprod', 'prod'], required=True, help='What environment do you want to build config for?')
    parser.add_argument('--stack-name', type=str, required=True, help="The name of the AWS CloudFormation stack that you're deploying to. If you specify an existing stack, the command updates the stack. If you specify a new stack, the command creates it.")
    parser.add_argument('--s3-bucket', type=str, required=True, help="The name of the Amazon S3 bucket where this command uploads your AWS CloudFormation template. If your template is larger than 51,200 bytes, then either the --s3-bucket or the --resolve-s3 option is required. If you specify both the --s3-bucket and --resolve-s3 options, then an error will result.")
    parser.add_argument('--s3-prefix', type=str, required=True, help="The prefix added to the names of the artifacts that are uploaded to the Amazon S3 bucket. The prefix name is a path name (folder name) for the Amazon S3 bucket.")
    parser.add_argument('--region', type=str, required=True, help="The AWS Region to deploy to. For example, us-east-1.")
    parser.add_argument('--capabilities', type=str, required=True, help="A list of capabilities that you must specify to allow AWS CloudFormation to create certain stacks. Some stack templates might include resources that can affect permissions in your AWS account, for example, by creating new AWS Identity and Access Management (IAM) users. For those stacks, you must explicitly acknowledge their capabilities by specifying this option. The only valid values are CAPABILITY_IAM and CAPABILITY_NAMED_IAM. If you have IAM resources, you can specify either capability. If you have IAM resources with custom names, you must specify CAPABILITY_NAMED_IAM. If you don't specify this option, the operation returns an InsufficientCapabilities error.")
    args = parser.parse_args()
    
    try:
        file = open('.{}.tags'.format(args.env), 'r')
        
        tags = []
        
        for line in file.readlines():
            key, value = line.strip().split("=")
            tags.append("\\\"{}\\\"=\\\"{}\\\"".format(key, value))
        
    except Exception as e:
        print("Unable to parse tags for environment: {}".format(args.env))
        print(e)
        
    try:
        file = open('.{}.params'.format(args.env), 'r')
        
        params = []
        
        for line in file.readlines():
            key, value = line.strip().split("=")
            params.append("\\\"{}\\\"=\\\"{}\\\"".format(key, value))
        
    except Exception as e:
        print("Unable to parse params for environment: {}".format(args.env))
        print(e)
    
    try:
        samconfig = open('samconfig.toml', 'w')
        
        samconfig.write("version = 0.1" + "\n")
        samconfig.write("[default]" + "\n")
        samconfig.write("[default.deploy]" + "\n")
        samconfig.write("[default.deploy.parameters]" + "\n")
        samconfig.write("stack_name = \"{}\"".format(args.stack_name) + "\n")
        samconfig.write("s3_bucket = \"{}\"".format(args.s3_bucket) + "\n")
        samconfig.write("s3_prefix = \"{}\"".format(args.s3_prefix) + "\n")
        samconfig.write("region = \"{}\"".format(args.region) + "\n")
        samconfig.write("confirm_changeset = {}".format("false") + "\n")
        samconfig.write("capabilities = \"{}\"".format(args.capabilities) + "\n")
        samconfig.write("parameter_overrides = {}".format("\"" + " ".join(params)) + "\"" + "\n")
        samconfig.write("image_repositories = {}".format("[]") + "\n")
        samconfig.write("tags = {}".format("\"" + " ".join(tags)) + "\"")
        
        samconfig.close()
        
    except Exception as e:
        print("Unable to create samconfig.toml configuration file for environment: {}".format(args.env))
        print(e)
    
    
if __name__ == "__main__":
   main()
