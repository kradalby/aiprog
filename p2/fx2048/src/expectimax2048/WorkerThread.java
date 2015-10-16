package expectimax2048;

import game2048.Direction;

import java.util.Arrays;
import java.util.Map;

/**
 * Created by kradalby on 13/10/15.
 */
public class WorkerThread implements Runnable {

    private String name;
    private Node node;
    private Direction dir;
    private int depth;
    private Map<Double, Direction> scores;

    public WorkerThread(String s, Node node, Direction dir, int depth, Map<Double, Direction> scores) {
        this.name = s;
        this.node = node;
        this.dir = dir;
        this.depth = depth;
        this.scores = scores;
    }

    @Override
    public void run() {
        double score = Expectiminimax.expectiminimax(node, depth);
        scores.put(score, dir);
    }
}
