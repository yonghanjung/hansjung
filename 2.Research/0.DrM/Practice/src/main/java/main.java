import java.util.HashMap;
import java.util.Map;

/**
 * Created by jeong-yonghan on 8/26/14.
 */
public class main {
    public static void main(String args[]){
        Map<Integer, Double> Test_Map = new HashMap<Integer, Double>();
        Test_Map.put(3,1.0);
        Test_Map.put(4,2.0);

        System.out.println(Test_Map.get(4));
        System.out.println(Test_Map);
    }
}
