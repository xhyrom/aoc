import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;

class Main {

    @FunctionalInterface
    interface Part {
        Object run();
    }

    private static void run(Part part, String name) {
        long start = System.nanoTime();
        Object result = part.run();
        long duration = System.nanoTime() - start;
        System.out.printf("%s (%d): %s%n", name, duration, result);
    }

    public static List<List<String>> grid(String fileName) {
        try (Stream<String> stream = Files.lines(Paths.get(fileName))) {
            return stream
                .map(line -> Arrays.asList(line.split("")))
                .collect(Collectors.toList());
        } catch (IOException e) {
            e.printStackTrace();
            return new ArrayList<>();
        }
    }

    public static void main(String[] args) {
        Part1 part1 = new Part1();
        Part2 part2 = new Part2();

        run(part1::run, "part_1");
        run(part2::run, "part_2");
    }
}

class Part1 {

    public Object run() {
        List<List<String>> grid = Main.grid("input.txt");
        Position start = findStart(grid);
        return calculatePath(grid, start).size();
    }

    protected Position findStart(List<List<String>> grid) {
        return grid
            .stream()
            .filter(row -> row.contains("^"))
            .map(row -> new Position(grid.indexOf(row), row.indexOf("^")))
            .findFirst()
            .orElseThrow(() -> new RuntimeException("No start position found!")
            );
    }

    protected Set<Position> calculatePath(
        List<List<String>> grid,
        Position start
    ) {
        Set<Position> seen = new HashSet<>();

        int r = start.row();
        int c = start.col();
        int dr = -1;
        int dc = 0;

        while (true) {
            seen.add(new Position(r, c));

            if (isOutOfBounds(grid, r + dr, c + dc)) {
                break;
            }

            if (grid.get(r + dr).get(c + dc).equals("#")) {
                int temp = dc;
                dc = -dr;
                dr = temp;
            } else {
                r += dr;
                c += dc;
            }
        }
        return seen;
    }

    protected boolean isOutOfBounds(List<List<String>> grid, int r, int c) {
        return r < 0 || r >= grid.size() || c < 0 || c >= grid.get(0).size();
    }
}

class Part2 extends Part1 {

    public Object run() {
        List<List<String>> grid = Main.grid("input.txt");
        Position start = findStart(grid);
        return findPossibleObstacles(grid, start).size();
    }

    private Set<Position> findPossibleObstacles(
        List<List<String>> grid,
        Position start
    ) {
        Set<Position> possibleObstacles = new HashSet<>();

        for (int r = 0; r < grid.size(); r++) {
            for (int c = 0; c < grid.get(0).size(); c++) {
                if (grid.get(r).get(c).equals(".")) {
                    Position obstaclePos = new Position(r, c);
                    if (createsLoop(grid, start, obstaclePos)) {
                        possibleObstacles.add(obstaclePos);
                    }
                }
            }
        }

        return possibleObstacles;
    }

    private boolean createsLoop(
        List<List<String>> originalGrid,
        Position start,
        Position obstacle
    ) {
        List<List<String>> grid = gridCopy(originalGrid);
        grid.get(obstacle.row()).set(obstacle.col(), "#");

        int r = start.row();
        int c = start.col();
        int dr = -1;
        int dc = 0;

        Set<DirectedPosition> seen = new HashSet<>();

        while (true) {
            DirectedPosition current = new DirectedPosition(r, c, dr, dc);
            if (seen.contains(current)) {
                return true;
            }

            seen.add(current);

            if (isOutOfBounds(grid, r + dr, c + dc)) {
                return false;
            }

            if (grid.get(r + dr).get(c + dc).equals("#")) {
                int temp = dc;
                dc = -dr;
                dr = temp;
            } else {
                r += dr;
                c += dc;
            }
        }
    }

    private List<List<String>> gridCopy(List<List<String>> originalGrid) {
        List<List<String>> copy = new ArrayList<>();

        for (List<String> row : originalGrid) {
            copy.add(new ArrayList<>(row));
        }

        return copy;
    }
}

record DirectedPosition(int row, int col, int dr, int dc) {}

record Position(int row, int col) {
    public Position move(int row, int col) {
        return new Position(this.row + row, this.col + col);
    }
}
