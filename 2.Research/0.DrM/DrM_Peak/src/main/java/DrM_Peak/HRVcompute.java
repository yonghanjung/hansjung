package DrM_Peak;

import java.util.*;
import java.lang.Object;
import java.util.Collections;



public class HRVcompute {
	Map <Integer, Double> data;
	List <Integer> myinterval = new ArrayList<Integer>();
	
	public HRVcompute(Map <Integer, Double> data){
		this.data = data;
	}
	
	List<Integer> RRloc(){
		// RR Interval and sort 
		List <Integer> mykey = new ArrayList<Integer>();
		Object[] myarray = data.keySet().toArray();
		for (int i = 0; i < myarray.length; i++){
			mykey.add((Integer)myarray[i] );
		}
		Collections.sort(mykey);
		return mykey; 
	}
	
	List<Double> RRinterval(){
		List<Integer> RRlocation = RRloc();
		List<Integer> dummy1 = new ArrayList<Integer>();
		List<Integer> dummy2 = new ArrayList<Integer>();
		List<Double> myRRinterval = new ArrayList<Double>();
		
		for(int i = 1; i< RRlocation.size(); i++){
			dummy1.add(RRlocation.get(i));
		}
		
		for(int i = 0; i < RRlocation.size()-1 ; i++){
			dummy2. add(RRlocation.get(i));
		}
		
		for(int i = 0; i < RRlocation.size()-1; i++){
			int locsjump = dummy1.get(i) - dummy2.get(i);
			double locsMs = (double)locsjump;
			locsMs  = (locsMs / 75 ); 
			myRRinterval.add(locsMs);
		}
		
		return myRRinterval;
	}

	double RRmean(){
		List<Double> RRinterval = RRinterval();
		double sum = 0.0;
        for(double a : RRinterval)
            sum += a;
        return sum/RRinterval.size();
    }
	
	double RRvariance(){
		List<Double> RRinterval = RRinterval();
		double mean = RRmean();
        double temp = 0;
        for(double a :RRinterval)
            temp += (mean-a)*(mean-a);
        return temp/RRinterval.size();
	}
	
	double RRstd(){
		return Math.sqrt(RRvariance());
	}
	
	double RR_RMS(){
		List<Double> RRinterval = RRinterval();
		double temp = 0; 
		
		for(double a : RRinterval){
			temp += a * a;
		}
		temp = temp / RRinterval.size();
		return Math.sqrt(temp);
	}
		
}
	
