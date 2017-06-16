package summerofcode;

/**
 *
 * @author Anton Dil
 */
public class Day3
{
   static final String pass = "the traveller in the grey riding-coat, who called himself mr. melville, was contemplating the malice of which the gods are capable.";

   public static void main(String[] args)
   {
      part1();
      System.out.println("\n PART 2 ");
      part2();
   }

   static void part2()
   {
      int[] newcode =
      {
         ci('r'), ci('i')
      };

      final int alpha = 5, beta = 11;

      System.out.printf("newcode %d %d %n", newcode[0], newcode[1]);

      for (int i = 0; i < pass.length(); i++)
      {
         char nextCh = pass.charAt(i);

         if (nextCh >= 'a' && nextCh <= 'z')
         {
            newcode[0] = wrap2(newcode[0] + alpha * newcode[1]);
            newcode[1] = wrap2(newcode[1] + beta * ci(nextCh));

            System.out.printf("nextchar %c newcode %c %c %n", nextCh, ic(newcode[0]), ic(newcode[1]));
         } //else skip this char

      }
   }

   static void part1()
   {
      //assuming string length > 1
      int[] oldcode =
      {
         ci(pass.charAt(0)), ci(pass.charAt(1))
      };

      System.out.printf("oldcode %d %d %n", oldcode[0], oldcode[1]);

      for (int i = 2; i < pass.length(); i++)
      {
         char nextCh = pass.charAt(i);

         if (nextCh >= 'a' && nextCh <= 'z')
         {
            //System.out.printf(" next char %c %d %n", nextCh, ci(nextCh));
            oldcode[0] = wrap(oldcode[0] + oldcode[1]);
            oldcode[1] = wrap(oldcode[1] + ci(nextCh));

            System.out.printf("next char %c oldcode %c %c %n", nextCh, ic(oldcode[0]), ic(oldcode[1]));
         } //else skip this char

      }
   }

   //char conversion to int scale, 1-based
   static int ci(char c)
   {
      return c - 'a' + 1;
   }

   //for readability, the int in char form
   static char ic(int x)
   {
      return (char) (x + 'a' - 1);
   }

   //oldwrap only needed adjustment by 26
   static int wrap(int x)
   {
      if (x > 26)
      {
         return x - 26;
      }

      return x;
   }

   //new wrap needs a modulus
   static int wrap2(int x)
   {
      if (x > 26)
      {
         return (x - 1) % 26 + 1;
      }

      return x;
   }

}
