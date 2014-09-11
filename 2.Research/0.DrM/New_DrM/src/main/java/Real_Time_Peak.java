import java.util.*;

/**
 * Created by jeong-yonghan on 9/11/14.
 */
public class Real_Time_Peak {
    List<Double> train_signal ;
    int size;
    double stdPPG;

    // Construct

    public Real_Time_Peak(List<Double> train_siganl){
        statistics mystat = new statistics(train_siganl);
        stdPPG = mystat.getStdDev();
        this.stdPPG = stdPPG;
        this.train_signal = train_siganl;
        size = train_siganl.size();
    }

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

    Map<Integer, Double> peak_detection( List<Double> batch_signal , int Fs) {
        Map<Integer, Double> max_detect = new HashMap<Integer, Double>();

        double Vpeak = 0;
        double thr_old = 0.5 * Collections.max(batch_signal);
        double cur_loc = 0;
        double prev_loc = 0;
        double thr_new = 0;
        double Sr = -0.6;
        double refract = -0.5;


        /* ------ */

        /* Initial Setting for Peak detection */
        Map<Integer, Double> adap = new HashMap<Integer, Double>();
        String mode = "thr";
        boolean cross = false;

        double prev_thr = 0.0;
        double cur_thr = 0.0;
        double prev_sig = 0.0;
        double cur_sig = 0.0;

        /* Peak Detection Start */
        for (int idx = 0; idx < batch_signal.size(); idx++) {
            if (idx > 0) {
                prev_thr = adap.get(idx - 1);
                cur_thr = adap.get(idx - 1) + (Sr * ((Vpeak + stdPPG) / Fs));
                prev_sig = batch_signal.get(idx - 1);
                cur_sig = batch_signal.get(idx);
                cross = check_cross(prev_thr, prev_sig, cur_thr, cur_sig);
            } else {

            }

            if (mode == "thr") {
                if (cross == false) {
                    mode = "thr";
                    if (idx == 0) {
                        thr_new = thr_old + (Sr * ((Vpeak + stdPPG) / Fs));
                    } else {
                        thr_new = adap.get(idx - 1) + (Sr * ((Vpeak + stdPPG) / Fs));
                    }
                    adap.put(idx, thr_new);
                } else if (cross == true) {
                    if (prev_loc != 0) {
                        if (idx - prev_loc < refract * Fs) {
                            mode = "thr";
                        } else {
                            mode = "sig";
                        }
                    } else {
                        mode = "sig";
                    }
                    adap.put(idx, cur_sig);
                    continue;
                }
            } else if (mode == "sig") {
                if (cur_sig >= prev_sig) {
                    adap.put(idx, cur_sig);
                } else {
                    prev_loc = cur_loc;
                    cur_loc = idx - 1;
                    Double new_thr = prev_sig + (Sr * ((Vpeak + stdPPG) / Fs));
                    adap.put(idx, new_thr);
                    mode = "thr";
                    max_detect.put(idx, prev_sig);
                    Vpeak = prev_sig;
                    continue;
                }
            }
        }

        return max_detect;
    }

    /*
        1: peak
        0 : increasing
        -1 : decreasing
     */
    int saddle(double prev, double cur, double next){
        if (prev < cur){
            if (next <= cur) {
                return 1;
            }
            else{
                return 0;
            }
        }
        else{
            return -1;
        }
    }

    List<Double> list_difference(List<Double> mysignal ){
        List<Double> temp1 = new ArrayList<Double>();
        List<Double> temp2 = new ArrayList<Double>();
        List<Double> temp3 = new ArrayList<Double>();

        for(int idx = 0; idx < mysignal.size()-1; idx ++){
            temp1.add(mysignal.get(idx));
        }

        for (int idx = 1; idx < mysignal.size(); idx ++){
            temp2.add(mysignal.get(idx));
        }

        for (int idx = 0; idx < temp1.size(); idx ++){
            double temp = temp2.get(idx) - temp1.get(idx);
            temp3.add( temp   );
        }
        return temp3;
    }

    double SSF(List<Double> window){
        List<Double> list_diff = list_difference(window);
        List<Double> temp = new ArrayList<Double>();

        for (double a : list_diff){
            if (a > 0){
                temp.add(a);
            }
        }

        double answer_sum = 0;

        for (double a : temp){
            answer_sum += a;
        }
        return answer_sum;
    }

    List<Double>SSF_newsignal(List<Double>train_signal, int window_size){
        int rem_size = train_signal.size();
        for (int idx = 0; idx < window_size; idx ++) {
            train_signal.add((double)0);
        }
        List<Double>new_signal = new ArrayList<Double>();
        for (int idx = 0; idx < rem_size; idx++){
            List<Double>temp = new ArrayList<Double>();
            for (int i = idx; i < window_size; i++){
                temp.add(train_signal.get(i));
            }
            new_signal.add(SSF(temp));
        }
        return new_signal;
    }

    double down_threshold(List<Double> train_signal, int window_size ){
        List<Double>SSF_train = SSF_newsignal(train_signal, window_size);
        Map<Integer, Double> mypeak = peak_detection(SSF_train, 75);

        double avg = 0;
        for (double a  : mypeak.values()){
            avg += a;
        }
        avg = avg / mypeak.values().size();
        avg = avg / 2;
        return avg ;

    }

    Map<Integer, Double> real_time_peak(List<Double>test_signal){
        int Fs = 75;
        int sec = 3;
        int window_size = 10;

        List<Double> temp1_window = new ArrayList<Double>();
        List<Double> temp2_window = new ArrayList<Double>();
        double down_thres = down_threshold(train_signal,window_size);

        for (int idx = train_signal.size() - 1 - window_size; idx < train_signal.size(); idx ++){
            temp1_window.add(train_signal.get(idx));
        }
        for (int idx = train_signal.size() - 2 - window_size; idx < train_signal.size()-1; idx++){
            temp2_window.add(train_signal.get(idx));
        }

        double prev = SSF(temp2_window);
        double cur = SSF(temp1_window);
        List<Double> window = temp1_window;

        Map<Integer, Double> mypeak_test = new HashMap<Integer, Double>();
        Map<Integer, Double> mypeak_SSF = new HashMap<Integer, Double>();

        for (int idx = 0; idx < test_signal.size(); idx ++){
            window.add(test_signal.get(idx));
            window.remove(0);
            double next = SSF(window);

            if (saddle(prev,cur,next) == 1){
                if (cur > down_thres){
                    mypeak_test.put(idx, test_signal.get(idx));
                    mypeak_SSF.put(idx - window_size, cur);
                }
            }

            prev = cur;
            cur = next;

        }

        return mypeak_test;
    }

}
