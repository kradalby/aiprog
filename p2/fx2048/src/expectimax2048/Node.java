package expectimax2048;

import game2048.Direction;
import game2048.Location;
import game2048.Tile;

import java.awt.*;
import java.util.*;


/**
 * Created by kradalby on 12/10/15.
 */
public class Node {
    private int[][] board;
    private double probability;
    private NodeType type;
    private int score;
    private ArrayList<Point> empty;
    private int emptyScore = 0;

    private static int[][] snake = new int[][] {
            {1024,512,256,256},
            {32,64,64,128},
            {0,0,0,0},
            {0,0,0,0}
    };

    private static int[][] gradiantRight = new int[][] {
            {0,1,2,3},
            {-1,0,1,2},
            {-2,-1,0,1},
            {-3,-2,-1,0}
    };
    private static int[][] gradiantLeft = new int[][] {
            {3,2,1,0},
            {2,1,0,-1},
            {1,0,-1,-2},
            {0,-1,-2,-3}
    };

    public Node(NodeType type) {
        this.type = type;
        empty = new ArrayList<>();
        board = new int [][] {
                {0,0,0,0},
                {0,0,0,0},
                {0,0,0,0},
                {0,0,0,0}
        };
    }

    public Node newNode(NodeType type) {
        Node node = new Node(type);
        node.setBoard(this.getCopyOfBoard());
        node.setScore(this.score);

        return node;
    }

    public Node getLeft() {
        Node node = this.newNode(NodeType.CHANCE);
        node.moveLeft();
        return node;
    }

    public Node getRight() {
        Node node = this.newNode(NodeType.CHANCE);
        Util.inplaceReverse(node.getBoard());
        node.moveLeft();
        Util.inplaceReverse(node.getBoard());
        return node;
    }

    public Node getUp() {
        Node node = this.newNode(NodeType.CHANCE);
        Util.inplaceRotate(node.getBoard());
        Util.inplaceRotate(node.getBoard());
        Util.inplaceRotate(node.getBoard());
        node.moveLeft();
        Util.inplaceRotate(node.getBoard());
        return node;
    }

    public Node getDown() {
        Node node = this.newNode(NodeType.CHANCE);
        Util.inplaceRotate(node.getBoard());
        node.moveLeft();
        Util.inplaceRotate(node.getBoard());
        Util.inplaceRotate(node.getBoard());
        Util.inplaceRotate(node.getBoard());

        return node;
    }

    public Node[] getMovePermutations() {
        Node[] nodes = new Node[4];
        nodes[0] = this.getUp();
        nodes[1] = this.getDown();
        nodes[2] = this.getLeft();
        nodes[3] = this.getRight();
        return nodes;
    }

    public Node[] getPermutations() {
        getNumberOfEmptyCells();
        ArrayList<Node> nodes = new ArrayList<>();
        for (Point t: empty) {
            Node node2 = this.newNode(NodeType.MAX);
            node2.setProbability(0.9);
            node2.getBoard()[t.y][t.x] = 2;
            nodes.add(node2);

            Node node4 = this.newNode(NodeType.MAX);
            node4.setProbability(0.1);
            node4.getBoard()[t.y][t.x] = 4;
            nodes.add(node4);

        }
        return nodes.toArray(new Node[nodes.size()]);
    }

    public void populateBoard(Map<Location, Tile> grid) {
        for (Location loc : grid.keySet()) {
            Tile t = grid.get(loc);
            if (t != null) {
                this.board[loc.getY()][loc.getX()] = t.getValue().intValue();
            }
        }
        System.out.println(this);
    }

    private int[][] getCopyOfBoard() {
        int[][] newBoard = new int[4][4];
        for (int i = 0; i < this.board.length; i++) {
            newBoard[i] = this.board[i].clone();
        }
        return newBoard;
    }

    private void moveLeft() {
        for (int row = 0; row < this.board.length; row++) {
            for (int i = 0; i < this.board[row].length; i++) {
                for (int n = i+1; n < this.board[row].length; n++) {
                    // If two neighbors are not equal, go to next item
                    if (this.board[row][n] != 0 && this.board[row][i] != this.board[row][n]) {
                        break;
                    }
                    if (this.board[row][n] != 0) {
                        if (this.board[row][i] == this.board[row][n]) {
                            this.board[row][i] = this.board[row][i] * 2;
                            this.board[row][n] = 0;
                            break;
                        }
                    }
                }
            }

            // Move all the things
            for (int i = 0; i < this.board[row].length; i++) {
                if (this.board[row][i] == 0 && this.board[row].length > i + 1) {
                    this.board[row][i] = this.board[row][i+1];
                    this.board[row][i+1] = 0;
                }
            }

            for (int i = 0; i < this.board[row].length; i++) {
                if (this.board[row][i] == 0 && this.board[row].length > i + 1) {
                    this.board[row][i] = this.board[row][i+1];
                    this.board[row][i+1] = 0;
                }
            }

            for (int i = 0; i < this.board[row].length; i++) {
                if (this.board[row][i] == 0 && this.board[row].length > i + 1) {
                    this.board[row][i] = this.board[row][i+1];
                    this.board[row][i+1] = 0;
                }
            }
        }
    }

    public int getNumberOfEmptyCells(){
        if (this.emptyScore == 0) {
            for (int row = 0; row < this.getBoard().length; row++) {
                for (int col = 0; col < this.getBoard()[row].length; col++) {
                    if (this.getBoard()[row][col] == 0) {
                        this.empty.add(new Point(col, row));
                    }
                }
            }
            this.emptyScore = this.empty.size();
        }
        return this.emptyScore;
    }

    private  int calculateClusteringScore() {
        int clusteringScore=0;
        int [][] boardArray = this.board;

        int[] neighbors = {-1,0,1};

        for(int i=0;i<boardArray.length;++i) {
            for(int j=0;j<boardArray.length;++j) {
                if(boardArray[i][j]==0) {
                    continue;
                }

                int numOfNeighbors=0;
                int sum=0;
                for(int k : neighbors) {
                    int x=i+k;
                    if(x<0 || x>=boardArray.length) {
                        continue;
                    }
                    for(int l : neighbors) {
                        int y = j+l;
                        if(y<0 || y>=boardArray.length) {
                            continue;
                        }

                        if(boardArray[x][y]>0) {
                            ++numOfNeighbors;
                            sum+=Math.abs(boardArray[i][j]-boardArray[x][y]);
                        }

                    }
                }

                clusteringScore+=sum/numOfNeighbors;
            }
        }

        //return 0;
        return clusteringScore;
    }

    public double compareBoardToWeightMatrix(int[][] weightMatrix, int[][] board) {
        double score = 0.0;

        for (int row = 0; row < board.length; row++) {
            for (int i = 0; i < board[row].length; i++) {
                score += weightMatrix[row][i] * board[row][i];
            }
        }
        return score;
    }

    public double calculatePotentialMergerScore() {
        double score = 0.0;



        return score;
    }

    public double heuristicScore() {
        double score = 0.0;

        double[] weightMatrixList = new double[4];
        for (int i = 0; i < 4; i++) {
            Util.inplaceRotate(gradiantLeft);
            weightMatrixList[i] = this.compareBoardToWeightMatrix(gradiantLeft, this.board);
        }

        Arrays.sort(weightMatrixList);
        double weightMatrix = weightMatrixList[weightMatrixList.length - 1];
        //double weightMatrix = this.compareBoardToWeightMatrix(gradiantLeft, this.board);

        score = weightMatrix;

        return score;
    }

    public int[][] getBoard(){
        return this.board;
    }

    public void setBoard(int[][] board) {
        this.board = board;
    }

    public double getProbability(int possibleChildren) {
        double halfPossibleChildren = possibleChildren / 2;
        double chance = (1 / halfPossibleChildren) * probability;
        return chance;
    }

    public void setProbability(double probability) {
        this.probability = probability;
    }

    public NodeType getType() {
        return this.type;
    }

    public int getScore() {
        return score;
    }

    public void setScore(int score) {
        this.score = score;
    }

    @Override
    public String toString() {
        String s = "";
        for (int row = 0; row < this.board.length; row++) {
            for (int i = 0; i < this.board[row].length; i++) {
                s += this.board[row][i];
                s += " ";
            }
            s += "\n";
        }
        return s;
    }

    public static void main(String[] args) {
        Node node = new Node(NodeType.MAX);
        node.setBoard(new int [][] {
                {4,4,0,0},
                {2,0,0,0},
                {0,0,0,0},
                {0,0,0,0},
        });
        //node = node.getLeft();
        //System.out.println("stuff");
        //Node[] nodes = node.getPermutations();
        //System.out.println("derp");
        //for (Node n : nodes) {
        //    System.out.println(n);
        //}



        Expectiminimax e = new Expectiminimax();
        System.out.println(e.runExpectiminimax(node, 8));
        System.out.println(node);

        for (Node child: node.getMovePermutations()) {
            System.out.println(child);
            System.out.println(child.heuristicScore());
        }

    }
}

