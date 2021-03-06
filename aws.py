#! /usr/bin/env python
import boto.ec2
import sys
import time
import os
import httplib

def delete_security_groups(_groups):
  for _group in _groups:
    _group.delete()
    print "Deleting: %s" % _group


def print_security_groups(_groups):
  for _group in _groups:
    print "Group: %s" % _group
    print "Rules: %s" % _group.rules


def terminate_all_instances(ec2):
  _instances = ec2.get_only_instances()
  for _instance in _instances:
    if _instance.state == 'terminated':
      continue
    print "Terminating: %s" % _instance.dns_name
    _instance.terminate()


def list_all_instances(ec2):
  _instances = ec2.get_only_instances()
  for _instance in _instances:
    print '''\
      Instance: %s
      State:   %s
      ''' % (_instance.dns_name, _instance.state)


def detect_source_addresses():
  if 'SOURCE_CIDRS' in os.environ:
    return os.environ['SOURCE_CIDRS'].split(',')
  else:
    h1 = httplib.HTTPConnection('ipecho.net')
    h1.request('GET', '/plain')
    source_ip = "%s/32" % h1.getresponse().read()
    return [source_ip]


def setup_security_group(ec2, sg_name, source_addresses):
  group_name = sg_name
  group_filter = { 'group-name': group_name }
  groups = ec2.get_all_security_groups(filters=group_filter)
  if groups:
    print "There are squid security groups already: %s" % str(groups)
    print_security_groups(groups)
  else:
    print "Creating squid security group..."
    new_sg = ec2.create_security_group(group_name, 'allow proxing')
    for source_cidr in source_addresses:
      new_sg.authorize('tcp','3128','3128',source_cidr)
      new_sg.authorize('tcp','22','22',source_cidr)
    sgs = ec2.get_all_security_groups()
    print_security_groups(sgs)


def is_connecting(ec2, instance):
  server = instance
  status = ''
  while status != 'ok':
    print "Checking connectivity... Status: %s" % status
    time.sleep(15)
    status = ec2.get_all_instance_status(instance_ids=[server.id])[0].instance_status.status
  return True


def launch_instance(ec2, security_group_name):
  key = os.environ['AWS_KEY_NAME']
  reservation = ec2.run_instances('ami-8737829a', instance_type = 'm3.medium', security_groups=[security_group_name], key_name=key)
  server = reservation.instances[0]
  while server.state != 'running':
    print "Lauching instance... Status: %s" % server.state
    time.sleep(10)
    server.update()
  print "Instance running!"
  if is_connecting(ec2, server):
    print '''
    Instance ready!
    IP: %s
    Connection string:
    ssh -i %s ec2-user@%s
    ''' % (server.ip_address, os.environ['AWS_KEY_FILE'], server.dns_name)  


def usage(command):
  return "Usage: %s list|start|stop" % command


conn = boto.ec2.connect_to_region('sa-east-1')

if len(sys.argv) == 1:
  print usage(sys.argv[0])
elif sys.argv[1] == 'start':
  my_ips = detect_source_addresses()
  setup_security_group(conn, 'squid', my_ips)
  launch_instance(conn, 'squid')
elif sys.argv[1] == 'stop':
  terminate_all_instances(conn)
elif sys.argv[1] == 'list':
  list_all_instances(conn)
else:
  print usage(sys.argv[0])
