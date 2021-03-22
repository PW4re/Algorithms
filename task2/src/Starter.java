import java.io.*;

public class Starter {
    public static void main(String[] args) {
        try (BufferedReader reader = new BufferedReader(new FileReader("in.txt"))) {
            String knightCoordinates = reader.readLine();
            String pawnCoordinates = reader.readLine();
            PathSearcher searcher = new PathSearcher(pawnCoordinates, knightCoordinates);
            writeResult(searcher.searchPath().toArray(new String[0]));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void writeResult(String[] result){
        try (FileWriter writer = new FileWriter("out.txt")) {
            for (String cell : result){
                writer.write(cell + "\n");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
