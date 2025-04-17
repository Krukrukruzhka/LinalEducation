export function getMatrixById(id) {
    let matrixElement = document.getElementById(id);
    let matrix = [];
    let rows = matrixElement.getElementsByClassName("matrix_row");
    for (let matrix_row of rows) {
        matrix.push([]);
        let n = matrix.length;
        let matrix_values = matrix_row.getElementsByClassName("matrix_element");
        for (let matrix_element of matrix_values) {
            matrix[n - 1].push(matrix_element.value);
        }
    }

    return matrix;
}