# AWS CMD TOOL

## Setup  ##
- aws cli install
- kubectl install
- terraform install
- helm install
  - brew install kubernetes-helm
- install python modules
  - pip install boto3 inquirer argcomplete
  - pip install pyyaml

  - copy or create symbol link of awstool to /usr/local/bin/awstool
  - add this line to `~/.bashrc`
    
    eval "$(register-python-argcomplete awstool)"
    
Then you use awstool to login aws, switch aws account, login ec2 instance, search or update secrets manager
