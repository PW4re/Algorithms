import java.util.*;

public class PathSearcher {
    private final HashMap<Integer, String> intCoordinates;
    private final int horizontalKnight, verticalKnight, horizontalPawn, verticalPawn;
    int[] forbiddenHorizontals;
    int forbiddenVertical;


    public PathSearcher(String pawnCoordinates, String knightCoordinates){
        HashMap<Character, Integer> stringCoordinates = new HashMap<>() {{
            put('a', 1);
            put('b', 2);
            put('c', 3);
            put('d', 4);
            put('e', 5);
            put('f', 6);
            put('g', 7);
            put('h', 8);
        }};
        intCoordinates = new HashMap<>(){{
            put(1, "a");
            put(2, "b");
            put(3, "c");
            put(4, "d");
            put(5, "e");
            put(6, "f");
            put(7, "g");
            put(8, "h");
        }};
        horizontalKnight = stringCoordinates.get(knightCoordinates.charAt(0));
        verticalKnight = knightCoordinates.charAt(1) - '0';
        horizontalPawn = stringCoordinates.get(pawnCoordinates.charAt(0));
        verticalPawn = pawnCoordinates.charAt(1) - '0';
        findForbiddenCoordinates();
    }

    public ArrayList<String> searchPath() {
        ArrayList<String> result = new ArrayList<>();
        for (Cell cell : search())
            result.add(intCoordinates.get(cell.horizontal) + cell.vertical);

        return result;
    }

    private ArrayList<Cell> getParentsChain(Cell cell){
        ArrayList<Cell> result = new ArrayList<>();
        Cell father = cell;
        while (father != null){
            result.add(father);
            father = father.father;
        }
        Collections.reverse(result);

        return result;
    }

    private ArrayList<Cell> search() {
        ArrayDeque<Cell> queue = new ArrayDeque<>();
        HashSet<Cell> visited = new HashSet<>();
        Cell knight = new Cell(horizontalKnight, verticalKnight, null);
        queue.add(knight);
        visited.add(knight);

        while (!queue.isEmpty()){
            for (Cell neighbor : getNeighbors(queue.peek())){
                if (neighbor == null) continue;
                if (neighbor.vertical == verticalPawn && neighbor.horizontal == horizontalPawn)
                    return getParentsChain(neighbor);
                if (!visited.contains(neighbor)) {
                    queue.add(neighbor);
                    visited.add(neighbor);
                }
            }

            queue.pop();
        }

        return new ArrayList<>();
    }

    // Фича: храним позицию как десятичное число с двумя разрядами.
    // В старшем разряде координаты по горизонтали, в младшем - по вертикали.
    private void findForbiddenCoordinates(){
        int leftHor = horizontalPawn - 1;
        int rightHor = horizontalPawn + 1;
        int vert = verticalPawn - 1;
        if (vert < 1 || leftHor < 1 && rightHor > 8) {
            forbiddenHorizontals = new int[0];
            forbiddenVertical = 0;
            return;
        }
        forbiddenVertical = vert;
        if (leftHor < 1) forbiddenHorizontals = new int[] { rightHor };
        else if (rightHor > 8) forbiddenHorizontals = new int[] { leftHor };
        else forbiddenHorizontals = new int[] { leftHor, rightHor };
    }

    private Cell[] getNeighbors(Cell cell) {
        return new Cell[]{
                getValidatedNeighbor(cell.horizontal + 1, cell.vertical + 2, cell),
                getValidatedNeighbor(cell.horizontal - 1, cell.vertical + 2, cell),
                getValidatedNeighbor(cell.horizontal - 2, cell.vertical + 1, cell),
                getValidatedNeighbor(cell.horizontal - 2, cell.vertical - 1, cell),
                getValidatedNeighbor(cell.horizontal - 1, cell.vertical - 2, cell),
                getValidatedNeighbor(cell.horizontal + 1, cell.vertical - 2, cell),
                getValidatedNeighbor(cell.horizontal + 2, cell.vertical - 1, cell),
                getValidatedNeighbor(cell.horizontal + 2, cell.vertical + 1, cell)
        };
    }

    private Cell getValidatedNeighbor(int horizontal, int vertical, Cell father){
        if ((horizontal <= 8 && horizontal >= 1) &&
                (vertical <= 8 && vertical >= 1) &&
                ((forbiddenHorizontals[0] != horizontal || forbiddenHorizontals[1] != horizontal)
                && vertical != forbiddenVertical))
            return new Cell(horizontal, vertical, father);
        return null;
    }


    private class Cell {
        private final int horizontal;
        private final int vertical;
        private final Cell father;

        private Cell(int horizontal, int vertical, Cell father){
            this.horizontal = horizontal;
            this.vertical   = vertical;
            this.father     = father;
        }
    }
}
