package summerofcode;

import java.io.FileReader;
import java.util.Scanner;

/**
 *
 * @author Anton Dil
 */
public class Day0
{
   public static void main(String[] args) throws Exception
   {  
      Scanner sc = new Scanner(new FileReader("00-prices.txt"));  
      
      String id, loc, bestId = "";
      int nullarbor = 0;
      int price, extras, nextCost;      
      int bestCost = Integer.MAX_VALUE;
      
      while(sc.hasNext())
      {
         id = sc.next();         
         price = sc.nextInt();         
         loc = sc.next();        
         extras = sc.nextInt();         
                  
         if(loc.contains("Nullarbor"))
            nullarbor++;
         
         nextCost = price + extras - Math.min(extras, 500);         
         
         if(nextCost < bestCost)
         {
            bestCost = nextCost;         
            bestId = id;
         }
      }      
      
      System.out.println("Nullarbor holidays " + nullarbor);
      System.out.println("Best price holiday " + bestCost + " id " + bestId );
   }
   
}
