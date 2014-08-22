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
        List<Double> adap = new ArrayList<Double>();
        adap.add(thr_old);
        String mode = "thr";
        boolean cross = false;
        int adap_it = 0;
        double prev_thr = 0.0;
        double cur_thr = 0.0;
        double prev_sig = 0.0;
        double cur_sig = 0.0;

        /* Peak Detection Start */
        for (int idx = 0; idx < mysignal.size(); idx ++){
            if (idx > 0){
                prev_thr = adap.get(adap.size() - 2);
                cur_thr = adap.get(adap.size() - 1);
                prev_sig = mysignal.get(idx - 1);
                cur_sig = mysignal.get(idx);
                cross = check_cross(prev_thr, prev_sig, cur_thr, cur_sig);
            }
            else{

            }

            if (mode == "thr"){
                if (cross == false){
                    mode = "thr";
                    thr_new = adap.get(adap_it) + (Sr * ((Vpeak + StdPPG) / Fs));
                    adap_it += 1;
                    adap.add(thr_new);
                }
                else if (cross == true){
                    mode = "sig";
                    adap.add(cur_sig);
                    adap_it += 1;
                    continue;
                }
            }

            else if (mode == "sig"){
                if (cur_sig > prev_sig){
                    adap.add(cur_sig);
                    adap_it += 1;
                }
                else if (cur_sig < prev_sig){
                    adap.add(cur_sig);
                    adap_it += 1;
                    mode = "thr";
                    max_detect.put(idx,prev_sig);
                    Vpeak = prev_sig;
                    continue;
                }
            }
        }

        return max_detect;
    }

    List<Double> adap() {
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
        List<Double> adap = new ArrayList<Double>();
        adap.add(thr_old);
        String mode = "thr";
        boolean cross = false;
        int adap_it = 0;
        double prev_thr = 0.0;
        double cur_thr = 0.0;
        double prev_sig = 0.0;
        double cur_sig = 0.0;

        /* Peak Detection Start */
        for (int idx = 0; idx < mysignal.size(); idx++) {
            if (idx > 0) {
                prev_thr = adap.get(adap.size() - 2);
                cur_thr = adap.get(adap.size() - 1);
                prev_sig = mysignal.get(idx - 1);
                cur_sig = mysignal.get(idx);
                cross = check_cross(prev_thr, prev_sig, cur_thr, cur_sig);
            } else {

            }

            if (mode == "thr") {
                if (cross == false) {
                    mode = "thr";
                    thr_new = adap.get(adap_it) + (Sr * ((Vpeak + StdPPG) / Fs));
                    adap_it += 1;
                    adap.add(thr_new);
                } else if (cross == true) {
                    mode = "sig";
                    adap.add(cur_sig);
                    adap_it += 1;
                    continue;
                }
            } else if (mode == "sig") {
                if (cur_sig > prev_sig) {
                    adap.add(cur_sig);
                    adap_it += 1;
                } else if (cur_sig < prev_sig) {
                    adap.add(cur_sig);
                    adap_it += 1;
                    mode = "thr";
                    max_detect.put(idx, prev_sig);
                    Vpeak = prev_sig;
                    continue;
                }
            }
        }

        return adap;
    }

}
