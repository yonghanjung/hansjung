import java.util.*;

/**
 * Created by jeong-yonghan on 9/3/14.
 */
public class batch_peak {
    // 글로벌 변수부터 만들자 (인풋)
    List<Double> orig_signal;
    int size;

    // 그 다음에 생성자를 만들자
    public batch_peak(List<Double>orig_signal){
        this.orig_signal = orig_signal;
        size = orig_signal.size();
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

    List<Integer>GetKey( Map<Integer, Double> PeakLoc   ){
        List<Integer>KeyList = new ArrayList<Integer>();

        for (Integer key : PeakLoc.keySet()){
            KeyList.add(key);
        }

        return KeyList;
    }


    Map<Integer, Double> peak_detection( List<Double> batch_signal   , int Fs, double StdPPG, double thr_old , double Sr, double refract, double Vpeak ) {
        Map<Integer, Double> max_detect = new HashMap<Integer, Double>();

        double cur_loc = 0;
        double prev_loc = 0;
        double thr_new = 0;


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
                cur_thr = adap.get(idx - 1) + (Sr * ((Vpeak + StdPPG) / Fs));
                prev_sig = batch_signal.get(idx - 1);
                cur_sig = batch_signal.get(idx);
                cross = check_cross(prev_thr, prev_sig, cur_thr, cur_sig);
            } else {

            }

            if (mode == "thr") {
                if (cross == false) {
                    mode = "thr";
                    if (idx == 0) {
                        thr_new = thr_old + (Sr * ((Vpeak + StdPPG) / Fs));
                    } else {
                        thr_new = adap.get(idx - 1) + (Sr * ((Vpeak + StdPPG) / Fs));
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
                    Double new_thr = prev_sig + (Sr * ((Vpeak + StdPPG) / Fs));
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

    Map<Integer, Double> batch_peak_detect(int bat_sec){
        int Fs = 75;
        int bat_idx = bat_sec * Fs;
        int bat_iter = 0;
        double Sr = -0.3;
        double refract = 1.0;
        int starting_idx = 0;
        Map<Integer, Double> new_max = new HashMap<Integer, Double>();
        int old_break_num = 0;
        int new_break_num = 0;
        double bat_start = 0;
        double Vpeak = 0;
        List<Integer> RR_locs = new ArrayList<Integer>(); // 얘는 RR idx 위치만 잡음
        List<Double> RR_interval = new ArrayList<Double>(); // Real RR Interval




        while (true){
            List<Double>bat_signal = new ArrayList<Double>();
            old_break_num = new_max.size();

            if (bat_iter == 0){
                for(int idx = 0; idx < bat_idx; idx ++){
                    bat_signal.add(orig_signal.get(idx));
                }
            }
            else{
                List<Integer> new_max_key = GetKey(new_max);
                starting_idx = Collections.max(new_max_key);

                for(int idx = starting_idx; idx < starting_idx + bat_idx; idx ++ ){
                    bat_signal.add(orig_signal.get(idx));
                }
            }
            statistics mystat = new statistics(bat_signal);
            double StdPPG = mystat.getStdDev();

            if (bat_iter == 0){
                bat_start = 0.5 * Collections.max(bat_signal);
                Vpeak = 0;
            }
            else{
                bat_start = bat_signal.get(0);
                Vpeak = bat_start;
            }

            Map<Integer, Double>peak_detect =  peak_detection(bat_signal,Fs,StdPPG,bat_start, Sr, refract, Vpeak);
            Map<Integer, Double>new_peak = new HashMap<Integer, Double>();

            for(Integer key : peak_detect.keySet()){
                new_peak.put( key + starting_idx, peak_detect.get(key)    );
            }

            List<Integer>get_new_peak_key = GetKey(new_peak);
            Collections.sort(get_new_peak_key);
            List<Integer> big_temp = new ArrayList<Integer>();
            List<Integer> small_temp = new ArrayList<Integer>();

            if (bat_iter > 0){
                if (get_new_peak_key.size()>0){
                    RR_locs.add(get_new_peak_key.get(0) - starting_idx);
                }
            }

            if (get_new_peak_key.size() > 0) {
                for (int i = 1; i < get_new_peak_key.size(); i++) {
                    big_temp.add(get_new_peak_key.get(i));
                }

                for (int i = 0; i < get_new_peak_key.size()-1; i++) {
                    small_temp.add(get_new_peak_key.get(i));
                }

                for (int i = 0 ; i < get_new_peak_key.size() -1; i++){
                    RR_locs.add( big_temp.get(i) - small_temp.get(i)      );
                }
            }

            for (int i = 0; i < RR_locs.size(); i++){
                RR_interval.add( (double) RR_locs.get(i) / 75    );
            }


            for (Integer key : new_peak.keySet()){
                new_max.put( key, new_peak.get(key)    );
            }

            bat_iter += 1;

            new_break_num = new_max.size();

            if (old_break_num == new_break_num){
                break;
            }

        }

        return new_max;


    }

}
