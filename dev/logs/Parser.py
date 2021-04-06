#!/usr/bin/env python
import sys
sys.path.append('../')
import Drain

input_dir  = 'logs/'  # The input directory of log file
output_dir = 'logs/'  # The output directory of parsing results
log_file   = 'syslog'  # The input log file name
log_format = '<Month> <Date> <Time> <Level> <Component>(\[<PID>\])?: <Content>'
regex = [r'(\d+\.){3}\d+', r'\d{2}:\d{2}:\d{2}']
st = 0.39
depth = 6 

parser = Drain.LogParser(log_format, indir=input_dir, outdir=output_dir,  depth=depth, st=st, rex=regex)
parser.parse(log_file)

