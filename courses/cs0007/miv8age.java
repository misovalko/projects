import tio.*;

class miv8age {
  public static void main(String[] args) {

    int years, days, seconds, hours, minutes;

    System.out.print("Please enter your age in years: ");
    years=Console.in.readInt();

    days=365*years;
    hours=24*days;
    minutes=60*hours;
    seconds=60*minutes;

    System.out.println("You have spent " + seconds + " seconds in this world.");
  }

}
