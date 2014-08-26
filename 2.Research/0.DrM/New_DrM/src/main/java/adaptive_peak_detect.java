import java.util.*;

/**
 * Created by jeong-yonghan on 8/22/14.
 */
public class adaptive_peak_detect {
    List<Double> mysignal;

    public adaptive_peak_detect(List<Double> mysignal) {
        this.mysignal = mysignal;
    }

    // public <Result Type> class name <input value>
    public boolean check_cross(double prev_thr, double prev_sig, double cur_thr, double cur_sig) {
        if (prev_thr > prev_sig) {
            if (cur_thr < cur_sig) {
                return true;
            } else {
                return false;
            }
        } else {
            return false;
        }
    }

    Map<Integer, Double> peak_detection() {
        Map<Integer, Double> max_detect = new HashMap<Integer, Double>();

        /* Call needed method */
        statistics mystat = new statistics(mysignal);

        /* Initial Setting for threshold */
        double Vpeak = 0.0;
        int Fs = 75;
        double StdPPG = mystat.getStdDev();
        Double thr_old = Collections.max(mysignal);
        double thr_new = 0.0;
        double Sr = -0.6;
        /* ------ */

        /* Initial Setting for Peak detection */
        Map<Integer ,Double> adap = new HashMap<Integer, Double>();
        String mode = "thr";
        boolean cross = false;

        double prev_thr = 0.0;
        double cur_thr = 0.0;
        double prev_sig = 0.0;
        double cur_sig = 0.0;

        /* Peak Detection Start */
        for (int idx = 0; idx < mysignal.size(); idx ++){
            if (idx > 0){
                prev_thr = adap.get(idx-1);
                cur_thr = adap.get(idx-1) + (Sr * ((Vpeak + StdPPG) / Fs));
                prev_sig = mysignal.get(idx - 1);
                cur_sig = mysignal.get(idx);
                cross = check_cross(prev_thr, prev_sig, cur_thr, cur_sig);
            }
            else{

            }

            if (mode == "thr"){
                if (cross == false){
                    mode = "thr";
                    if (idx == 0){
                        thr_new = thr_old + (Sr * (( Vpeak + StdPPG) / Fs));
                    }
                    else{
                        thr_new = adap.get(idx-1) + (Sr * ((Vpeak + StdPPG) / Fs));
                    }
                    adap.put(idx, thr_new);
                }
                else if (cross == true){
                    mode = "sig";
                    adap.put(idx, cur_sig);
                    continue;
                }
            }

            else if (mode == "sig"){
                if (cur_sig >= prev_sig){
                    adap.put(idx, cur_sig);
                }
                else {
                    Double new_thr = prev_sig + (Sr * (( Vpeak + StdPPG) / Fs));
                    adap.put(idx , new_thr);
                    mode = "thr";
                    max_detect.put(idx,prev_sig);
                    Vpeak = prev_sig;
                    continue;
                }
            }
        }

        return max_detect;
    }

    Map<Integer, Double> Myadap() {
        Map<Integer, Double> max_detect = new HashMap<Integer, Double>();

        /* Call needed method */
        statistics mystat = new statistics(mysignal);

        /* Initial Setting for threshold */
        double Vpeak = 0.0;
        int Fs = 75;
        double StdPPG = mystat.getStdDev();
        Double thr_old = Collections.max(mysignal);
        double thr_new = 0.0;
        double Sr = -0.6;
        /* ------ */

        /* Initial Setting for Peak detection */
        Map<Integer ,Double> adap = new HashMap<Integer, Double>();
        String mode = "thr";
        boolean cross = false;

        double prev_thr = 0.0;
        double cur_thr = 0.0;
        double prev_sig = 0.0;
        double cur_sig = 0.0;

        /* Peak Detection Start */
        for (int idx = 0; idx < mysignal.size(); idx ++){
            if (idx > 0){
                prev_thr = adap.get(idx-1);
                cur_thr = adap.get(idx-1) + (Sr * ((Vpeak + StdPPG) / Fs));
                prev_sig = mysignal.get(idx - 1);
                cur_sig = mysignal.get(idx);
                cross = check_cross(prev_thr, prev_sig, cur_thr, cur_sig);
            }
            else{

            }

            if (mode == "thr"){
                if (cross == false){
                    mode = "thr";
                    if (idx == 0){
                        thr_new = thr_old + (Sr * (( Vpeak + StdPPG) / Fs));
                    }
                    else{
                        thr_new = adap.get(idx-1) + (Sr * ((Vpeak + StdPPG) / Fs));
                    }
                    adap.put(idx, thr_new);
                }
                else if (cross == true){
                    mode = "sig";
                    adap.put(idx, cur_sig);
                    continue;
                }
            }

            else if (mode == "sig"){
                if (cur_sig >= prev_sig){
                    adap.put(idx, cur_sig);
                }
                else {
                    Double new_thr = prev_sig + (Sr * (( Vpeak + StdPPG) / Fs));
                    adap.put(idx , new_thr);
                    mode = "thr";
                    max_detect.put(idx,prev_sig);
                    Vpeak = prev_sig;
                    continue;
                }
            }
        }

        return adap;
    }

}
