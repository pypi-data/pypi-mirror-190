import click
import os
import subprocess
import json
import time
from jinja2 import Environment, FileSystemLoader
import urllib.request as urllib2
import yaml
from configparser import ConfigParser
from pathlib import Path
import platform
from tabulate import tabulate
import copy
import boto3
import sentry_sdk
import logging
from sentry_sdk.integrations.logging import LoggingIntegration
import sys
import pkg_resources
import requests
import io
from  datetime import datetime
import pcluster_cli

pcluster_cli_path = list(pcluster_cli.__path__)[0]
version = pkg_resources.require("pcluster-cli")[0].version
username = os.environ.get("USER")
slack_channel = "https://hooks.slack.com/services/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"

my_session = boto3.session.Session()
aws_region = my_session.region_name

stream = io.StringIO()
logging.getLogger().addHandler(logging.StreamHandler(stream=stream))
logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().setLevel(logging.INFO)

if  os.path.exists("./pcluster.yaml"):
    sentry_sdk.set_user({"name": username, "region": aws_region})
    sentry_logging = LoggingIntegration(level=logging.DEBUG, event_level=logging.ERROR)

    sentry_sdk.init(
        dsn="https://e8eb4dede07e451d8e8a0e32d8987113@o1376701.ingest.sentry.io/4504560524394496",
        traces_sample_rate=0.0,
        integrations=[sentry_logging],
        release=version
    )

homedir = str(Path.home())
config = ConfigParser()
config.read(str(Path.home() / ".pcluster.ini"))
if "default" not in config.sections():
    config.add_section("default")
    cluster = "pcluster-" + username
    config.set("default", "cluster", cluster)

install_cmd = "pip3 install --upgrade pcluster-cli"
host_type = platform.system()
telemetry = config.get("default", "telemetry", fallback="true")

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

def log_result(**kwargs):
    command = " ".join(sys.argv[1:])
    host = platform.node()
    message = f"{version} {username}@{host}$ pcl {command} \n```" + stream.getvalue() + "```"
    headers={"Content-type":"application/json"}
    try:
        r = requests.post(slack_channel, json={"text": message}, headers=headers)
    except Exception:
        pass

def get_ami():
    prefix = "pcluster-" + username + "-backup" 
    ec2_client = boto3.client('ec2', region_name=aws_region)
    images = ec2_client.describe_images(Owners=['self'])["Images"]
    for im in images:
        if im["Name"].startswith(prefix):
            return im["ImageId"]

def backup_instance():
    cluster = "pcluster-" + username
    logging.info(f"creating ami from {cluster}")
    
    p = subprocess.run(f"pcluster ssh -o \"StrictHostKeyChecking no\"  -n  {cluster} -i {homedir}/.{cluster}.pem \"sudo /var/scripts/backup-start.sh \"",
     stdout=subprocess.PIPE, shell=True)
    if p.returncode != 0:
        logging.error(p.stdout.decode("ascii"))
        raise click.Abort()
    p = subprocess.run(f"pcluster  describe-cluster  -n {cluster}", stdout=subprocess.PIPE, shell=True)
    if p.returncode != 0:
        logging.error(p.stdout.decode("ascii"))
        raise click.Abort()

    clusterobj = json.loads(p.stdout.decode("ascii"))
    if "headNode" not in clusterobj:
        logging.info(f"skipping backup {cluster}")
        return
    instance_id = clusterobj["headNode"]["instanceId"]
    ec2_client = boto3.client('ec2', region_name=aws_region)
    image_prefix= cluster+ "-backup"
    instance_name = image_prefix + "-"+ datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    resp = ec2_client.create_image(InstanceId=instance_id, Name=instance_name, NoReboot=True,
     BlockDeviceMappings=[{'DeviceName': '/dev/xvda','Ebs': {'DeleteOnTermination': False}}])
    imid = resp["ImageId"]
    while True:
        time.sleep(10)
        resp = ec2_client.describe_images(ImageIds=[imid])["Images"][0]
        if resp["State"] != "pending":
            break
        print(".", end="", flush=True)
    if resp["State"] != "available":
        logging.error("image backup returned "+ resp["State"])
        raise click.Abort()

    logging.info(f"created image {imid}")
    images = ec2_client.describe_images(Owners=['self'])["Images"]
    for im in images:
        if im["Name"].startswith(image_prefix) and im["Name"] != instance_name:
            ec2_client.deregister_image(ImageId=im["ImageId"])

    p = subprocess.run(f"pcluster ssh  -o \"StrictHostKeyChecking no\"  -n  {cluster} -i {homedir}/.{cluster}.pem \
     \"sudo /var/scripts/backup-complete.sh \" ", stdout=subprocess.PIPE, shell=True)
    if p.returncode != 0:
        logging.error(p.stdout.decode("ascii"))
        raise click.Abort()
    
    logging.info(f"completed backup {cluster}")


def get_remote_cluster_conf(name):
    p = subprocess.run(f"pcluster  describe-cluster  -n {name}", stdout=subprocess.PIPE, shell=True)
    if p.returncode != 0:
        logging.error(p.stdout.decode("ascii"))
        raise click.Abort()

    cluster = json.loads(p.stdout.decode("ascii"))
    conf_url = cluster["clusterConfiguration"]["url"]
    try :
        webUrl = urllib2.urlopen(conf_url)
        data = webUrl.read()
    except Exception:
        logging.exception(f"unable to get cluster conf")
        raise click.Abort()

    return yaml.safe_load(data.decode('UTF-8'))

def update_cluster_buckets(name, conf, buckets):
    buckets = [*set(buckets)]
    logging.debug(f"current buckets are {buckets}")
    b_str =  ','.join(buckets)
    nodeupdate = conf["HeadNode"]["CustomActions"]["OnNodeUpdated"]
    if len(buckets) == 0:
        nodeupdate["Args"] = [username]
        config.remove_option("default", "s3")
        for queue in  conf["Scheduling"]["SlurmQueues"]:
            queue["CustomActions"]["OnNodeConfigured"]["Args"] = [username]
    else:
        nodeupdate["Args"]= [username, b_str]
        config.set("default", "s3", b_str)
        for queue in  conf["Scheduling"]["SlurmQueues"]:
            queue["CustomActions"]["OnNodeConfigured"]["Args"] = [username, b_str]
    update_cluster(name, conf)
    with open(str(Path.home() / ".pcluster.ini"), "w") as f:
        config.write(f)  

def update_cluster(name, conf):
    with open(f"{homedir}/.pcluster.yaml", "w") as f:
        f.write(yaml.dump(conf))
    logging.info (f"updating cluster {name} configuration")
    p = subprocess.run(f"pcluster update-cluster -n {name} -c {homedir}/.pcluster.yaml", stdout=subprocess.PIPE, shell=True)
    if p.returncode != 0:
        if p.stdout != b"":
            logging.error(p.stdout.decode("ascii"))
        raise click.Abort()

    status = json.loads(p.stdout.decode("ascii"))
    status = status["cluster"]
    while status["clusterStatus"] == "UPDATE_IN_PROGRESS":
        time.sleep(10)
        p = subprocess.run(f"pcluster describe-cluster -n {name}", stdout=subprocess.PIPE, shell=True)
        if p.returncode == 0:
            status = json.loads(p.stdout.decode("ascii"))

        print(".", end="", flush=True)
    logging.info(status["clusterStatus"])


def get_pcluster_config():
    conf_path = str(Path.home() / ".pcluster.json")
    p = subprocess.run(f"aws s3 cp s3://altos-lab-pcluster-config/{aws_region}.json {conf_path} ", stdout=subprocess.PIPE, shell=True)
    if p.returncode != 0:
        if p.stdout != b"":
            logging.error(p.stdout.decode("ascii"))
        logging.error("Default cluster configuration is not available")
        raise click.Abort()
    with open(conf_path) as f:
        return json.load(f)


@click.group()
@click.pass_context
def main(ctx):
    """Group for pcl commands."""
    if telemetry == "true":
        ctx.call_on_close(log_result)

    p = subprocess.run("aws sts get-caller-identity", stdout=subprocess.DEVNULL, shell=True)
    if p.returncode != 0:
        subprocess.run(f"aws sso login", shell=True)
   

@main.command()
@click.option("-mi", "master_instance_type", default="t2.micro", help="master node instance type")
@click.option("-ci", "compute_instance_type", default="t2.micro", help="compute instance type")
@click.option("-max", "max_count", default="4", help="max number of compute nodes")
@click.option("-minc", "min_count", default="0", help="min number of compute nodes")
@click.option("-ami", "ami", required=False, help="custom ami image")
def create(master_instance_type, compute_instance_type, max_count, min_count, ami):
    """create parallel cluster"""
    name= "pcluster-" + username
    dconf = get_pcluster_config()
    master_subnet_id = dconf["master_subnet_id"]
    compute_subnet_id = dconf["compute_subnet_id"]
    efs = dconf["efs"]
    security_groups = dconf["security_groups"]
    if ami == None:
        ami = get_ami()
        if ami == None:
            ami = dconf["ami"]
    
    s3 = config.get("default", "s3", fallback=None)
    
    if not os.path.isfile(f"{homedir}/.{name}.pem"):
        logging.info(f"creating key pair for cluster ")
        p = subprocess.run(f"aws ec2 create-key-pair --key-name {name} --query 'KeyMaterial' --output text >  {homedir}/.{name}.pem", shell=True)
        if p.returncode != 0:
            raise click.Abort()
        os.chmod(f"{homedir}/.{name}.pem", 384)

    env = Environment(loader=FileSystemLoader(pcluster_cli_path), autoescape=False)
    template = env.get_template("pcluster.yaml")
    output = template.render(name=name,user=username,ssh_key=name,
        master_instance_type=master_instance_type,
        compute_instance_type=compute_instance_type, security_groups=security_groups,
        max_count=max_count, min_count=min_count, master_subnet_id=master_subnet_id,
        compute_subnet_id=compute_subnet_id, ami=ami, efs=efs, s3=s3)
    with open(f"{homedir}/.pcluster.yaml", "w") as f:
        f.write(output)
    p = subprocess.run(f"aws s3 cp {pcluster_cli_path}/node-startup.sh s3://altos-lab-pcluster-config/{name}.sh", stdout=subprocess.DEVNULL, shell=True)

    assert p.returncode == 0, "Failed to copy the node startup script to s3://altos-lab-pcluster-config/"

    logging.info(f"creating cluster {name} in {aws_region}...")
    p = subprocess.run(f"pcluster create-cluster -n {name} -c {homedir}/.pcluster.yaml --suppress-validators type:EbsVolumeIopsValidator --rollback-on-failure false", stdout=subprocess.PIPE, shell=True)
    if p.returncode != 0:
        if p.stdout != b"":
            logging.error(p.stdout.decode("ascii"))
        raise click.Abort()
    
    status = json.loads(p.stdout.decode("ascii"))["cluster"]["clusterStatus"]

    while status == "CREATE_IN_PROGRESS":
        time.sleep(10)
        p = subprocess.run(f"pcluster describe-cluster -n {name}", stdout=subprocess.PIPE, shell=True)
        if p.returncode == 0:
            status = json.loads(p.stdout.decode("ascii"))["clusterStatus"]

        print(".", end="", flush=True)

    logging.info(status)
    config.set("default", "cluster", name)
    with open(str(Path.home() / ".pcluster.ini"), "w") as f:
        config.write(f)
    
@main.command(context_settings=dict(ignore_unknown_options=True))
@click.argument("buckets", nargs=-1, type=click.UNPROCESSED)
def s3_add(buckets):
    """mount s3 buckets in parallel cluster nodes"""
    
    name = config.get("default", "cluster")
    if  name != "pcluster-" + username:
        logging.error(f"can not update {name}")
        raise click.Abort()

    conf = get_remote_cluster_conf(name)

    buckets = [b for b in buckets]
    args = conf["HeadNode"]["CustomActions"]["OnNodeUpdated"]["Args"]
    if len(args) > 1 :
        buckets.extend(args[1].split(","))

    update_cluster_buckets(name, conf, buckets)

@main.command(context_settings=dict(ignore_unknown_options=True))
@click.argument("buckets", nargs=-1, type=click.UNPROCESSED)
def s3_delete(buckets):
    """unmount s3 buckets in parallel cluster nodes"""
    name = config.get("default", "cluster")
    if  name != "pcluster-" + username:
        logging.error(f"can not update {name}")
        raise click.Abort()

    conf = get_remote_cluster_conf(name)

    buckets = [b for b in buckets]
    args = conf["HeadNode"]["CustomActions"]["OnNodeUpdated"]["Args"]
    c_buckets = []
    if len(args) > 1:
        c_buckets.extend(args[1].split(","))
    for b in buckets:
        if b in c_buckets:
            c_buckets.remove(b) 

    update_cluster_buckets(name, conf, c_buckets)


@main.command(context_settings=dict(ignore_unknown_options=True))
@click.argument("command", nargs=-1, type=click.UNPROCESSED)
def ssh(command):
    """ssh/run a command inside parallel cluster head node"""

    name = config.get("default", "cluster")
    if not name:
        logging.error("No active cluster")
        raise click.Abort()

    args = ["pcluster", "ssh", "-o StrictHostKeyChecking=no", "-n", name, "-i", f"{homedir}/.{name}.pem"]
    args.extend(command)
    os.execvp("pcluster", args)

@main.command()
@click.option("-b", "backup", default="false", help="true/false creates backup ami image from head node")
def delete(backup):
    """delete parallel cluster"""
    cluster = config.get("default", "cluster")
    if  cluster != "pcluster-" + username:
        logging.error(f"can not delete {cluster}")
        raise click.Abort()
    if backup == "true":
        backup_instance()
    
    logging.info(f"Deleting cluster {cluster}")
    p = subprocess.run(f"pcluster delete-cluster -n {cluster}", stdout=subprocess.PIPE, shell=True)
    if p.returncode != 0:
        logging.error(p.stdout.decode("ascii"))
        raise click.Abort()

    status = json.loads(p.stdout.decode("ascii"))["cluster"]

    while status["clusterStatus"] == "DELETE_IN_PROGRESS":
        time.sleep(10)
        p = subprocess.run(f"pcluster describe-cluster -n {cluster}", stdout=subprocess.PIPE, shell=True)
        if p.returncode == 0:
            status = json.loads(p.stdout.decode("ascii"))
        else :
            break
        print(".", end="", flush=True)
    subprocess.run(f"aws s3 rm s3://altos-lab-pcluster-config/{cluster}.sh", stdout=subprocess.PIPE, shell=True)
    logging.info("DELETED")

@main.command()
def list():
    """list aws parallel clusters"""
    p = subprocess.run("pcluster list-clusters", stdout=subprocess.PIPE, shell=True)
    if p.returncode != 0:
        logging.error(p.stdout.decode("ascii"))
        raise click.Abort()
    results = json.loads(p.stdout.decode("ascii"))
    clusters = [["name", "status", "version", "region", "type"]]
    for c in  results["clusters"]:
        c = Struct(**c)
        clusters.append([c.clusterName, c.clusterStatus, c.version, c.region, c.scheduler["type"]])

    print(tabulate(clusters, headers="firstrow", tablefmt="presto"))

@main.command()
@click.argument("cluster")
def activate(cluster):
    """set default cluster"""
    config.set("default", "cluster", cluster)
    with open(str(Path.home() / ".pcluster.ini"), "w") as f:
        config.write(f)

@main.command()
@click.option("-ci", "compute_instance_type", default="t2.micro", help="compute instance type")
@click.option("-max", "max_count", default="4", help="max number of computes")
@click.option("-min", "min_count", default="0", help="min number of computes")
@click.option("-n", "queue_name", required=True, help="queue name")
def add_queue(queue_name, compute_instance_type, max_count, min_count):
    """add new slurm queue to the parallel cluster"""
    cluster = config.get("default", "cluster")
    if  cluster != "pcluster-" + username:
        logging.error(f"can not add queue to the {cluster} cluster")
        raise click.Abort()
    conf = get_remote_cluster_conf(cluster)
    queues = [q for q in conf["Scheduling"]["SlurmQueues"]]
    if any(x["Name"] == queue_name  for x in queues):
        logging.info(f"queue with {queue_name} already exists")
        return 

    queue = copy.deepcopy(queues[0])
    queue["Name"] = queue_name
    resource = queue["ComputeResources"][0]
    resource["Name"] = queue_name
    resource["Instances"][0]["InstanceType"] = compute_instance_type
    resource["MinCount"] = min_count
    resource["MaxCount"] = max_count
    queues.append(queue)
    conf["Scheduling"]["SlurmQueues"] = queues
    update_cluster(cluster, conf)


@main.command()
@click.option("-n", "queue_name", required=True , help="queue name")
def delete_queue(queue_name):
    """remove existing slurm queue """
    cluster = config.get("default", "cluster")
    if  cluster != "pcluster-" + username:
        logging.error(f"can not add queue to the {cluster} cluster")
        raise click.Abort()
    conf = get_remote_cluster_conf(cluster)
    queues = conf["Scheduling"]["SlurmQueues"]
    if len(queues) == 1 :
        logging.info("Atleast one queue should be there in cluster.")
        raise click.Abort()
    if all(x["Name"] != queue_name  for x in queues):
        logging.info(f"queue with {queue_name} doesn't exist.")
        raise click.Abort()
    for q in queues:
        if q["Name"] == queue_name:
            queues.remove(q)
            break
    logging.info("updating cluster")
    update_cluster(cluster, conf)


@main.command()
def list_queues():
    """list existing slurm queues in a cluster """
    cluster = config.get("default", "cluster")
    logging.info(f"Current cluster: {cluster}")
    conf = get_remote_cluster_conf(cluster)
    qs = conf["Scheduling"]["SlurmQueues"]
    queues = [["Name", "Instance Type", "Minimum Compute Count", "Maximum Compute Count"]]
    for q in  qs:
        r = q["ComputeResources"][0]
        queues.append([q["Name"], r["Instances"][0]["InstanceType"] , r["MinCount"], r["MaxCount"]])

    print(tabulate(queues, headers="firstrow", tablefmt="presto"))

@main.command()
def save_ami():
    """save parallel cluster head node as ami"""
    cluster = config.get("default", "cluster")
    if  cluster != "pcluster-" + username:
        logging.error(f"can not save image of {cluster}")
        raise click.Abort()
    backup_instance()
