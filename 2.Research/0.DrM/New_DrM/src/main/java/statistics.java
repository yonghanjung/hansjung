import java.util.List;

public class statistics {
    List <Double> data;
    double size;

    public statistics(List<Double> data){
        this.data = data;
        size = data.size();
    }

    double getMean()
    {
        double sum = 0.0;
        for(double a : data)
            sum += a;
        return sum/size;
    }

    double getVariance()
    {
        double mean = getMean();
        double temp = 0;
        for(double a :data)
            temp += (mean-a)*(mean-a);
        return temp/size;
    }

    double getStdDev()
    {
        return Math.sqrt(getVariance());
    }

    double getRMS()
    {
        double ms = 0;
        for (double a : data)
            ms += a*a;
        ms /= size;
        return Math.sqrt(ms);
    }

}
