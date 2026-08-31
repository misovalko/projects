import tio.*;

class miv8average {
  public static void main(String[] args) {

    int inputNumber; 
    long sum=0;
    int count=0;
    boolean finished = false;

    while (!finished) {
      inputNumber = Console.in.readInt();
      if (inputNumber<0) 
        finished = true;
      else {
        sum += inputNumber;
        count++;
      }
    }
    if (count>0)  
      System.out.println("The average is " + (float)sum/count +"."); 
    
  }    
}
