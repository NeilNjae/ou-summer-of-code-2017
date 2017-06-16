/*
 * Day 1 parts 1 and 2
 */
package summerofcode;

import java.io.FileReader;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

/**
 *
 * @author Anton Dil
 */
public class Day1
{
   private final static Map<String,Double> scores = new HashMap<>();
   
   static
   {
      scores.put("Almaty", 2.0);
      scores.put("Brorfelde", 0.9);
      scores.put("Estacada", 0.4);
      scores.put("Jayuya", 0.6);
      scores.put("Karlukovo", 2.2);
      scores.put("Morgantown", 2.9);
      scores.put("Nordkapp", 1.5);
      scores.put("Nullarbor", 2.2);
      scores.put("Puente-Laguna-Garzonkuala-Penyu", 0.4);
      scores.put("Uzupis", 0.9);
   }
   
   public static void main(String[] args) throws Exception
   { 
      Scanner sc = new Scanner(new FileReader("01-holidays.txt"));  
      
      String id, loc, bestId = "";
      double value, score;
      double bestValue = 0;      
      int price, days;      
      int afford = 0;
      
      while(sc.hasNext())
      {
         id = sc.next();         
         price = sc.nextInt();         
         loc = sc.next();        
         days = sc.nextInt(); 
         
         if(scores.get(loc) != null)
         {
            score = scores.get(loc);
         }
         else
         {
            score = 1.0;
         }
      
         //only consider holidays we can afford        
         if(price <= 1200)
         {                     
            value = score * days/price;   
         
            System.out.printf("%s %d %s %d value %.5f %n", id, price, loc, days, value);
            afford++;
            
            if(value > bestValue)
            {
               bestValue = value;
               bestId = id;
            }
         }
      }      

      System.out.println("Affordable " + afford);
      System.out.printf("Best value is id %s with value %f%n", bestId, bestValue);
   }
}
