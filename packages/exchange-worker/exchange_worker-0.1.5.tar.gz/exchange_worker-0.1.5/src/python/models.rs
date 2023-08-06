use pyo3::prelude::*;
use serde_json::Value;
use crate::binance_connector::BinanceTick;

#[pyclass]
#[derive(Debug)]
pub struct TickData {
    #[pyo3(get)]
    pub update_id: u64,
    #[pyo3(get)]
    pub symbol: String,
    #[pyo3(get)]
    pub bid: String,
    #[pyo3(get)]
    pub bid_size: String,
    #[pyo3(get)]
    pub ask: String,
    #[pyo3(get)]
    pub ask_size: String,  // ask_size
}

impl From<BinanceTick> for TickData {
    fn from(value: BinanceTick) -> Self {
        Self {
            update_id: value.data.u,
            symbol: value.data.s,
            bid: value.data.b,
            bid_size: value.data.B,
            ask: value.data.a,
            ask_size: value.data.A,
        }
    }
}

#[pymethods]
impl TickData {
    // For `__repr__` we want to return a string that Python code could use to recreate
    // the `Number`, like `Number(5)` for example.
    fn __repr__(&self) -> String {
        // We use the `format!` macro to create a string. Its first argument is a
        // format string, followed by any number of parameters which replace the
        // `{}`'s in the format string.
        format!("TickData: symbol={symbol} bid={bid} ask={ask}",
                ask = &self.ask,
                bid = &self.bid,
                symbol = &self.symbol,
        )
    }

    // `__str__` is generally used to create an "informal" representation, so we
    // just forward to `i32`'s `ToString` trait implementation to print a bare number.
    fn __str__(&self) -> String {
        self.__repr__()
    }
}
