# -*- coding: utf-8 -*-

# Copyright (c) 2006 Filip Wasilewski <filipwasilewski@gmail.com>
# See COPYING for license details.

cimport c_python
cimport c_string
cimport c_wfdb
from c_wfdb cimport WFDB_Siginfo, WFDB_Sample, WFDB_Anninfo

from os.path import dirname, basename, isdir, splitext
from os import chdir, getcwdu

cdef c_python.PyObject* currently_opened
currently_opened = NULL

cdef int is_opened(object this):
    """
    Check if given signal is currently opened.
    """
    global currently_opened
    return (currently_opened == <c_python.PyObject*>this)
 
cdef set_opened(object this):
    """
    Set currently opened signl.
    """
    global currently_opened
    currently_opened = <c_python.PyObject*> this

def verbose(flag=True):
    """
    Set wfdblib to verbose mode (prints some extra info on error).
    Debug only.
    """
    if flag:
        c_wfdb.wfdbverbose()
    else:
        c_wfdb.wfdbquiet()

class Error(Exception):
    pass

class InitError(Error):
    pass

STAT_READ = c_wfdb.WFDB_READ
"""Stat annotation access flag."""

STAT_READ_AHA = c_wfdb.WFDB_AHA_READ
"""Stat annotation access flag."""

cdef public class Record [object PyRecord, type RecordType]:
    """Access MIT-BIH database records.

    Record(string record)

        record - path to record (without extension. i.e. c:/physiobank/100)

    fields:

        record       - record name
        nsig         - number of signals in record
        frequency    - sampling frequency
        signal_names - signals names
        name         - alias for record
    """

    cdef init_record_name
    cdef readonly record   #record name
    
    cdef readonly basedir  #path to record
    cdef readonly int nsig #number of signals
    cdef readonly c_wfdb.WFDB_Frequency frequency #frequency
    cdef readonly object signal_names
    cdef c_wfdb.WFDB_Siginfo* siginfo
    
    def __new__(self, char* record):
        """
        Open record

        record - path to record (without extension. i.e. c:/physiobank/100)
        """
        self.siginfo = NULL
        self.nsig = 0

        self.init_record_name = record
        self.basedir = dirname(record)
        cwd = getcwdu()

        if self.basedir:
            chdir(self.basedir)
        
        self.record = splitext(basename(record))[0]
        if self.record.startswith('+'):
            raise ValueError, "Record name can not start with '+'"
        
        self.nsig = c_wfdb.isigopen(self.record, NULL, 0)

        self.frequency =  c_wfdb.sampfreq(self.record)
        if self.frequency < 0: # error reading header
            self.frequency = 0

        if self.basedir:
            chdir(cwd)

        if self.nsig <= 0:
            raise InitError, c_wfdb.wfdberror()
        
        self.siginfo = <c_wfdb.WFDB_Siginfo *> c_python.PyMem_Malloc(self.nsig * sizeof(WFDB_Siginfo))
        if self.siginfo == NULL: 
            raise MemoryError 
        
        self.reopen()

        names = []
        for signal in xrange(self.nsig):
            names.append(self.siginfo[signal].desc)
        self.signal_names = tuple(names)


    property name:
        def __get__(self):
            return self.record

    def __dealloc__(self):
        global currently_opened
        if is_opened(self):
            currently_opened = NULL
            #c_wfdb.isigclose() #TODO check 
        if self.siginfo:
            c_python.PyMem_Free(self.siginfo) 
    
    #due to limitations of WFDB library, if someone wants to access multiple signals at once
    cdef void reopen(self):
        """
        Ensure that signal file is currently opened.
        """

        if is_opened(self):
            return

        cwd = getcwdu()
        if self.basedir:
            chdir(self.basedir)

        if c_wfdb.isigopen(self.record, self.siginfo, self.nsig) <= 0:
            raise InitError, c_wfdb.wfdberror()
        
        set_opened(self)
        
        if self.basedir:
            chdir(cwd)

    cdef int opened(self):
        global currently_opened
        return (currently_opened == <c_python.PyObject*>self)

    cdef signal_number(self, object name_or_number):
        """
        signal number or signal name -> signal number
        """
        if type(name_or_number) is int:
            if not (0 <= name_or_number < self.nsig):
                raise ValueError, "invalid signal number"
            return name_or_number
        elif type(name_or_number) in (str, unicode) and name_or_number in self.signal_names:
            for i in xrange(self.nsig):
                if name_or_number == self.signal_names[i]:
                    return i
        
        raise ValueError, "Wrong signal number or name"

    def read(self, signal_id, c_wfdb.WFDB_Time start = 0, c_wfdb.WFDB_Time length = 0, correct_gain=True):
        """
        read(signal_id, start=0, length=0, correct_gain=True) -> list
        
            signal_id    - signal number or signal name in record
            start        - index in sample intervals from the beginning of the record 
            length       - sample count, if 0 - read all annotations
            correct_gain - return values in real physical units instead of sampled data file values
        """

        cdef c_wfdb.WFDB_Time i
        cdef double gain
        cdef int signal
        
        signal = self.signal_number(signal_id)

        self.reopen()

        if not (0 <= signal < self.nsig):
            raise ValueError, "invalid signal number"

        if start >= self.siginfo[signal].nsamp:
            raise ValueError, "start index out of range (%Lu)" % self.siginfo[signal].nsamp
        if length < 0:
            raise ValueError, "invalid length"

        if length == 0:
            length = self.siginfo[signal].nsamp

        if (start + length) > self.siginfo[signal].nsamp:
            length = self.siginfo[signal].nsamp - start
        
        if c_wfdb.isigsettime(start) < 0:   #set signal position
            raise InitError, c_wfdb.wfdberror()

        cdef object ret
        ret = c_python.PyList_New(length)
        
        cdef c_wfdb.WFDB_Sample* vector
        vector = <c_wfdb.WFDB_Sample *> c_python.PyMem_Malloc(self.nsig * sizeof(WFDB_Sample))
        if vector == NULL: 
            raise MemoryError

        #append = ret.append
        if correct_gain:
            if self.siginfo[signal].gain == 0.0:
                gain = c_wfdb.WFDB_DEFGAIN
            else:
                gain = self.siginfo[signal].gain
            
            for i from 0 <= i < length:
                c_wfdb.getvec(vector)
                
                if c_python.PyList_SetItem(ret, i, c_python.PyFloat_FromDouble((vector[signal]-self.siginfo[signal].adczero)/gain)) < 0:
                    raise RuntimeError, "Can not set list item <PyList_SetItem>"
                #append( ((vector[signal] - self.siginfo[signal].adczero)) / gain )
        else:
            for i from 0 <= i < length:
                c_wfdb.getvec(vector)
                if c_python.PyList_SetItem(ret, i, c_python.PyInt_FromLong( vector[signal]-self.siginfo[signal].adczero )) < 0:
                    raise RuntimeError, "Can not set list item <PyList_SetItem>"
                #append((<double> (vector[signal] - self.siginfo[signal].adczero)))

        c_python.PyMem_Free(vector)
        return ret

    def annotation(self, name = 'atr',  stat=STAT_READ):
        """
        annotation(name='atr', stat=STAT_READ) -> Annotation
            name - annotation name (file extension)

        Returns Annotation object for record.
        """
        return Annotation(self.init_record_name, name)

    def signal_info(self, signal_id):
        """
        signal_info(signal_id) -> dict
            signal_id   - signal number or signal name in record

        Returns dictionary with information about specified signal.
        """
        cdef int signal
        signal = self.signal_number(signal_id)

        self.reopen()
        
        info = dict()
        
        info["record"] = self.record
        info["file"] = self.siginfo[signal].fname
        info["frequency"] = self.frequency
        info["description"] = self.siginfo[signal].desc
        info["adc_zero"] = self.siginfo[signal].adczero
        info["adc_resolution"] = self.siginfo[signal].adcres
        info["initial_value"] = self.siginfo[signal].initval
        info["storage_format"] = self.siginfo[signal].fmt

        if self.siginfo[signal].gain == 0.0:
            info["gain"] = WFDB_DEFGAIN
        else:
            info["gain"] = self.siginfo[signal].gain

        if self.siginfo[signal].units:
            info["units"] = self.siginfo[signal].units
        else:
            info["units"] = "mV"

        info["starting_time"] = c_wfdb.timstr(0)
        if self.siginfo[signal].nsamp > 0:
            info["length"] = c_wfdb.timstr(self.siginfo[signal].nsamp)
            info["samples"] = self.siginfo[signal].nsamp
            info["checksum"] = self.siginfo[signal].cksum
            
        return info

    def __repr__(self):
        return "pywfdb.Record(%s)" % self.init_record_name


    def __str__(self):
        """
        Information about record.
        """
        self.reopen()

        s = []

        s.append("Record %s\n" % self.record)
        s.append("Starting time:  %s\n" % c_wfdb.timstr(0))
        s.append("Sampling frequency: %g Hz\n" % self.frequency)
        s.append("%d signals\n" % self.nsig)

        for signal from 0 <= signal < self.nsig:
            s.append("Signal %d:\n" % (signal))
            s.append(" File: %s\n" %  self.siginfo[signal].fname)
            s.append(" Description: %s\n" % self.siginfo[signal].desc)
            s.append(" Gain: ")
            
            if self.siginfo[signal].gain == 0.0:
                s.append("uncalibrated assume %g" %  c_wfdb.WFDB_DEFGAIN)
            else:
                s.append("%g" %  self.siginfo[signal].gain)
            
            if self.siginfo[signal].units:
                s.append(" adu/%s\n" %  self.siginfo[signal].units)
            else:
                s.append(" adu/%s\n" % "mV")
                
            s.append(" Initial value: %d\n" %  self.siginfo[signal].initval)
            s.append(" Storage format: %d\n" %  self.siginfo[signal].fmt)
            s.append(" I/O: ")
 
            if self.siginfo[signal].bsize == 0:
                s.append("can be unbuffered\n")
            else:
                s.append("%d-byte blocks\n" %  self.siginfo[signal].bsize)

            s.append(" ADC resolution: %d bits\n" %  self.siginfo[signal].adcres)
            s.append(" ADC zero: %d\n" %  self.siginfo[signal].adczero)
            if self.siginfo[signal].nsamp > 0:
                s.append(" Length: %s (%ld sample intervals)\n" % (
                    c_wfdb.timstr(self.siginfo[signal].nsamp), self.siginfo[signal].nsamp))
                s.append(" Checksum: %d\n" %  self.siginfo[signal].cksum)
            else:
                s.append(" Length undefined\n")

        return "".join(s)


    def close(self):
        """
        Close record files.
        """
        if self.opened():
            #isigclose() #TODO
            set_opened(None)


cdef class AnnotationEntry:             # WFDB_Annotation, not WFDB_Anninfo
    """
    Represents annotation event

    AnnotationEntry(int time, int type, int subtype=0, int channel=0, int annotator=0, string aux="")
        
        time      - annotation time, in sample intervals from the beginning of the record 
        type      - annotation type (see EcgCodes)
        subtype   - annotation subtype
        channel   - channel number
        annotator - annotator number
        aux       - auxiliary information 

    fields:

        time      - annotation time, in sample intervals from the beginning of the record 
        type      - annotation type
        subtype   - annotation subtype
        channel   - channel number
        annotator - annotator number
        aux       - auxiliary information 
        isqrs     - if annotation is of qrs type
        typestr   - string representation of annotation type
        description - description of annotation type

    """
    cdef unsigned char anntype          # annotation type (< ACMAX, see <wfdb/ecgcodes.h> 
    cdef public c_wfdb.WFDB_Time time   # annotation time, in sample intervals from the beginning of the record 
    cdef public signed char subtype     # annotation subtype 
    cdef public signed char channel     # channel number 
    cdef public char annotator          # annotator number 
    cdef readonly aux             # pointer to auxiliary information 
    
    def __new__(self, c_wfdb.WFDB_Time time, unsigned short type, signed short subtype = 0, signed short channel = 0, signed short annotator = 0, char* aux=NULL):
        """
        Create new entry.

        time    - annotation time, in sample intervals from the beginning of the record 
        type    - annotation type
        subtype - annotation subtype
        channel - channel number
        annotator - annotator number
        aux     - auxiliary information 
        """
        self.time = time
        self.type = type
        self.subtype = subtype
        self.channel = channel 
        self.annotator = annotator
        if aux:
            self.aux = aux

    #proxy to self.anntyp
    property type:
        """Annotation type"""
        def __set__(self, value):
            if not 0 < value < c_wfdb.ACMAX:
                raise ValueError, "annotation type value out of range"
            self.anntype = value
        def __get__(self):
            return self.anntype
    
    property isqrs:
        """Check if type is QRS"""
        def __get__(self):
            return c_python.PyBool_FromLong(c_wfdb.isqrs(self.anntype))

    property typestr:
        """Return string representing type"""
        def __get__(self):
            return c_wfdb.annstr(self.anntype)
        def __set__(self, char* value):
            self.anntype = c_wfdb.strann(value)

    property description:
        """Return description for type"""
        def __get__(self):
            return c_wfdb.anndesc(self.anntype)
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self.aux:
            ret = "[%s (%d) %Lu] - %s at %s, %s." % (self.typestr, self.anntype, self.time, self.description, c_wfdb.timstr(self.time).strip(), self.aux)
        else:
            ret = "[%s (%d) %Lu] - %s at %s." % (self.typestr, self.anntype, self.time, self.description, c_wfdb.timstr(self.time).strip())
        return ret

    cdef c_wfdb.WFDB_Annotation get_struct(self):
        cdef c_wfdb.WFDB_Annotation an
        an.time = self.time
        an.anntyp = self.anntype
        an.subtyp = self.subtype
        an.chan = self.channel
        an.num = self.annotator
        an.aux = self.aux
        return an


cdef public class Annotation [object PyAnnotation, type AnnotationType]:
    """
    Access annotation files.

    Annotation(record, name='atr', stat=STAT_READ)

        record  - path to record
        name    - name of annotation file (extension)
        stat    - annotation access mode
                  STAT_READ - read annotation in MIT-BIH format
                  STAT_READ_AHA - read annotation in AHA format

    fields:
        record  - record name
        basedir - directory with record file
        
    """

    cdef init_record_name
    cdef readonly record   #record name
    cdef readonly basedir  #path to record
    cdef c_wfdb.WFDB_Anninfo anninfo
    #cdef readonly annotations

    cdef readonly name

    #def __new__(self, *args, **kwrds):
        #self.WFDB_READ = stat.WFDB_READ
        #self.WFDB_AHA_READ =stat.WFDB_AHA_READ
        #self.annotations = None
    
    def __new__(self, char* record, name ="atr", stat=STAT_READ):
        """
        Open annotation file.

        record - path to record
        name   - name of annotation file (extension)
        stat   - annotation access mode
                 STAT_READ - read annotation in MIT-BIH format
                 STAT_READ_AHA - read annotation in AHA format
        """

        if stat != STAT_READ and stat != STAT_READ_AHA:
            raise ValueError, "Invalid stat"

        self.init_record_name = record
        
        self.name = name # incref
        self.anninfo.name = name
        
        self.anninfo.stat = stat
    
        self.basedir = dirname(record) 
        cwd = getcwdu()

        self.record = splitext(basename(record))[0]
        if self.record.startswith('+'):
            raise ValueError, "Record name can not start with '+'"

        if self.basedir:
            chdir(self.basedir)
        
        if c_wfdb.annopen(self.record, &self.anninfo, 1) < 0:
            if self.basedir: 
                chdir(cwd)
            raise InitError, wfdberror()

        set_opened(self)

        #cdef WFDB_Annotation annot
        #while getann(0, &annot) == 0:
        #   print annot.time, annot.anntyp
        #   self.annotations.append(AnnotationEntry(annot.time, annot.anntyp, annot.subtyp, annot.chan, annot.num))

        if self.basedir: 
            chdir(cwd)

    def __repr__(self):
        return "pywfdb.Annotation(%s, name='%s', stat=%d)" % (self.init_record_name, self.anninfo.name, self.anninfo.stat)

    def read(self, c_wfdb.WFDB_Time start=0, c_wfdb.WFDB_Time length=0, anntype = 0, int annotator = 0):
        """read(start=0, length=0, anntype=0, annotator=0) -> list [AnnotationEntry]
            start   - starting index
            length  - samples count, if 0 - read all annotations
            anntype - filter annotations by type (see EcgCodes)

        Returns list of AnnotationEntry objects.
        """
        cdef c_wfdb.WFDB_Annotation annot
        cdef int anntype_

        if type(anntype) is int:
            anntype_ = anntype
        elif type(anntype_) in (str, unicode):
            anntype_ = c_wfdb.strann(anntype)
        else:
            raise ValueError, "Incorrect annotation type"

        if not is_opened(self):
            cwd = getcwdu()
            if self.basedir:
                chdir(self.basedir)

            if c_wfdb.annopen(self.record, &self.anninfo, 1) < 0:
                if self.basedir:
                    chdir(cwd)
                raise InitError, wfdberror()
            
            if self.basedir:
                chdir(cwd)
            set_opened(self)

        if start >= 0:
            if c_wfdb.iannsettime(start) < 0:
                raise ValueError, c_wfdb.wfdberror()

        annotations = []
        add = annotations.append
        cdef c_wfdb.WFDB_Time end
        
        if length:
            end = start + length
            if anntype_:
                while (c_wfdb.getann(annotator, &annot) == 0) and (annot.time < end):
                    if annot.anntyp != anntype_:
                        continue
                    add(AnnotationEntry(annot.time, annot.anntyp, annot.subtyp, annot.chan, annot.num))
            else:
                while (c_wfdb.getann(annotator, &annot) == 0) and (annot.time < end):
                    #if annot.aux:
                    #   add(AnnotationEntry(annot.time, annot.anntyp, annot.subtyp, annot.chan, annot.num, annot.aux))
                    #else:
                    add(AnnotationEntry(annot.time, annot.anntyp, annot.subtyp, annot.chan, annot.num))

        else:
            if anntype_:
                while c_wfdb.getann(annotator, &annot) == 0:
                    if annot.anntyp != anntype_:
                        continue
                    #if annot.aux:
                    #   add(AnnotationEntry(annot.time, annot.anntyp, annot.subtyp, annot.chan, annot.num, annot.aux))
                    #else:
                    add(AnnotationEntry(annot.time, annot.anntyp, annot.subtyp, annot.chan, annot.num))
            else:
                while c_wfdb.getann(annotator, &annot) == 0:
                    #if annot.aux:
                    #   add(AnnotationEntry(annot.time, annot.anntyp, annot.subtyp, annot.chan, annot.num, annot.aux))
                    #else:
                    add(AnnotationEntry(annot.time, annot.anntyp, annot.subtyp, annot.chan, annot.num))

        return annotations
            

verbose(0)

__all__ = ['Record', 'Annotation', 'AnnotationEntry', 'InitError', 'verbose', 'STAT_READ', 'STAT_READ_AHA']

