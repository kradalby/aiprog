package expectimax2048;

import game2048.Direction;
import game2048.Location;
import game2048.Tile;

import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

/**
 * Created by kradalby on 12/10/15.
 */
public class Expectiminimax {

    public Expectiminimax() {
    }

    public double expectiminimax(Node node, int depth) {
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
            for (Node child : node.getMovePermutations()) {
                alpha = Math.max(alpha, expectiminimax(child, depth - 1));
            }
        } else if (!node.getTurn()) {
            alpha = 0;
            for (Node child : node.getPermutations()) {
                alpha = alpha + (node.getProbability() * expectiminimax(child, depth - 1));
            }
        }
        return alpha;

    }

    public Direction getNextMove(Map<Location, Tile> current, int score) {
        System.out.println("Getting next move");
        Map<Double, Direction> scores = new HashMap<>();
        int depth = 8;
        Node node = new Node();
        node.setScore(score);
        node.populateBoard(current);

        System.out.println(new PrettyPrintingMap<Double, Direction>(scores));

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

        System.out.println(new PrettyPrintingMap<Double, Direction>(scores));

        return scores.get((Collections.max(scores.keySet())));
    }


}
