import os
from .. import eprover

RESULTS_DIR = os.getenv("EXPRES_RESULTS", "./00RESULTS")

def path(bid, pid, problem, limit, ext="out"):
   d_pid = "%s--%ss" % (pid, limit)
   f_out = "%s.%s" % (problem, ext)
   return os.path.join(RESULTS_DIR, bid, d_pid, f_out)

def output(bid, pid, problem, limit):
   return file(path(bid, pid, problem, limit)).read()

def save(bid, pid, problem, limit, out):
   f_out = path(bid, pid, problem, limit)
   os.system("mkdir -p %s" % os.path.dirname(f_out))
   file(f_out,"w").write(out)

def load(bid, pid, problem, limit, trains=False):
   f_out = path(bid, pid, problem, limit)
   return eprover.result.parse(file(f_out).read(), trains=trains)

