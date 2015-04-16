import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;

import java.io.FileInputStream;
import java.io.InputStream;
import java.util.HashMap;
import java.util.List;
import java.util.Map.Entry;
import java.util.Set;

/**
 * Created by andrew on 4/7/15.
 */
public class OptionCounter extends Wget2BaseListener {

    public HashMap<String, Integer> optionCounts = new HashMap<String, Integer>();
    public HashMap<OptPair, Integer> pairCounts = new HashMap<OptPair, Integer>();

    /**
     * Two option pairs should be equivalent even if the options are in different orders.
     */
    private class OptPair {

        public final String opt1;
        public final String opt2;

        public OptPair(String opt1, String opt2) {
            this.opt1 = opt1;
            this.opt2 = opt2;
        }

        public boolean equals(Object other) {
            if (other == null) return false;
            if (!(other instanceof OptPair)) return false;
            OptPair otherPair = (OptPair) other;
            if ((otherPair.opt1.equals(this.opt1) && otherPair.opt2.equals(this.opt2)) ||
                    (otherPair.opt2.equals(this.opt1) && otherPair.opt1.equals(this.opt2))) {
                return true;
            } else return false;
        }

        public int hashCode() {
            final int prime = 31;
            int result = 1;
            result = result + prime * ((opt1 == null) ? 0 : opt1.hashCode());
            result = result + prime * ((opt2 == null) ? 0 : opt2.hashCode());
            return result;
        }

    }

    public static void main(String [] args) throws Exception {

        String inputFile = null;
        if (args.length > 0) inputFile = args[0];
        InputStream is = System.in;
        if (inputFile != null) is = new FileInputStream(inputFile);

        Wget2Lexer lexer = new Wget2Lexer(new ANTLRInputStream(is));
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        Wget2Parser parser = new Wget2Parser(tokens);
        ParseTree tree = parser.lines();
        ParseTreeWalker walker = new ParseTreeWalker();
        OptionCounter counter = new OptionCounter();
        walker.walk(counter, tree);

        System.out.println("Option occurences");
        Set<Entry<String,Integer>> entries = counter.optionCounts.entrySet();
        for (Entry<String, Integer> entry : entries) {
            System.out.println(entry.getKey() + "\t" + entry.getValue());
        }

        System.out.println("Option Co-occurences");
        Set<Entry<OptPair,Integer>> pairCounts = counter.pairCounts.entrySet();
        for (Entry<OptPair, Integer> entry : pairCounts) {
            String opt1 = entry.getKey().opt1;
            String opt2 = entry.getKey().opt2;
            // Don't print out the co-occurences of an option with itself
            if (!opt1.equals(opt2)) {
                System.out.println(opt1 + "\t" + opt2 + "\t" + entry.getValue());
            };
        }

    }

    private String getOptString(Wget2Parser.OptionContext option) {
        String optionKey = null;
        if (option.SOPTAS() != null) optionKey = option.SOPTAS().getText();
        else if (option.SOPTSO() != null) optionKey = option.SOPTSO().getText();
        else if (option.LOPTAS() != null) optionKey = option.LOPTAS().getText();
        else if (option.LOPTSO() != null) optionKey = option.LOPTSO().getText();
        return optionKey;
    }

    public void exitLine(Wget2Parser.LineContext ctx) {

        // Count all option pairs on each line
        List<Wget2Parser.ChunkContext> chunkList = ctx.chunk();
        for (int i = 0; i < chunkList.size(); i++) {
            Wget2Parser.ChunkContext chunk = chunkList.get(i);
            if (chunk.option() != null) {
                for (int j = i; j < chunkList.size(); j++) {
                    Wget2Parser.ChunkContext chunk2 = chunkList.get(j);
                    if (chunk2.option() != null) {
                        OptPair pair = new OptPair(getOptString(chunk.option()), getOptString(chunk2.option()));
                        int pairCount;
                        if (!pairCounts.containsKey(pair)) pairCount = 1;
                        else pairCount = pairCounts.get(pair) + 1;
                        pairCounts.put(pair, pairCount);
                    }
                }
            }
        }

    }

    public void exitOption(Wget2Parser.OptionContext ctx) {
        String optionKey = getOptString(ctx);
        if (optionKey != null) {
            int count;
            if (!optionCounts.containsKey(optionKey)) count = 0;
            else count = optionCounts.get(optionKey);
            optionCounts.put(optionKey, count + 1);
        }
    }

}