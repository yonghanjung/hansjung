package DrM_Peak;

import java.util.List;
import java.util.Map;
import java.util.HashMap;


public class PeakDetect {

	public Map<Integer, Double> peak_detection(List<Double> values) {

		Map<Integer, Double> maxima = new HashMap<Integer, Double>();

		boolean lookForMax = true;
		double cur, next, prev;
		int tempcur; 
		int tempprev = 1; 
		int tempdif;
		
		statistics mystat = new statistics(values);
		double mymean = mystat.getMean();
		double mystd = mystat.getStdDev();
		//double thres = mymean + mystd;
		double thres = 160;
		int widththres = 50;

		if (values.size() > 1) {
			for (int pos = 0; pos < values.size() - 1; pos++) {
				cur = values.get(pos);
				next = values.get(pos + 1);
				if (lookForMax) {
					if (cur > next) {
						lookForMax = false;
						if (cur > thres) // To test, remove this condition
							if (maxima.size() == 0){
								maxima.put(pos + 1, cur);
								tempprev = pos+1; 
							}
							else{
								tempcur = pos+1; 
								tempdif = tempcur - tempprev; 
								tempprev = tempcur; 

								if (tempdif > widththres)
									maxima.put(pos+1, cur);
							}

					}
				} else {
					if (cur < next) {
						lookForMax = true;
					}
				}
			}
			cur = values.get(values.size() - 1); 
			prev = values.get(values.size() - 2);
			if (cur > prev && cur > mymean+mystd)
				maxima.put(values.size(), (double) cur);
		} else
			maxima.put(1, values.get(0));

		return maxima;
	}	
}