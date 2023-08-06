use numpy::ndarray::Array1;
use numpy::{IntoPyArray, PyArray1, PyReadonlyArray2};
use pyo3::exceptions::PyValueError;
use pyo3::{pymodule, types::PyModule, PyErr, PyResult, Python};

#[pymodule]
fn unique_with_tol(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    #[pyfn(m)]
    #[pyo3(name = "indices_unique_with_tol")]
    fn indices_unique_with_tol<'py>(
        py: Python<'py>,
        a: PyReadonlyArray2<'_, f64>,
        tol: f64,
    ) -> PyResult<&'py PyArray1<i32>> {
        let a = a.as_array();
        // let a: Vec<ArrayView1<f64>> = a.axis_iter(Axis(0)).collect();

        let mut inverses: Vec<i32> = vec![-1; a.nrows()];
        let mut index = 0;

        loop {
            // get index of element in inverses that is -1
            let i = match inverses.iter().position(|&x| x == -1) {
                Some(i) => i,
                None => break,
            };

            for j in 0..a.nrows() {
                let distance = a
                    .row(i)
                    .iter()
                    .zip(a.row(j).iter())
                    .fold(0.0, |acc, (x, y)| acc + (x - y).powi(2));
                if distance < tol.powi(2) {
                    if inverses[j] != -1 {
                        return Err(PyErr::new::<PyValueError, _>(
                            "The radius graph is a disjoint union of cliques.",
                        ));
                    }
                    inverses[j] = index;
                }
            }

            index += 1;
        }
        Ok(Array1::from(inverses).into_pyarray(py))
    }

    Ok(())
}
