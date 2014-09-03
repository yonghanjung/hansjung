import java.util.*;

public class Main {
    public static void main (String[] args){
        Map<Integer, Double> testmap = new HashMap<Integer, Double>();
        testmap.put(65,196.0);
        testmap.put(266,196.0);
        testmap.put(331,190.0);
        testmap.put(134,185.0);
        testmap.put(201,206.0);

        System.out.println("주어진 신호 : {locs, peaks} ");
        System.out.println(testmap);

        HRV hrv = new HRV(testmap);
        System.out.println("RR Interval 뽑기");
        System.out.println(hrv.RR_interval());
        List <Double> RR_time_interval = hrv.RR_interval();

        System.out.println("원하는구간만큼 쪼개기");
        System.out.println(hrv.Chunk(RR_time_interval,2));

        System.out.println("구간들 사이의 Mean NN");
        System.out.println(hrv.meanNN(RR_time_interval,2));

        System.out.println("구간들 사이의 std NN");
        System.out.println(hrv.stdNN(RR_time_interval, 2));

        List<Double> testlist = new ArrayList<Double>();
        for (int idx = 1; idx < 11; idx ++){
            testlist.add((double)idx);
        }
        statistics mystat = new statistics(testlist);
        System.out.println(mystat.getRMS());

        System.out.println("50ms 넘는 인터벌 비율");
        System.out.println(hrv.pNN50(RR_time_interval));

        System.out.println("SD1");
        System.out.println(hrv.PoinPlot_sd1(RR_time_interval,2));

        System.out.println("SD2");
        System.out.println(hrv.PoinPlot_sd2(RR_time_interval,2));



    }
}
