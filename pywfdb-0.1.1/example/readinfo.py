import pywfdb
import time

record = "d:/mitdb/101"

rec = pywfdb.Record(record)

print rec

print
print "Reading data from %d signals from record %s:" % (rec.nsig, rec.record)

for name in rec.signal_names:
    print ("Reading 20000 of %d samples from signal %s..." % 
                                (rec.signal_info(name)["samples"], name)),

    signal = rec.read(name, start=1000, length=20000)
    print " got %d samples." % len(signal)
    print "Printing 5 samples:", "[%.3f, %.3f, %.3f, %.3f, %.3f]" % tuple(signal[:5])
    print 
    

print "Reading first 5s of annotation from record %s:" % rec.record

ann = rec.annotation() # assuming default annotation file '.atr'
for a in ann.read(0, int(5*rec.frequency)):
    print " ", a

print
print "Reading 5s of annotation from record %s, filtered by type N:" % rec.record
ann = rec.annotation()
for a in ann.read(0, int(5*rec.frequency), anntype=pywfdb.EcgCodes.NORMAL):
    print " ", a



