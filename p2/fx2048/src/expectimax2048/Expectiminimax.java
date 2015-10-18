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

    public static double highest = 0.0;

    public Expectiminimax() {
    }

    public static double expectiminimax(Node node, int depth) {
        double alpha = 0.0;

        if (depth == 0) {
            double heuristic = node.heuristicScore();
            return heuristic;
        }

        if (node.getType() == NodeType.MAX) {
            //System.out.println("Got a max node");
            alpha = Double.NEGATIVE_INFINITY;

            Node[] children = node.getMovePermutations();

            for (Node child : children) {
                alpha = Math.max(alpha, expectiminimax(child, depth - 1));
            }

        } else if (node.getType() == NodeType.CHANCE) {
            //System.out.println("Got a Chance node");
            alpha = 0.0;

            Node[] children = node.getPermutations();

            for (Node child : children) {
                alpha += child.getProbability() * expectiminimax(child, depth - 1);
            }
        }
        return alpha;

    }

//    public static double expectiminimax(Node node, int depth) {
//        //System.out.println("Starting Expectiminimax");
//        double alpha = 0;
//        if (depth == 0) {
//            double heuristicScore = node.heuristicScore();
//            return heuristicScore;
//        }
//        if (node.getTurn()) {
//            alpha = Double.NEGATIVE_INFINITY;
//            Node[] children = node.getPermutations();
//            for (Node child : children) {
//                alpha = Math.max(alpha, expectiminimax(child, depth - 1));
//            }
//        } else {
//        //} else if (!node.getTurn()) {
//            alpha = 0.0;
//            Node[] children = node.getMovePermutations();
//            for (Node child : children) {
//                System.out.println("PROBABILITY: " + node.getProbability());
//                double result = (node.getProbability() * (expectiminimax(child, depth - 1)));
//                alpha += result;
//
//                if (result > highest) {
//                    highest = result;
//                }
//            }
//            System.out.println("------------------");
//            System.out.println(alpha);
//            System.out.println(children.length);
//            alpha = alpha / children.length;
//            System.out.println("ALPHA RESULT:" + alpha);
//        }
//        return alpha;
//    }

    public int getDynamicDepth(Node node, int baseDepth) {
        int depth = baseDepth;

        if (node.getNumberOfEmptyCells() != 0) {
            if (node.getNumberOfEmptyCells() < 2) {
                depth = baseDepth + 4;
                System.out.println("Changed depth to " + depth);
            } else if (node.getNumberOfEmptyCells() < 4) {
                depth = baseDepth + 3;
                System.out.println("Changed depth to " + depth);
            } else if (node.getNumberOfEmptyCells() < 6) {
                depth = baseDepth + 2;
                System.out.println("Changed depth to " + depth);
            } else if (node.getNumberOfEmptyCells() < 8) {
                depth = baseDepth + 1;
                System.out.println("Changed depth to " + depth);
            } else {
                depth = baseDepth;
                System.out.println("Changed depth to " + depth);
            }
        }

        return depth;

    }

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

        //System.out.println(new PrettyPrintingMap<Double, Direction>(scores));
        double heuristic = Collections.max(scores.keySet());
        Direction dir = scores.get(heuristic);

        System.out.println("Scores:");
        System.out.println(new PrettyPrintingMap<Double, Direction>(scores));

        System.out.println("Heuristic: " + heuristic);

        return dir;
    }

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

    public Direction getNextMove(Map<Location, Tile> current, int score, boolean threaded) {
        Direction dir;
        //System.out.println("Getting next move");
        int baseDepth = 3;
        Node node = new Node(NodeType.CHANCE);
        node.setScore(score);
        node.populateBoard(current);

        threaded = true;
        if (threaded) {
            dir = runExpectiminimaxThreaded(node, baseDepth);
        } else {
            dir = runExpectiminimax(node, baseDepth);
        }

        //System.out.println(node);

        System.out.println(dir);


        return dir;
    }

}
