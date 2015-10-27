package expectimax2048;

import game2048.Direction;
import game2048.Location;
import game2048.Tile;

import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

/**
 * Created by kradalby on 12/10/15.
 */
public class Expectiminimax {

    public Expectiminimax() {
    }

    // Expectiminimax imlementation
    public static double expectiminimax(Node node, int depth) {
        double alpha = 0.0;

        if (depth == 0) {
            double heuristic = node.heuristicScore();
            return heuristic;
        }

        if (node.getType() == NodeType.MAX) {
            alpha = Double.NEGATIVE_INFINITY;

            // Get all permutations of the board based on move
            Node[] children = node.getMovePermutations();

            for (Node child : children) {
                alpha = Math.max(alpha, expectiminimax(child, depth - 1));
            }

        } else if (node.getType() == NodeType.CHANCE) {
            alpha = 0.0;

            // Get all permutations of the board based on random spawns
            Node[] children = node.getPermutations();

            for (Node child : children) {
                alpha += child.getProbability(children.length) * expectiminimax(child, depth - 1);
            }

        }
        return alpha;

    }

    // Change the depth dynamically based on empty squares.
    public int getDynamicDepth(Node node, int baseDepth) {
        int depth = baseDepth;

        if (node.getNumberOfEmptyCells() != 0) {
            if (node.getNumberOfEmptyCells() <= 1) {
                depth = baseDepth + 5;
            } else if (node.getNumberOfEmptyCells() < 2) {
                depth = baseDepth + 4;
            } else if (node.getNumberOfEmptyCells() < 4) {
                depth = baseDepth + 3;
            } else if (node.getNumberOfEmptyCells() < 6) {
                depth = baseDepth + 2;
            } else if (node.getNumberOfEmptyCells() < 8) {
                depth = baseDepth + 1;
            } else {
                depth = baseDepth;
            }
            System.out.println("Changed depth to " + depth);
        }

        return depth;

    }

    /*
    Single thread usage of expectiminimax.
    runs expectimax for each move, compares and returns the
    best direction.
     */
    public Direction runExpectiminimax(Node node, int depth) {
        Map<Double, Direction> scores = new HashMap<>();
        depth = getDynamicDepth(node, depth);

        Node up = node.getUp();
        Node right = node.getRight();
        Node down = node.getDown();
        Node left = node.getLeft();

        if (!Arrays.deepEquals(node.getBoard(), up.getBoard())) {
            scores.put(this.expectiminimax(node.getUp(), depth), Direction.UP);
        }
        if (!Arrays.deepEquals(node.getBoard(), right.getBoard())) {
            scores.put(this.expectiminimax(node.getRight(), depth), Direction.RIGHT);
        }
        if (!Arrays.deepEquals(node.getBoard(), down.getBoard())) {
            scores.put(this.expectiminimax(node.getDown(), depth), Direction.DOWN);
        }
        if (!Arrays.deepEquals(node.getBoard(), left.getBoard())) {
            scores.put(this.expectiminimax(node.getLeft(), depth), Direction.LEFT);
        }

        double heuristic = Collections.max(scores.keySet());
        Direction dir = scores.get(heuristic);

        System.out.println("Scores:");
        System.out.println(new PrettyPrintingMap<Double, Direction>(scores));

        System.out.println("Heuristic: " + heuristic);

        return dir;
    }

    /*
    Multi thread usage of expectiminimax.
    runs expectimax for each move, compares and returns the
    best direction.
    Currently got some bugs.
     */
    public Direction runExpectiminimaxThreaded(Node node, int depth) {
        depth = getDynamicDepth(node, depth);

        Map<Double, Direction> scores = new HashMap<>();
        //System.out.println(new PrettyPrintingMap<Double, Direction>(scores));

        Node up = node.getUp();
        Node right = node.getRight();
        Node down = node.getDown();
        Node left = node.getLeft();

        ExecutorService executor = Executors.newFixedThreadPool(4);
        if (!Arrays.deepEquals(node.getBoard(), up.getBoard())) {
            Runnable workerUp = new WorkerThread("UP", up, Direction.UP, depth, scores);
            executor.execute(workerUp);
        }
        if (!Arrays.deepEquals(node.getBoard(), right.getBoard())) {
            Runnable workerRight = new WorkerThread("RIGHT", right, Direction.RIGHT, depth, scores);
            executor.execute(workerRight);
        }
        if (!Arrays.deepEquals(node.getBoard(), down.getBoard())) {
            Runnable workerDown = new WorkerThread("DOWN", down, Direction.DOWN, depth, scores);
            executor.execute(workerDown);
        }
        if (!Arrays.deepEquals(node.getBoard(), left.getBoard())) {
            Runnable workerLeft = new WorkerThread("LEFT", left, Direction.LEFT, depth, scores);
            executor.execute(workerLeft);
        }

        executor.shutdown();
        //while (!executor.isTerminated()) {}
        try {
            executor.awaitTermination(Long.MAX_VALUE, TimeUnit.NANOSECONDS);
        } catch (InterruptedException e) {

        }

        System.out.println("Scores:");
        System.out.println(new PrettyPrintingMap<Double, Direction>(scores));
        double heuristic = Collections.max(scores.keySet());
        Direction dir = scores.get(heuristic);

        System.out.println("Heuristic: " + heuristic);
        System.out.println("Direction: " + dir.toString());

        return dir;
    }

    /*
    The entrypoint for FX2048, takes a board representation and returns
    the best direction.
     */
    public Direction getNextMove(Map<Location, Tile> current, boolean threaded) {
        Direction dir;
        //System.out.println("Getting next move");
        int baseDepth = 3;
        Node node = new Node(NodeType.CHANCE);
        node.populateBoard(current);

        threaded = false;
        if (threaded) {
            dir = runExpectiminimaxThreaded(node, baseDepth);
        } else {
            dir = runExpectiminimax(node, baseDepth);
        }


        System.out.println(dir);


        return dir;
    }

}
