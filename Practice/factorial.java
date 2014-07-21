import java.util.Scanner;

public class factorial{
	public static void main(String[] args){
		Scanner scan = new Scanner(System.in);
		System.out.println("Num");
		int inp = scan.nextInt();

		System.out.print(factorial(inp));
		System.out.println();
	}
	public static int factorial(int input){
		int output = 1; 
		for(int i = 1; i <= input  ; i++){
			output *= i;
		}
		return output;
	}
}