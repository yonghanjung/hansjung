package DrM_Peak;

import static org.junit.Assert.*;

import org.junit.Test;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import org.junit.Before;

public class TestDetectPeak {
	PeakDetect det;
	
	@Before
	public void setUp() throws Exception {
		det = new PeakDetect();
	}
	
	@Test
	public void test1() {
		List<Double> values = new ArrayList<Double>();
		values.add(9.0);
		values.add(10.0);
		values.add(11.0);
		values.add(5.0);
		Map<Integer, Double> result = det.peak_detection(values);
		
		assertTrue(result.size() == 1);
		for (Entry<Integer, Double> entry : result.entrySet()) {
			assertTrue(entry.getKey() == 3);
			assertTrue(entry.getValue() == 11);
		}

	}
	
	@Test
	public void test2() {
		List<Double> values = new ArrayList<Double>();
		//values.add(5.0);
		values.add(9.0);
		values.add(8.0);
		values.add(7.0);
		values.add(6.0);
		Map<Integer, Double> result = det.peak_detection(values);
		
		assertTrue(result.size() == 1);
		for (Entry<Integer, Double> entry : result.entrySet()) {
			assertTrue(entry.getKey() == 1);
			assertTrue(entry.getValue() == 9);
		}

	}
	
	@Test
	public void test3() {
		List<Double> values = new ArrayList<Double>();
		values.add(5.0);
		values.add(6.0);
		values.add(7.0);
		values.add(8.0);
		values.add(9.0);
		Map<Integer, Double> result = det.peak_detection(values);
		
		assertTrue(result.size() == 1);
		for (Entry<Integer, Double> entry : result.entrySet()) {
			assertTrue(entry.getKey() == 5);
			assertTrue(entry.getValue() == 9);
		}

	}
	
	@Test
	public void test4() {
		List<Double> values = new ArrayList<Double>();
		//values.add(5.0);
		values.add(9.0);
		values.add(8.0);
		values.add(7.0);
		values.add(6.0);
		values.add(9.0);
		values.add(8.0);
		values.add(7.0);
		values.add(6.0);
		Map<Integer, Double> result = det.peak_detection(values);
		
		assertTrue(result.size() == 2);
		for (Entry<Integer, Double> entry : result.entrySet()) {
			assertTrue(entry.getValue() == 9);
		}

	}
	
	@Test
	public void test5() {
		List<Double> values = new ArrayList<Double>();
		values.add(5.0);
		values.add(6.0);
		values.add(7.0);
		values.add(8.0);
		values.add(9.0);
		values.add(5.0);
		values.add(6.0);
		values.add(7.0);
		values.add(8.0);
		values.add(9.0);
		Map<Integer, Double> result = det.peak_detection(values);
		
		assertTrue(result.size() == 2);
		for (Entry<Integer, Double> entry : result.entrySet()) {
			assertTrue(entry.getValue() == 9);
		}

	}
	
	@Test
	public void test6() {
		List<Double> values = new ArrayList<Double>();
		values.add(5.0);
		values.add(8.0);
		values.add(6.0);
		values.add(7.0);
		values.add(8.0);
		values.add(9.0);
		values.add(5.0);
		values.add(8.0);
		values.add(6.0);
		values.add(7.0);
		values.add(8.0);
		values.add(9.0);
		values.add(5.0);
		values.add(9.0);
		values.add(6.0);
		Map<Integer, Double> result = det.peak_detection(values);
		
		assertTrue(result.size() == 5);
	}

}
