public class fibo{
	public static void main(String[] args){
		int[] test = new int[5];
		for(int i = 0; i < 5; i++){
			test[i] = i+1;
		}

		for (int i = 0; i < 5; i++){
			System.out.print(test[i]);
			System.out.print('\n');
		}

		System.out.println();
	}
}