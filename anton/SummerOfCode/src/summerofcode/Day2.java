package summerofcode;

import java.io.FileReader;
import java.util.Scanner;

/**
 *
 * @author Anton Dil
 */
public class Day2
{
   public static void main(String[] args) throws Exception
   {
      Scanner sc = new Scanner(new FileReader("02-lifts.txt"));
      int exit = Integer.MIN_VALUE; //replaceable floor value
      String input = "";
      int floor = 0;

      while (sc.hasNext())
      {
         input = sc.next(); //just one line of input in fact
      }

      System.out.println("Input was " + input);

      for (char ch : input.toCharArray())
      {
         switch (ch)
         {
            case 'v':
               floor--;
               break;
            case '^':
               floor++;
               break;
            case '=':
               if (floor > exit)
               {
                  exit = floor;
               }
         }
      }

      System.out.printf("final floor %d, highest exit %d%n", floor, exit);
   }
}
