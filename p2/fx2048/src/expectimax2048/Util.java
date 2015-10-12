package expectimax2048;

import java.util.Arrays;
import java.util.Collections;

/**
 * Created by kradalby on 12/10/15.
 */
public class Util {
    // Rotate NxN int matrix in-place
    // This is an inplace transpose, followed by an inplace reflection along y direction in the middle
    public static void inplaceRotate(int[][] arr){
        inplaceTranspose(arr);
        inplaceReflect(arr);
    }

    // pre: arr is square
    public static void inplaceReflect(int[][] arr){
        int size = arr.length;
        for(int k=0; k < size; k++){
            for(int i=0; i < Math.floor(size/2); i++){
                swap(arr, k, i, k, size-i-1);
            }
        }
    }

    // pre: matrix is square
    public static void inplaceTranspose(int[][] arr){
        int size = arr.length;
        for(int diag = 0; diag < size; diag++){
            for(int i=diag+1; i<size; i++){
                swap(arr, diag, i, i, diag);
            }
        }
    }

    public static void inplaceReverse(int[][] arr) {
        int size = arr.length;
        for(int j = 0; j < arr.length; j++){
            for(int i = 0; i < arr[j].length / 2; i++) {
                int temp = arr[j][i];
                arr[j][i] = arr[j][arr[j].length - i - 1];
                arr[j][arr[j].length - i - 1] = temp;
            }
        }
    }

    // Swaps elements of int array
    public static void swap(int[][] arr, int row1, int col1, int row2, int col2){
        int num1 = arr[row1][col1];
        int num2 = arr[row2][col2];
        arr[row1][col1] = num2;
        arr[row2][col2] = num1;
    }
}
