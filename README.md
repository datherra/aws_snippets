## AWS Playground

### Setting up a Squid Proxy

Working version of a Python script using boto (2.38) to start, stop and list EC2 VMs

1. create a `.boto` file in your `$HOME` directory containing:
```
[Credentials]
aws_access_key_id = <your access key>
aws_secret_access_key = <your secret access key>
```

2. The script `aws.py` doesn't create the Key/Pair for you. It considers that you already have one set.

3. The `aws.py` script also relies on the following environment variables being set:
```
export AWS_KEY_NAME=<your valid key/pair name>
export AWS_KEY_FILE=< /full/path/to/your/key.pem >
```

4. You can relly on the script and Ansible playbook to automaticaly detect your source IP address while configuring AWS Security Groups and Squid ACLs or, you provide your CIDRs as shown below:
```
# Change to your CIDRs. The example below uses Google's.
# Separate with comma if more than one block.
export SOURCE_CIDRS=27.33.250.121/32,220.240.229.121/32
```

5. The `ec2.py` dynamic inventory file is the same one found at [Ansible dynamic inventory scripts](https://github.com/ansible/ansible/tree/devel/contrib/inventory).


### TODO
- update boto
- verify if it will break
- update AMI
- create class(es)
- use setuptools