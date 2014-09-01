import java.util.ArrayList;
import java.util.List;

/**
 * Created by jeong-yonghan on 8/29/14.
 */
public class temp {
    int iter;
    int pound;
    List<Integer> coins = new ArrayList<Integer>();

    public temp (int pound){
        this.pound = pound;
        int cent = pound * 100;
    }

    int count_method(int left, int i, List<List<Integer>> comb, List<Integer> myadd){
        if (myadd.size() == 0){
            comb.add(myadd);
        }

        if (left == 0 || (i+1) == coins.size()) {
            if ((i + 1) == coins.size() && left > 0) {
                Integer coin = coins.get(i);
                List<Integer> temp = new ArrayList<Integer>();
                temp.add(left);
                temp.add(coin);
                comb.add(temp);
                i += 1;
            }

            while (i < coins.size()) {
                Integer coin = coins.get(i);
                List<Integer> temp = new ArrayList<Integer>();
                temp.add(0);
                temp.add(coin);
                comb.add(temp);
                i += 1;
            }

            return 1;
        }
        Integer cur = coins.get(i);

        for(int x = 0; x < (int)(left/cur)+1;  x++){
            List<Integer> temp = new ArrayList<Integer>();
            temp.add(x);
            temp.add(cur);
            count_method(left-x*cur, i+1, comb, temp );
        }

    }



}
