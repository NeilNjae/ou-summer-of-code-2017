import java.util.Scanner;
import java.util.Scanner.*;
import java.io.FileReader;
import java.io.FileReader.*;

public class Day0
{
   public static void main(String[] args) throws Exception
   {
      FileReader f = new FileReader("00-prices.txt");     
      Scanner sc = new Scanner(f);  
      
      String id, bestId = "";
      int nullarbor = 0;
      int price, extras, nextCost;      
      int bestCost = Integer.MAX_VALUE;
      
      while(sc.hasNext())
      {
         id = sc.next();
         
         price = sc.nextInt();
         
         String lo = sc.next();
         
         if(lo.contains("Nullarbor"))
            nullarbor++;
         
         extras = sc.nextInt();
         
         nextCost = price + extras;
         
         int savings = Math.min(extras, 500);
         
         nextCost -= savings;
         
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
