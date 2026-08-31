import tio.*;

class miv8cycle1 {
  public static void main(String[] args) {

    int inputNumber; 
    double a;
    
    while (1) {

      inputNumber = Console.in.readInt();
     
      if (inputNumber==0) continue;
      
      a = (double)1/inputNumber;
      System.out.println("1/" + inputNumber + " = " + a);
      if  (inputNumber < 0) break;
      

    }
    
  }    
}
