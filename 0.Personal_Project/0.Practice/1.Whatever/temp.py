import time
 
def elapsed_time(functor):
     def decorated(*args, **kwargs):
             start = time.time()
             functor(args, kwargs)
             end = time.time()
             print "Elapsed time: %f" % (end-start)
     return decorated
   
 
@elapsed_time
def hello():
     print 'hello'
