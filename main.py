#!/usr/bin/env python2
import pika,argparse
import json, sys,time
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('dummy_generator')

parser = argparse.ArgumentParser(description='generates dummy package on given exchange against AMQP')
parser.add_argument('--host',default='141.31.8.11',      help='AMQP host ip address')
#parser.add_argument('--port',type=int,default=5672,      help='AMQP host port')
parser.add_argument('-u','--username',default='guest',   help='AMQP username') 
parser.add_argument('-p','--password',default='guest',   help='AMQP password') 
parser.add_argument('-e','--exchange',default='mail_src',help='AMQP Exchange to connect to') 
parser.add_argument('-q','--quiet',action='store_true',help='will only(!) write data from exchange to stdout') 

args = parser.parse_args()

if args.quiet:
  logging.basicConfig(level=logging.ERROR)

log.debug ('Parameters %s' % args)

connection = pika.AsyncoreConnection(pika.ConnectionParameters(
          credentials = pika.PlainCredentials(args.username,args.password), 
          host=args.host))
channel = connection.channel()

channel.exchange_declare(exchange=args.exchange,
                             type='fanout')
queue_name = channel.queue_declare(exclusive=True).queue

channel.queue_bind(exchange=args.exchange,
                   queue=queue_name)

print 'Waiting for logs. To exit press CTRL+C'

def callback(ch, method, header, body):
    log.info (header)
    print "%r" % (body,)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)
pika.asyncore_loop()
