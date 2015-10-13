package expectimax2048;

import game2048.Location;
import game2048.Tile;

import java.awt.*;
import java.util.*;

/**
 * Created by kradalby on 12/10/15.
 */
public class Node {
    private int[][] board;
    private Node parent;
    private ArrayList<Point> empty;

    public Node() {
        empty = new ArrayList<>();
    }

    public Node getLeft() {
        Node node = new Node();
        node.setParent(this);
        node.setBoard(this.getCopyOfBoard());
        node.moveLeft();
        return node;
    }

    public Node getRight() {
        Node node = new Node();
        node.setParent(this);
        node.setBoard(this.getCopyOfBoard());
        Util.inplaceReverse(node.getBoard());
        node.moveLeft();
        Util.inplaceReverse(node.getBoard());
        return node;
    }

    public Node getUp() {
        Node node = new Node();
        node.setParent(this);
        node.setBoard(this.getCopyOfBoard());
        Util.inplaceRotate(node.getBoard());
        Util.inplaceRotate(node.getBoard());
        Util.inplaceRotate(node.getBoard());
        node.moveLeft();
        Util.inplaceRotate(node.getBoard());
        return node;
    }

    public Node getDown() {
        Node node = new Node();
        node.setParent(this);
        node.setBoard(this.getCopyOfBoard());
        Util.inplaceRotate(node.getBoard());
        node.moveLeft();
        Util.inplaceRotate(node.getBoard());
        Util.inplaceRotate(node.getBoard());
        Util.inplaceRotate(node.getBoard());

        return node;
    }

    public ArrayList<Node> getPermutations() {
        ArrayList<Node> nodes = new ArrayList<>();
        for (Point t: empty) {
            Node node2 = new Node();
            node2.setParent(this);
            node2.setBoard(this.getCopyOfBoard());
            node2.getBoard()[t.y][t.x] = 2;
            nodes.add(node2);

            Node node4 = new Node();
            node4.setParent(this);
            node4.setBoard(this.getCopyOfBoard());
            node4.getBoard()[t.y][t.x] = 4;
            nodes.add(node4);
        }
        return nodes;
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

            // Save all the empty spots
            for (int i = 0; i < this.board[row].length; i++) {
                if (this.board[row][i] == 0) {
                    this.empty.add(new Point(i, row));
                }
            }
        }
    }

    public void populateBoard(Map<Location, Tile> grid) {
        System.out.println(new PrettyPrintingMap<Location, Tile>(grid));
    }

    private int[][] getCopyOfBoard() {
        int[][] newBoard = new int[4][4];
        for (int i = 0; i < this.board.length; i++) {
            newBoard[i] = this.board[i].clone();
        }
        return newBoard;
    }

    public int[][] getBoard(){
        return this.board;
    }


    public Node getParent() {
        return parent;
    }

    public void setParent(Node parent) {
        this.parent = parent;
    }

    public void setBoard(int[][] board) {
        this.board = board;
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
        Node node = new Node();
        node.setBoard(new int [][] {
                {2,2,0,2},
                {2,4,2,2},
                {0,2,2,4},
                {0,0,4,2}
        });
        node = node.getDown();
        System.out.println("stuff");
        ArrayList<Node> nodes = node.getPermutations();
        System.out.println("derp");
        for (Node n : nodes) {
            System.out.println(n);
        }
    }
}

