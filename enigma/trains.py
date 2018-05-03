
PREFIX = {
   "+": "+1",
   "-": "+10",
   "*": "Should not ever see me"
}

BOOSTS = {
   "WRONG:POS": 1,
   "WRONG:NEG": 10
}

def count(ftrs, counts, emap, offset, strict=True):
   for ftr in ftrs:
      if "/" in ftr:
         parts = ftr.split("/")
         ftr = parts[0]
         inc = int(parts[1])
         if inc == 0:
            continue
      else:
         inc = 1
      if (not strict) and (ftr not in emap):
         continue
      fid = emap[ftr] + offset
      counts[fid] = counts[fid]+inc if fid in counts else inc

def encode(pr, emap, strict=True):
   (sign,clause,conj) = pr.strip().split("|")
   counts = {}
   count(clause.strip().split(" "), counts, emap, 0, strict)
   count(  conj.strip().split(" "), counts, emap, len(emap), strict)
   ftrs = ["%s:%s"%(fid,counts[fid]) for fid in sorted(counts)] 
   ftrs = "%s %s"%(PREFIX[sign], " ".join(ftrs))
   return ftrs

def make(pre, emap, out=None, strict=True):
   train = []
   for pr in pre:
      tr = encode(pr, emap, strict)
      if out:
         out.write(tr)
         out.write("\n")
      else:
         train.append(tr)
   return train if not out else None

def boost(f_in, f_out, out, method="WRONG:POS"):
   if method not in BOOSTS:
      raise Exception("Unknown boost method (%s)")
   CLS = BOOSTS[method]

   ins = file(f_in).read().strip().split("\n")
   outs = file(f_out).read().strip().split("\n")

   for (correct,predicted) in zip(ins,outs):
      out.write(correct)
      out.write("\n")
      cls = int(correct.split()[0])
      if cls == CLS and cls != int(predicted):
         out.write(correct)
         out.write("\n")

