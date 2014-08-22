import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;

/**
 * Created by jeong-yonghan on 8/22/14.
 */
public class HRV {
    Map<Integer, Double> R_peak;

    public HRV(Map<Integer, Double> R_peak) {
        this.R_peak = R_peak;
    }

    List<Double> RR_interval() {
        List<Double> RR_time_interval = new ArrayList<Double>();
        List<Double> R_peak_loc = new ArrayList<Double>();

        List<Double> temp1_R_peak_loc = new ArrayList<Double>();
        List<Double> temp2_R_peak_loc = new ArrayList<Double>();

        List<Integer> Sorted_R_peak = new ArrayList(R_peak.keySet());
        Collections.sort(Sorted_R_peak);

        for (int idx = 0; idx < Sorted_R_peak.size(); idx++) {
            double loc = (double) Sorted_R_peak.get(idx);
            double time_loc = loc / 75;
            R_peak_loc.add(time_loc);
        }

        // A[:-1]
        for (int idx = 0; idx < R_peak_loc.size() - 1; idx++) {
            temp1_R_peak_loc.add(R_peak_loc.get(idx));
        }

        // A[1:]
        for (int idx = 1; idx < R_peak_loc.size(); idx++) {
            temp2_R_peak_loc.add(R_peak_loc.get(idx));
        }

        // RR_interval
        for (int idx = 0; idx < temp1_R_peak_loc.size(); idx++) {
            RR_time_interval.add(temp2_R_peak_loc.get(idx) - temp1_R_peak_loc.get(idx));
        }
        return RR_time_interval;
    }

    List<List<Double>> Chunk(List<Double> RR_time_interval, int cutnumber) {
        List<List<Double>> splited_RR_time_interval = new ArrayList<List<Double>>();

        if (cutnumber < 1) {
            cutnumber = 1;
        }

        for (int idx = 0; idx < RR_time_interval.size(); idx += cutnumber) {
            List<Double> temp = new ArrayList<Double>();
            int endit = 0;
            if (idx + cutnumber >= RR_time_interval.size()) {
                endit = RR_time_interval.size();
            } else {
                endit = idx + cutnumber;
            }

            for (int new_idx = idx; new_idx < endit; new_idx++) {
                temp.add(RR_time_interval.get(new_idx));
            }
            splited_RR_time_interval.add(temp);
        }

        return splited_RR_time_interval;
    }

    List<Double> meanNN(List<Double> RR_time_interval, int cutnumber) {
        List<List<Double>> splited_RR_time_interval = Chunk(RR_time_interval, cutnumber);
        List<Double> MymeanNN = new ArrayList<Double>();
        List<Double> temp = new ArrayList<Double>();

        for (int idx = 0; idx < splited_RR_time_interval.size(); idx++) {
            temp = splited_RR_time_interval.get(idx);
            statistics mystat = new statistics(temp);
            double mymean = mystat.getMean();
            MymeanNN.add(mymean);
        }

        return MymeanNN;
    }

    List<Double> stdNN(List<Double> RR_time_interval, int cutnumber) {
        List<List<Double>> splited_RR_time_interval = Chunk(RR_time_interval, cutnumber);
        List<Double> MystdNN = new ArrayList<Double>();
        List<Double> temp = new ArrayList<Double>();

        for (int idx = 0; idx < splited_RR_time_interval.size(); idx++) {
            temp = splited_RR_time_interval.get(idx);
            statistics mystat = new statistics(temp);
            double mymean = mystat.getStdDev();
            MystdNN.add(mymean);
        }

        return MystdNN;
    }


    List<Double> RMSNN(List<Double> RR_time_interval, int cutnumber) {
        List<List<Double>> splited_RR_time_interval = Chunk(RR_time_interval, cutnumber);
        List<Double> MyRMSNN = new ArrayList<Double>();
        List<Double> temp = new ArrayList<Double>();

        for (int idx = 0; idx < splited_RR_time_interval.size(); idx++) {
            temp = splited_RR_time_interval.get(idx);
            statistics mystat = new statistics(temp);
            double mymean = mystat.getRMS();
            MyRMSNN.add(mymean);
        }

        return MyRMSNN;
    }
}
