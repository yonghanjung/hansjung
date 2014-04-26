cdef extern from "ecgcodes.h":
    int ACMAX

cdef extern from "ecgmap.h":
    # macros from ecgmap.h
    cdef char isann(int A) 
    cdef char isqrs(int A) 


cdef extern from "wfdb.h":
    ctypedef int         WFDB_Sample    #/* units are adus */
    ctypedef long        WFDB_Time      #/* units are sample intervals */
    ctypedef long        WFDB_Date      #/* units are days */
    ctypedef double      WFDB_Frequency #/* units are Hz (samples/second/signal) */
    ctypedef double      WFDB_Gain      #/* units are adus per physical unit */
    ctypedef unsigned int WFDB_Group    #/* signal group number */
    ctypedef unsigned int WFDB_Signal   #/* signal number */
    ctypedef unsigned int WFDB_Annotator#/* annotator number */ 


    cdef struct WFDB_siginfo:#/* signal information structure */
        char *fname     #/* filename of signal file */
        char *desc      #/* signal description */
        char *units     #/* physical units (mV unless otherwise specified) */
        WFDB_Gain gain  #/* gain (ADC units/physical unit, 0: uncalibrated) */
        WFDB_Sample initval #/* initial value (that of sample number 0) */
        WFDB_Group group    #/* signal group number */
        int fmt         #/* format (8, 16, etc.) */
        int spf         #/* samples per frame (>1 for oversampled signals) */
        int bsize       #/* block size (for character special files only) */
        int adcres      #/* ADC resolution in bits */
        int adczero     #/* ADC output given 0 VDC input */
        int baseline    #/* ADC output given 0 physical units input */
        long nsamp      #/* number of samples (0: unspecified) */
        int cksum       #/* 16-bit checksum of all samples */

    cdef struct WFDB_calinfo:#/* calibration information structure */
        double low      #/* low level of calibration pulse in physical units */
        double high     #/* high level of calibration pulse in physical units */
        double scale    #/* customary plotting scale (physical units per cm) */
        char *sigtype   #/* signal type */
        char *units     #/* physical units */
        int caltype     #/* calibration pulse type (see definitions above) */

    cdef struct WFDB_anninfo:#/* annotator information structure */
        char *name      #/* annotator name */
        int stat        #/* file type/access code (READ, WRITE, etc.) */

    cdef struct WFDB_ann:   #/* annotation structure */
        WFDB_Time time  #/* annotation time, in sample intervals from the beginning of the record */
        char anntyp     #/* annotation type (< ACMAX, see <wfdb/ecgcodes.h> */
        signed char subtyp  #/* annotation subtype */
        signed char chan    #/* channel number */
        signed char num     #/* annotator number */
        char *aux       #/* pointer to auxiliary information */ 

    ctypedef WFDB_siginfo WFDB_Siginfo
    ctypedef WFDB_calinfo WFDB_Calinfo
    ctypedef WFDB_anninfo WFDB_Anninfo
    ctypedef WFDB_ann WFDB_Annotation 

    ctypedef char *FSTRING
    ctypedef WFDB_Date FDATE
    ctypedef double FDOUBLE
    ctypedef WFDB_Frequency FFREQUENCY
    ctypedef int FINT
    ctypedef long FLONGINT
    ctypedef WFDB_Sample FSAMPLE
    ctypedef WFDB_Time FSITIME
    ctypedef void FVOID

    cdef FINT annopen(char *record, WFDB_Anninfo *aiarray, unsigned int nann)
    cdef FINT isigopen(char *record, WFDB_Siginfo *siarray, int nsig)
    cdef FINT osigopen(char *record, WFDB_Siginfo *siarray, unsigned int nsig)
    cdef FINT osigfopen(WFDB_Siginfo *siarray, unsigned int nsig)
    cdef FINT wfdbinit(char *record, WFDB_Anninfo *aiarray, unsigned int nann, WFDB_Siginfo *siarray, unsigned int nsig)
    cdef FINT getspf()
    cdef FVOID setgvmode(int mode)
    cdef FINT setifreq(WFDB_Frequency freq)
    cdef FFREQUENCY getifreq()
    cdef FINT getvec(WFDB_Sample *vector)
    cdef FINT getframe(WFDB_Sample *vector)
    cdef FINT putvec(WFDB_Sample *vector)
    cdef FINT getann(WFDB_Annotator a, WFDB_Annotation *annot)
    cdef FINT ungetann(WFDB_Annotator a, WFDB_Annotation *annot)
    cdef FINT putann(WFDB_Annotator a, WFDB_Annotation *annot)
    cdef FINT isigsettime(WFDB_Time t)
    cdef FINT isgsettime(WFDB_Group g, WFDB_Time t)
    cdef FINT iannsettime(WFDB_Time t)
    cdef FSTRING ecgstr(int annotation_code)
    cdef FINT strecg(char *annotation_mnemonic_string)
    cdef FINT setecgstr(int annotation_code, char *annotation_mnemonic_string)
    cdef FSTRING annstr(int annotation_code)
    cdef FINT strann(char *annotation_mnemonic_string)
    cdef FINT setannstr(int annotation_code, char *annotation_mnemonic_string)
    cdef FSTRING anndesc(int annotation_code)
    cdef FINT setanndesc(int annotation_code, char *annotation_description)
    cdef FVOID iannclose(WFDB_Annotator a)
    cdef FVOID oannclose(WFDB_Annotator a)
    cdef FSTRING timstr(WFDB_Time t)
    cdef FSTRING mstimstr(WFDB_Time t)
    cdef FSITIME strtim(char *time_string)
    cdef FSTRING datstr(WFDB_Date d)
    cdef FDATE strdat(char *date_string)
    cdef FINT adumuv(WFDB_Signal s, WFDB_Sample a)
    cdef FSAMPLE muvadu(WFDB_Signal s, int microvolts)
    cdef FDOUBLE aduphys(WFDB_Signal s, WFDB_Sample a)
    cdef FSAMPLE physadu(WFDB_Signal s, double v)
    cdef FSAMPLE sample(WFDB_Signal s, WFDB_Time t)
    cdef FINT sample_valid()
    cdef FINT calopen(char *calibration_filename)
    cdef FINT getcal(char *description, char *units, WFDB_Calinfo *cal)
    cdef FINT putcal(WFDB_Calinfo *cal)
    cdef FINT newcal(char *calibration_filename)
    cdef FVOID flushcal()
    cdef FSTRING getinfo(char *record)
    cdef FINT putinfo(char *info)
    cdef FINT newheader(char *record)
    cdef FINT setheader(char *record, WFDB_Siginfo *siarray, unsigned int nsig)
    cdef FINT setmsheader(char *record, char **segnames, unsigned int nsegments)
    cdef FINT wfdbgetskew(WFDB_Signal s)
    cdef FVOID wfdbsetskew(WFDB_Signal s, int skew)
    cdef FLONGINT wfdbgetstart(WFDB_Signal s)
    cdef FVOID wfdbsetstart(WFDB_Signal s, long bytes)
    cdef FVOID wfdbquit()
    cdef FFREQUENCY sampfreq(char *record)
    cdef FINT setsampfreq(WFDB_Frequency sampling_frequency)
    cdef FFREQUENCY getcfreq()
    cdef FVOID setcfreq(WFDB_Frequency counter_frequency)
    cdef FDOUBLE getbasecount()
    cdef FVOID setbasecount(double count)
    cdef FINT setbasetime(char *time_string)
    cdef FVOID wfdbquiet()
    cdef FVOID wfdbverbose()
    cdef FSTRING wfdberror()
    cdef FVOID setwfdb(char *database_path_string)
    cdef FSTRING getwfdb()
    cdef FINT setibsize(int input_buffer_size)
    cdef FINT setobsize(int output_buffer_size)
    cdef FSTRING wfdbfile(char *file_type, char *record)
    cdef FVOID wfdbflush() 

    #/* WFDB_anninfo '.stat' values */
    cdef enum:
        WFDB_READ      = 0   #/* standard input annotation file */
        WFDB_WRITE     = 1   #/* standard output annotation file */
        WFDB_AHA_READ  = 2   #/* AHA-format input annotation file */
        WFDB_AHA_WRITE = 3   #/* AHA-format output annotation file */

cdef enum:
    WFDB_DEFFREQ   = 250  #/* default sampling frequency (Hz) */
    WFDB_DEFGAIN   = 200  #/* default value for gain (adu/physical unit) */
    WFDB_DEFRES    = 12     #/* default value for ADC resolution (bits) */ 

