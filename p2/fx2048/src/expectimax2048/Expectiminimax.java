package expectimax2048;

import game2048.Direction;
import game2048.Location;
import game2048.Tile;

import java.util.Map;

/**
 * Created by kradalby on 12/10/15.
 */
public class Expectiminimax {

    public Expectiminimax() {
    }

    public double expectiminimax(Node node, int depth) {
        double alpha = 0;
        if (depth == 0) {
            return 0.0;
        }

//        if () {
//            alpha = 999999999;
//            for (Node child: node.getPermutations()) {
//                alpha = Math.min(alpha, expectiminimax(child, depth - 1));
//            }
//        }
        if (node.getTurn()) {
            alpha = -999999999;
            for (Node child: node.getMovePermutations()) {
                alpha = Math.max(alpha, expectiminimax(child, depth - 1));
            }
        }
        else if (!node.getTurn()) {
            alpha = 0;
            for (Node child: node.getPermutations()) {
                alpha = alpha + (node.getProbability() * expectiminimax(child, depth -1));
            }
        }
        return alpha;

    }

    public Direction getNextMove(Map<Location, Tile> current, int score) {
        Node node = new Node();
        node.setScore(score);
        node.populateBoard(current);


    }


}
