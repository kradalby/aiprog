package expectimax2048;

import game2048.Direction;
import game2048.Location;
import game2048.Tile;

import java.util.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

/**
 * Created by kradalby on 12/10/15.
 */
public class Expectiminimax {

    public Expectiminimax() {
    }

    public static double expectiminimax(Node node, int depth) {
        //System.out.println("Starting Expectiminimax");
        double alpha = 0;
        if (depth == 0) {
            //System.out.println("Reached depth 0");
            return node.heuristicScore();
        }

//        if () {
//            alpha = 999999999;
//            for (Node child: node.getPermutations()) {
//                alpha = Math.min(alpha, expectiminimax(child, depth - 1));
//            }
//        }
        if (node.getTurn()) {
            alpha = -999999999;
            ArrayList<Node> children = node.getPermutations();
            //System.out.println("--------------------------------");
            //System.out.println(node.getTurn());
            //for (Node child : children) {
            //    System.out.println(child);
            //}
            //System.out.println("--------------------------------");
            for (Node child : children) {
                alpha = Math.max(alpha, expectiminimax(child, depth - 1));
            }
        } else if (!node.getTurn()) {
            alpha = 0;
            Node[] children = node.getMovePermutations();
            //System.out.println("--------------------------------");
            //System.out.println(node.getTurn());
            //for (Node child : children) {
            //    System.out.println(child);
            //}
            //System.out.println("--------------------------------");
            for (Node child : children) {
                alpha = alpha + (node.getProbability() * expectiminimax(child, depth - 1));
            }
        }
        //System.out.println(depth);
        return alpha;

    }

    public int getDynamicDepth(Node node, int baseDepth) {
        int depth = baseDepth;

        if (node.getNumberOfEmptyCells() != 0) {
            if (node.getNumberOfEmptyCells() < 3) {
                depth = baseDepth + 2;
                System.out.println("Changed depth to " + depth);
            } else if (node.getNumberOfEmptyCells() < 6) {
                depth = baseDepth + 1;
                System.out.println("Changed depth to " + depth);
            } else {
                depth = baseDepth;
                System.out.println("Changed depth to " + depth);
            }
        }

        return depth;

    }

    public Direction getNextMove(Map<Location, Tile> current, int score) {
        System.out.println("Getting next move");
        Map<Double, Direction> scores = new HashMap<>();
        int baseDepth = 3;
        int depth = baseDepth;
        Node node = new Node();
        node.setScore(score);
        node.populateBoard(current);
        node.getPermutations();

        depth = getDynamicDepth(node, baseDepth);

        System.out.println(new PrettyPrintingMap<Double, Direction>(scores));

        Node up = node.getUp();
        //Node right = node.getRight();
        Node down = node.getDown();
        Node left = node.getLeft();

        if (!Arrays.deepEquals(node.getBoard(), up.getBoard())) {
            scores.put(this.expectiminimax(node.getUp(), depth), Direction.UP);
        }
        // if (!Arrays.deepEquals(node.getBoard(), right.getBoard())) {
        //     scores.put(this.expectiminimax(node.getRight(), depth), Direction.RIGHT);
        // }
        if (!Arrays.deepEquals(node.getBoard(), down.getBoard())) {
            scores.put(this.expectiminimax(node.getDown(), depth), Direction.DOWN);
        }
        if (!Arrays.deepEquals(node.getBoard(), left.getBoard())) {
            scores.put(this.expectiminimax(node.getLeft(), depth), Direction.LEFT);
        }

        System.out.println(new PrettyPrintingMap<Double, Direction>(scores));

        return scores.get((Collections.max(scores.keySet())));
    }

    public Direction getNextMoveThreaded(Map<Location, Tile> current, int score) {
        System.out.println("Getting next threaded move");
        Map<Double, Direction> scores = new HashMap<>();
        int baseDepth = 3;
        int depth = baseDepth;
        Node node = new Node();
        node.setScore(score);
        node.populateBoard(current);
        node.getPermutations();

        depth = getDynamicDepth(node, baseDepth);

        //System.out.println(new PrettyPrintingMap<Double, Direction>(scores));

        Node up = node.getUp();
        //Node right = node.getRight();
        Node down = node.getDown();
        Node left = node.getLeft();

        ExecutorService executor = Executors.newFixedThreadPool(4);
        if (!Arrays.deepEquals(node.getBoard(), up.getBoard())) {
            Runnable workerUp = new WorkerThread("UP", up, Direction.UP, depth, scores);
            executor.execute(workerUp);
        }
        // if (!Arrays.deepEquals(node.getBoard(), right.getBoard())) {
        //     Runnable workerRight = new WorkerThread("RIGHT", right, Direction.RIGHT, depth, scores);
        //     executor.execute(workerRight);
        // }
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

        return scores.get((Collections.max(scores.keySet())));
    }

}
